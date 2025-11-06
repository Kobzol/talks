from elsie import Slides
from elsie.boxtree.box import Box
from elsie import TextStyle as T
from elsie.ext import unordered_list

from utils import topic


def maintenance(slides: Slides):
    @slides.slide()
    def maintenance(slide: Box):
        topic(slide.box(), "Maintenance", "broom.svg")

    @slides.slide()
    def github_activity(slide: Box):
        slide.box(width=1600).image("images/github-activity.png")
        # slide.box(y=box.y("30%"), show="1", width="100%", height="100%").rect(bg_color="white")
        # x = 1200
        # y = 500
        # slide.box(x=x, y=y, width=380, height=500, show="3").rect(color="red", stroke_width=4)
        # slide.box(x=x - 500, y=y, show="last+").text("Communication!", T(color="red"))

    @slides.slide()
    def curl(slide: Box):
        slide.box(width=1800).image("images/curl-maintenance.png")
        slide.box(x="[98%]", y="[98%]").text("Daniel Stenberg @ FrOSCon", T(size=40))

    @slides.slide()
    def maintenance_is_hard(slide: Box):
        slide.box(p_bottom=80).text("Maintaining stuff is hard!")

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("~300 repositories managed by the Rust Project", escape_char="#")
        lst.item(show="next+").text("Unglamorous (but crucial!) work")

    @slides.slide(bg_color="black")
    def rule_of_two(slide: Box):
        slide.set_style("red", T(size=80, color="red"))

        slide.box(y=100).text("Rule of two", T(color="white", size=80))

        box = slide.box(x="[20%]")
        box.box(width=1400).image("images/rule-of-two.jpg")

        x_text = 1350

        x1 = 900
        y1 = 600
        width1 = 350
        slide.line([
            (x1, y1),
            (x1 + width1, y1)
        ], color="red", stroke_width=10)
        slide.box(x=x_text, y=y1 - 50).text("Maintainer", "red")

        x2 = 750
        y2 = 780
        width2 = 550
        slide.line([
            (x2, y2),
            (x2 + width2, y2)
        ], color="red", stroke_width=10)
        slide.box(x=x_text, y=y2 - 50).text("Implementer", "red")

    @slides.slide()
    def funds(slide: Box):
        slide.box(width=1400).image("images/rust-foundation-fund.png")
        slide.box(width=1200, p_top=50).image("images/rustnl-fund.png")
