from __future__ import annotations

import io
from typing import Any, Optional

from PIL import Image

__all__ = ["what"]


def _format_or_none(image: Image.Image) -> Optional[str]:
    fmt = (image.format or "").lower().strip()
    return fmt or None


def what(file: Any, h: Any = None) -> Optional[str]:
    """
    Minimal replacement for stdlib imghdr.what (removed in Python 3.13).
    Uses Pillow to detect image format from bytes or file-like objects.
    """
    try:
        if h is not None:
            data = h if isinstance(h, (bytes, bytearray)) else str(h).encode()
            with Image.open(io.BytesIO(data)) as image:
                return _format_or_none(image)

        if isinstance(file, (str, bytes, bytearray)):
            with Image.open(file) as image:
                return _format_or_none(image)

        # File-like object
        pos = file.tell() if hasattr(file, "tell") else None
        data = file.read()
        if pos is not None and hasattr(file, "seek"):
            file.seek(pos)
        with Image.open(io.BytesIO(data)) as image:
            return _format_or_none(image)
    except Exception:
        return None
