"""Runtime patch for native SVG picture insertion in python-pptx (PR #1115)."""

from __future__ import annotations

import os
import re
from xml.etree import ElementTree
from xml.sax.saxutils import escape

from pptx.opc.constants import CONTENT_TYPE as CT
from pptx.opc.package import PartFactory
from pptx.opc.spec import image_content_types
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pptx.oxml.shapes import groupshape as gs_mod
from pptx.oxml.shapes import picture as pic_mod
from pptx.parts import image as img_mod
from pptx.parts.image import Image, ImagePart
from pptx.shapes import shapetree as st_mod

_SVG_NS = "http://www.w3.org/2000/svg"
_SVG_LENGTH_RE = re.compile(
    r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.?\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z%]*)\s*$"
)
_SVG_PX_PER_INCH = 96.0
_PATCHED = False


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _is_svg(blob: bytes, filename: str | None) -> bool:
    if filename is not None and os.path.splitext(filename)[1].lower() == ".svg":
        return True
    stripped = blob.lstrip()
    if not stripped.startswith(b"<"):
        return False
    try:
        root = ElementTree.fromstring(blob)
    except ElementTree.ParseError:
        return False
    return _local_name(root.tag) == "svg"


def _svg_viewbox(svg: ElementTree.Element):
    view_box = svg.get("viewBox")
    if view_box is None:
        return None
    parts = view_box.replace(",", " ").split()
    if len(parts) != 4:
        raise ValueError("SVG viewBox must contain four numeric values")
    _, _, width, height = (float(part) for part in parts)
    if width <= 0 or height <= 0:
        raise ValueError("SVG viewBox dimensions must be greater than zero")
    return width, height


def _svg_length_to_px(length: str | None):
    if length is None:
        return None
    match = _SVG_LENGTH_RE.match(length)
    if match is None:
        raise ValueError(f"unsupported SVG length value '{length}'")
    magnitude = float(match.group(1))
    unit = match.group(2).lower() or "px"
    if unit == "%":
        return None
    if unit == "px":
        return magnitude
    if unit == "in":
        return magnitude * _SVG_PX_PER_INCH
    if unit == "cm":
        return magnitude * _SVG_PX_PER_INCH / 2.54
    if unit == "mm":
        return magnitude * _SVG_PX_PER_INCH / 25.4
    if unit == "pt":
        return magnitude * _SVG_PX_PER_INCH / 72.0
    if unit == "pc":
        return magnitude * _SVG_PX_PER_INCH / 6.0
    raise ValueError(f"unsupported SVG length unit '{unit}'")


def _svg_viewport_px_size(svg: ElementTree.Element):
    viewbox = _svg_viewbox(svg)
    width_px = _svg_length_to_px(svg.get("width"))
    height_px = _svg_length_to_px(svg.get("height"))
    if width_px is None and height_px is None and viewbox is None:
        return 300.0, 150.0
    if viewbox is not None:
        viewbox_width, viewbox_height = viewbox
        if width_px is None and height_px is None:
            return viewbox_width, viewbox_height
        if width_px is None:
            return height_px * viewbox_width / viewbox_height, height_px
        if height_px is None:
            return width_px, width_px * viewbox_height / viewbox_width
    if width_px is None or height_px is None:
        raise ValueError("SVG width and height must both be specified unless viewBox is present")
    if width_px <= 0 or height_px <= 0:
        raise ValueError("SVG dimensions must be greater than zero")
    return width_px, height_px


class Svg(Image):
    @property
    def content_type(self):
        return CT.SVG

    @property
    def dpi(self):
        return (int(_SVG_PX_PER_INCH), int(_SVG_PX_PER_INCH))

    @property
    def ext(self):
        return "svg"

    @property
    def _format(self):
        return "SVG"

    @property
    def size(self):
        return self._px_size

    @property
    def _px_size(self):
        width_px, height_px = _svg_viewport_px_size(self._root)
        return int(round(width_px)), int(round(height_px))

    @property
    def _root(self):
        root = ElementTree.fromstring(self._blob)
        if _local_name(root.tag) != "svg":
            raise ValueError("image blob is not an SVG document")
        return root


class SvgImagePart(ImagePart):
    @property
    def image(self):
        return Svg(self._blob, self.desc)


def _svg_pic_tmpl():
    return (
        "<p:pic %s>\n"
        "  <p:nvPicPr>\n"
        '    <p:cNvPr id="%%d" name="%%s" descr="%%s"/>\n'
        "    <p:cNvPicPr>\n"
        '      <a:picLocks noChangeAspect="1"/>\n'
        "    </p:cNvPicPr>\n"
        "    <p:nvPr/>\n"
        "  </p:nvPicPr>\n"
        "  <p:blipFill>\n"
        '    <a:blip r:embed="%%s">\n'
        "      <a:extLst>\n"
        '        <a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">\n'
        '          <asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="%%s"/>\n'
        "        </a:ext>\n"
        "      </a:extLst>\n"
        "    </a:blip>\n"
        "    <a:stretch>\n"
        "      <a:fillRect/>\n"
        "    </a:stretch>\n"
        "  </p:blipFill>\n"
        "  <p:spPr>\n"
        "    <a:xfrm>\n"
        '      <a:off x="%%d" y="%%d"/>\n'
        '      <a:ext cx="%%d" cy="%%d"/>\n'
        "    </a:xfrm>\n"
        '    <a:prstGeom prst="rect">\n'
        "      <a:avLst/>\n"
        "    </a:prstGeom>\n"
        "  </p:spPr>\n"
        "</p:pic>" % nsdecls("a", "p", "r")
    )


def _new_svg_pic(shape_id, name, desc, rId, x, y, cx, cy):
    return parse_xml(_svg_pic_tmpl() % (shape_id, name, escape(desc), rId, rId, x, y, cx, cy))


def _add_svg_pic(grp_sp, id_, name, desc, rId, x, y, cx, cy):
    pic = _new_svg_pic(id_, name, desc, rId, x, y, cx, cy)
    grp_sp.insert_element_before(pic, "p:extLst")
    return pic


def _image_from_blob(blob, filename=None):
    if _is_svg(blob, filename):
        return Svg(blob, filename)
    return Image(blob, filename)


def _image_part_new(cls, package, image):
    part_cls = SvgImagePart if isinstance(image, Svg) else cls
    return part_cls(
        package.next_image_partname(image.ext),
        image.content_type,
        package,
        image.blob,
        image.filename,
    )


def _add_pic_from_image_part(self, image_part, rId, x, y, cx, cy):
    id_ = self._next_shape_id
    scaled_cx, scaled_cy = image_part.scale(cx, cy)
    name = "Picture %d" % (id_ - 1)
    desc = image_part.desc
    if image_part.ext == "svg":
        pic = _add_svg_pic(self._grpSp, id_, name, desc, rId, x, y, scaled_cx, scaled_cy)
    else:
        pic = self._grpSp.add_pic(id_, name, desc, rId, x, y, scaled_cx, scaled_cy)
    return pic


def apply_pptx_svg_support():
    global _PATCHED
    if _PATCHED:
        return

    if not hasattr(CT, "SVG"):
        CT.SVG = "image/svg+xml"
    image_content_types["svg"] = CT.SVG

    img_mod.Svg = Svg
    img_mod.SvgImagePart = SvgImagePart
    Image.from_blob = classmethod(lambda cls, blob, filename=None: _image_from_blob(blob, filename))
    ImagePart.new = classmethod(_image_part_new)

    pic_mod.CT_Picture.new_svg_pic = classmethod(
        lambda cls, shape_id, name, desc, rId, x, y, cx, cy:
        _new_svg_pic(shape_id, name, desc, rId, x, y, cx, cy)
    )
    gs_mod.CT_GroupShape.add_svg_pic = _add_svg_pic

    st_mod._BaseGroupShapes._add_pic_from_image_part = _add_pic_from_image_part

    PartFactory.part_type_for[CT.SVG] = SvgImagePart
    _PATCHED = True
