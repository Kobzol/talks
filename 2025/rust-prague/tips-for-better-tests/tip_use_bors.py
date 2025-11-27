from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import StateCounter, quotation


def use_bors(slides: Slides, tips: StateCounter):
    @slides.slide()
    def no_rocket_science(slide: Box):
        quotation(slide.box(), """
~bold{The Not Rocket Science Rule Of Software Engineering:}
Automatically maintain a repository of code that always passes all the tests.
""", "Graydon Hoare (creator of Rust)", size=50)

    @slides.slide()
    def pr_green_red_tests(slide: Box):
        dim = 135

        def circle(x: int, y: int, text: str, show: str = "1+", color="black") -> Box:
            pr = slide.box(x=x, y=y, width=dim, height=dim, show=show)
            pr.ellipse(color=color, bg_color="white", stroke_width=6)
            pr.text(text, T(size=40))
            return pr

        def arrow(src, dst, show: str = "1+"):
            slide.fbox(x=0, y=0, show=show).line((
                (src.x("50%"), src.y("0%")),
                (dst.x("50%"), dst.y("100%")),
            ), color="black", stroke_width=4)

        c_x = 800
        base_y = 800
        x_offset = 150
        y_offset = 200
        main1 = circle(c_x, base_y, "main1")
        circle(c_x - x_offset, base_y - y_offset, "pr1", show="1")
        pr1 = circle(c_x - x_offset, base_y - y_offset, "pr1", show="2", color="green")
        arrow(main1, pr1, show="1-2")
        circle(c_x + x_offset, base_y - y_offset, "pr2", show="1")
        pr2 = circle(c_x + x_offset, base_y - y_offset, "pr2", show="2-3", color="green")
        arrow(main1, pr2, show="1-3")

        main2 = circle(c_x, base_y - int(y_offset * 1.5), "main2", show="3+", color="green")
        arrow(main1, main2, show="3+")

        main3 = circle(c_x, base_y - y_offset * 3, "main3", show="4+", color="red")
        arrow(main2, main3, show="4+")

    @slides.slide()
    def use_merge_queues(slide: Box):
        tips.tip(slide, "Use merge queues/trains")
