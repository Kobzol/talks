from typing import Optional

from elsie import Slides


def image(slides: Slides, path: str, height: Optional[str] = None, width: Optional[str] = None):
    slide = slides.new_slide(name=path)

    assert height is None or width is None

    args = {}
    if width is not None:
        args["width"] = width
    elif height is not None:
        args["height"] = height
    else:
        args["height"] = "80%"
    box = slide.fbox(**args)
    box.image(path)
