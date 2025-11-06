from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import dimmed_list_item


def open_source(slides: Slides):
    @slides.slide()
    def xkcd(slide: Box):
        slide.box().image("images/xkcd-2347.png")
        slide.box(x="[98%]", y="[98%]").text("xkcd #2347", T(size=40))

    @slides.slide()
    def screwdriver_analogy(slide: Box):
        slide.box(y=150).text("Open-source maintenance")

        arrow = Arrow(size=20)

        images = [
            "screwdriver",
            # "factory",
            "wheel",
            "ambulance",
            "doctor"
        ]
        boxes = []
        row = slide.box(horizontal=True, x=250)
        for (step, image) in enumerate(images, start=1):
            box = row.box(show=f"{step}+", width=128).image(f"images/{image}.svg")
            arrow_box = row.box(width=300)
            if image != images[-1]:
                slide.box(show=f"{step + 1}+").line([
                    (arrow_box.x("20%"), arrow_box.y("50%")),
                    (arrow_box.x("80%"), arrow_box.y("50%")),
                ], color="black", stroke_width=8, end_arrow=arrow)
            boxes.append(box)

        offset = 50
        slide.box(x=boxes[0].x("30%"), y=boxes[0].y("100%").add(offset), show="next+").text("+1%")
        slide.box(x=boxes[3].x(0).add(-20), y=boxes[3].y("100%").add(offset), show="next+").text("+1000%")


    @slides.slide()
    def open_source(slide: Box):
        slide.box().text("Do you depend on open-source?")
        slide.box(p_top=40, show="next+").text("(yes, you do :-) )", "small")

        slide.box(show="next+", p_top=100).text("Try to give back!")

    @slides.slide()
    def contributions(slide: Box):
        slide.box(y=50).text("Every contribution counts")

        items = [
            "Create an issue",
            "Upstream fixes/features",
            "Improve documentation",
            "Discuss things, write blog posts",
            "Give credit",
            "Be kind!",
            "Sponsor maintainers"
        ]
        lst = unordered_list(slide.box())
        for (step, item) in enumerate(items, start=2):
            dimmed_list_item(lst, item, show=step, last=item == items[-1])

    @slides.slide()
    def thanks_dev(slide: Box):
        slide.box().image("images/thanks.dev.png")

    @slides.slide()
    def github_sponsors(slide: Box):
        slide.box(width=1200).image("images/github-sponsors.png")
