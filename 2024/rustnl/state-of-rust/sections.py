import contextlib
from typing import Optional

from elsie import SlideDeck, TextStyle as T
from elsie.boxtree.box import Box

from config import sh, sw
from utils import COLOR_ORANGE


class SectionManager:
    def __init__(self):
        self.sections = {}

    @contextlib.contextmanager
    def start_section(self, slides: SlideDeck, name: str):
        start = len(slides._slides)
        yield
        end = len(slides._slides)
        count = end - start

        assert name not in self.sections
        self.sections[name] = (start, count)

    def get_section(self, index: int) -> Optional[str]:
        for (name, (start, count)) in self.sections.items():
            if start <= index < start + count:
                return name
        return None

    def apply(self, slides: SlideDeck):
        for (index, slide) in enumerate(slides._slides):
            section = self.get_section(index)
            if section is not None:
                box = slide.box()
                offset_x = 50
                offset_y = 40
                box: Box = box.box(
                    x=-sw(offset_x),
                    y=-sh(offset_y),
                    width=sw(300),
                    height=sh(140),
                    z_level=-1
                )
                radius = 10
                box.rect(bg_color=COLOR_ORANGE, rx=radius, ry=radius)
                inner_box = box.fbox(p_left=sw(offset_x + 20), p_top=sh(offset_y), p_right=sw(20))
                inner_box.text(section, T(color="white", size=sw(70), align="right"))
