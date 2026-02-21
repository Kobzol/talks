from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import StateCounter, code, project, render_rustc_error


def compile_time_tests(slides: Slides, tips: StateCounter):
    @slides.slide()
    def compile_time_tests(slide: Box):
        tips.tip(slide, "Leverage compile-time tests")

    @slides.slide()
    def compile_time_tests_types(slide: Box):
        codebox = code(slide.box(), """
def find_item(
  items: ~#test1{Iterable[Item]},
  check: ~#test2{Callable[[Item], bool]}
) -> ~#test3{Item | None}:
    …
""", use_styles=True, return_codebox=True)

        positions = [
            (600, 200, "30%", -150),
            (1400, 200, "75%", 20),
            (1200, 700, "40%", 20),
        ]

        for (i, (x, y, pct, x_offset)) in zip(range(1, 4), positions):
            box = codebox.inline_box(f"#test{i}")
            top = y < 500
            target_y = box.y("0%") if top else box.y("100%")
            slide.fbox(show="2", x=0, y=0).line((
                (x, y + 50),
                (box.x(pct), target_y)
            ), stroke_width=6, end_arrow=Arrow(20))
            slide.box(x=x + x_offset, y=y, show="2").text("Test")
