"""Image slot placeholders and fill helpers.

Agent contract
--------------
- Generation scripts place placeholders (`add_image_placeholder` / page layouts).
- The agent retrieves suitable images by whatever means it chooses.
- Then call registered tool `fill_image_slots` with an explicit
  ``{slot_id: local_path}`` map — no directory scan, no auto search.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt

from .figures import add_figure_on_slide
from .theme import FONT_CN, FS_CAPTION, LIGHT_GRAY, MEDIUM_GRAY, PALE_BLUE

_SLOT_PREFIX = "slot:"
_LABEL_PREFIX = "slot-label:"


@dataclass
class ImageSlot:
    """Rectangular region reserved for a figure."""

    slot_id: str
    left: int
    top: int
    width: int
    height: int
    label: str = ""
    slide_index: int | None = None  # 0-based; set when loaded from a .pptx


def add_image_placeholder(
    slide,
    left,
    top,
    width,
    height,
    slot_id: str,
    label: str = "图示占位",
) -> ImageSlot:
    """Draw a pale frame + hint text. Return slot for later fill_image_slots."""
    frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    frame.fill.solid()
    frame.fill.fore_color.rgb = PALE_BLUE
    frame.line.color.rgb = LIGHT_GRAY
    frame.line.width = Pt(1.25)
    # name used by list/fill from file (agent tools)
    try:
        frame.name = f"{_SLOT_PREFIX}{slot_id}"
    except Exception:
        pass

    hint = slide.shapes.add_textbox(left, top, width, height)
    tf = hint.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = label or slot_id
    run.font.size = Pt(FS_CAPTION)
    run.font.color.rgb = MEDIUM_GRAY
    run.font.name = FONT_CN
    try:
        hint.name = f"{_LABEL_PREFIX}{slot_id}"
    except Exception:
        pass

    return ImageSlot(slot_id=slot_id, left=left, top=top, width=width, height=height, label=label)


def fill_image_slots(slide, slots: dict[str, ImageSlot] | list[ImageSlot], paths: dict[str, str]):
    """Fill reserved slots with caller-provided local paths (in-memory slide).

    Agent / script must supply ``paths`` explicitly. This function never
    searches the filesystem for candidate images.
    Missing paths or unknown slot_ids are skipped; placeholders stay visible.
    """
    if isinstance(slots, list):
        slot_map = {s.slot_id: s for s in slots}
    else:
        slot_map = slots

    placed = {}
    for slot_id, path in paths.items():
        slot = slot_map.get(slot_id)
        if slot is None or not path or not os.path.exists(path):
            continue
        result = add_figure_on_slide(
            slide,
            path,
            left=slot.left,
            top=slot.top,
            max_width=slot.width,
            max_height=slot.height,
        )
        if result is None:
            continue
        pic, w, h = result
        pic.left = int(slot.left + (slot.width - w) / 2)
        pic.top = int(slot.top + (slot.height - h) / 2)
        placed[slot_id] = path
    return placed


def _iter_slot_frames(slide):
    for shape in slide.shapes:
        name = getattr(shape, "name", "") or ""
        if name.startswith(_SLOT_PREFIX) and not name.startswith(_LABEL_PREFIX):
            yield name[len(_SLOT_PREFIX) :], shape


def list_image_slots(pptx_path: str) -> list[dict]:
    """List placeholder slots already marked in a .pptx (by shape name ``slot:id``).

    This only reads slot markers — it does not invent or scan for image files.
    """
    prs = Presentation(pptx_path)
    out: list[dict] = []
    for i, slide in enumerate(prs.slides):
        for slot_id, shape in _iter_slot_frames(slide):
            out.append(
                {
                    "slot_id": slot_id,
                    "slide_index": i,
                    "left": int(shape.left),
                    "top": int(shape.top),
                    "width": int(shape.width),
                    "height": int(shape.height),
                    "label": "",
                }
            )
    return out


def fill_image_slots_pptx(
    pptx_path: str,
    paths: dict[str, str],
    *,
    output_path: str | None = None,
) -> dict:
    """Agent entry: open pptx, fill slots from explicit path map, save.

    Parameters
    ----------
    pptx_path:
        Existing presentation with ``slot:<id>`` placeholders.
    paths:
        ``{slot_id: local_image_path}`` chosen by the agent after retrieval.
        Unknown ids / missing files are skipped (no auto-pick).
    output_path:
        Defaults to overwriting ``pptx_path``.

    Returns
    -------
    dict with keys ``placed``, ``skipped``, ``output_path``.
    """
    if isinstance(paths, str):
        paths = json.loads(paths)

    prs = Presentation(pptx_path)
    # slot_id -> (slide, ImageSlot); last wins if duplicate ids
    index: dict[str, tuple] = {}
    for i, slide in enumerate(prs.slides):
        for slot_id, shape in _iter_slot_frames(slide):
            index[slot_id] = (
                slide,
                ImageSlot(
                    slot_id=slot_id,
                    left=int(shape.left),
                    top=int(shape.top),
                    width=int(shape.width),
                    height=int(shape.height),
                    slide_index=i,
                ),
            )

    placed: dict[str, str] = {}
    skipped: dict[str, str] = {}
    for slot_id, path in paths.items():
        if slot_id not in index:
            skipped[slot_id] = "unknown_slot"
            continue
        if not path or not os.path.exists(path):
            skipped[slot_id] = "missing_file"
            continue
        slide, slot = index[slot_id]
        got = fill_image_slots(slide, {slot_id: slot}, {slot_id: path})
        if slot_id in got:
            placed[slot_id] = path
        else:
            skipped[slot_id] = "place_failed"

    out = output_path or pptx_path
    prs.save(out)
    return {"placed": placed, "skipped": skipped, "output_path": out}


def slots_to_json(slots: dict[str, ImageSlot] | list[ImageSlot]) -> str:
    """Serialize in-memory slots for handoff to an agent tool call."""
    if isinstance(slots, dict):
        items = list(slots.values())
    else:
        items = list(slots)
    return json.dumps([asdict(s) for s in items], ensure_ascii=False, indent=2)
