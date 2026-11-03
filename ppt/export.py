"""PPTX → PDF export via LibreOffice (preferred) or Spire fallback."""

from __future__ import annotations

import os
import shutil
import subprocess

from .theme import LIBREOFFICE_PORTABLE


def find_soffice():
    """Return (soffice_path, env) or (None, None)."""
    if os.path.isfile(LIBREOFFICE_PORTABLE):
        lo_prog = os.path.dirname(LIBREOFFICE_PORTABLE)
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = lo_prog + (
            ":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else ""
        )
        return LIBREOFFICE_PORTABLE, env

    system_lo = shutil.which("libreoffice") or shutil.which("soffice")
    if system_lo:
        return system_lo, os.environ.copy()
    return None, None


def export_pdf(pptx_path, pdf_path):
    """Convert PPTX to PDF. Prefer LibreOffice for full slide count."""
    soffice, env = find_soffice()
    if soffice:
        out_dir = os.path.dirname(pdf_path) or "."
        os.makedirs(out_dir, exist_ok=True)
        cmd = [
            soffice, "--headless", "--nologo", "--nofirststartwizard",
            "--convert-to", "pdf", "--outdir", out_dir, pptx_path,
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
        if result.stderr:
            print(result.stderr.strip())
        generated = os.path.join(
            out_dir, os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf"
        )
        if generated != pdf_path and os.path.exists(generated):
            os.replace(generated, pdf_path)
        if not os.path.exists(pdf_path):
            raise RuntimeError(f"PDF not created: {pdf_path}")
        print(f"PDF exported via LibreOffice ({soffice})")
        return pdf_path

    try:
        from spire.presentation import Presentation as SpirePresentation, FileFormat

        pres = SpirePresentation()
        pres.LoadFromFile(pptx_path)
        pres.SaveToFile(pdf_path, FileFormat.PDF)
        pres.Dispose()
        if os.path.exists(pdf_path):
            print("WARNING: Spire fallback used - PDF may be limited to 10 pages.")
            return pdf_path
    except Exception as exc:
        raise RuntimeError(
            f"No PDF converter available (LibreOffice missing; Spire failed: {exc})"
        ) from exc
    raise RuntimeError(f"PDF not created: {pdf_path}")
