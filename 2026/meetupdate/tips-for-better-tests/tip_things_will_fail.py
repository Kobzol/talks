from typing import Optional

from elsie import Slides
from elsie.boxtree.box import Box

from utils import StateCounter, source


def things_will_fail(slides: Slides, tips: StateCounter):
    @slides.slide()
    def things_will_fail(slide: Box):
        """
        Embrace it.
        """
        box = tips.tip(slide, "Things will still fail somehow")
        slide.box(show="next+", y=box.y("100%").add(40)).text("…so make peace with it")

    @slides.slide()
    def rustc_perf_commands(slide: Box):
        slide.box(width=1800).image("images/rustc-perf-comment-1.png")
        slide.box(width=1800, show="next+", p_top=40).image("images/rustc-perf-comment-2.png")

    @slides.slide()
    def rustc_perf_pr(slide: Box):
        slide.box(width=1800).image("images/rustc-perf-pr.png")

    @slides.slide()
    def rustc_perf_bug(slide: Box):
        def img(show: int, width: Optional[int] = None, height: Optional[int] = None):
            slide.box(width=width, height=height, x="[50%]", y="[50%]", show=f"{show}").image(
                f"images/rustc-perf-comment-{show + 2}.png")

        img(1, 1800)
        img(2, 1800)
        img(3,height=1000)
        img(4, 1800)

    @slides.slide()
    def gemini_bug(slide: Box):
        slide.box(width=1000).image("images/gemini-loop.png")

        source(slide, "https://github.com/google-gemini/gemini-cli/issues/16750")
