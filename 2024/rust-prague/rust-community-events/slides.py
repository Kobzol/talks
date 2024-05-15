from typing import Tuple, List

import elsie
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from utils import LOWER_OPACITY, generate_qr_code

"""
Links
- https://blog.rust-lang.org/2024/05/01/gsoc-2024-selected-projects.html
- https://this-week-in-rust.org/blog/2024/05/08/this-week-in-rust-546/
- https://makepad.dev/
- https://github.com/rust-lang/rfcs/pull/3621
- https://github.com/sophiajt/june
- https://project-robius.github.io/book/
- https://github.com/rust-lang/a-mir-formality
"""

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=60))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")


@slides.slide()
def intro(slide: Box):
    row = slide.box(horizontal=True, p_bottom=sh(60))
    row.box(width=sw(300), p_right=sw(80)).image("images/rust-logo.png")
    row.box(width=sw(300)).image("images/ferris-cz.png")
    slide.box(p_bottom=sh(40)).text("Rust Prague meetup #3", style=T(bold=True))
    slide.box(p_bottom=sh(40)).text("14. 5. 2024 @ MFF UK", style=T(size=40))


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100))
    line = row.box(padding=40, width=sw(100), height=sh(500))
    line.fbox().rect(bg_color="black")
    right = row.box()
    return (left, right)


@slides.slide()
def thanks(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(60)).text("Thanks!", T(bold=True))

    lst = unordered_list(content.box())
    lst.item().text("Martin Děcký")
    lst.item().text("Department of Distributed\nand Dependable Systems")
    content.box().image("images/d3s-logo.png")


@slides.slide()
def submit_a_talk(slide: Box):
    """
    Suggest, OOP in Rust.
    """
    content = slide.box()
    content.box(p_bottom=sh(60)).text("Propose your own talk!", T(bold=True))

    link = "https://docs.google.com/forms/d/e/1FAIpQLSdWFgyJ9Kp0bVRZ-1wqD8JTueKrcjh9sEAePouZo69MWOARLw/viewform"
    qrcode = generate_qr_code(link)
    slide.box().image(qrcode, image_type="png")


@slides.slide()
def recent_meetups(slide: Box):
    link = "https://youtu.be/YodMJMP2dfA?t=380"
    qr_code = generate_qr_code(link)
    slide.box(show="1", width=sw(1400)).image("images/meetup-ostrava-1.png")
    slide.box(x="[90%]", y="[10%]", width=sw(1000), show="1").image(qr_code, image_type="png")

    slide.box(x="[50%]", y="[50%]", show="next", width=sw(1400)).image("images/meetup-braiins-2.png")


@slides.slide()
def rustlangcz(slide: Box):
    content = slide.fbox()
    left, right = two_column_layout(content)
    left.box().text("~tt{rustlang.cz}")
    qr = generate_qr_code(
        "https://rustlang.cz",
        scale=22
    )
    right.image(qr, image_type="png")


@slides.slide()
def gsoc(slide: Box):
    content = slide.fbox()
    left, right = two_column_layout(content)
    left.image("images/rust-gsoc.png")
    qr = generate_qr_code(
        "https://blog.rust-lang.org/2024/05/01/gsoc-2024-selected-projects.html",
        scale=14
    )
    right.image(qr, image_type="png")


@slides.slide()
def conferences(slide: Box):
    slide.box().text("Rust community events", T(size=sw(80)))
    # Meetups: https://this-week-in-rust.org/blog/2024/05/08/this-week-in-rust-546/


@slides.slide()
def rustconf(slide: Box):
    slide.box(width=sw(1800)).image("images/rustconf.png")


@slides.slide()
def euro_rust(slide: Box):
    slide.box(width=sw(1800)).image("images/eurorust.png")


@slides.slide(bg_color="#780AE9")
def rust_nation(slide: Box):
    slide.box().image("images/rust-nation.png")


def image_slides(slides: SlideDeck, paths: List[str], width: int = 1600):
    for path in paths:
        slide = slides.new_slide()
        slide.box(width=sw(width)).image(f"images/{path}")


image_slides(slides, [
    "rustnation-jd.png",
    "rustnation-amanieu.png",
    "rustnation-jon.png",
    "rustnation-pietro.png",
    "rustnation-turborepo.png",
    "rustnation-lars.png",
])


@slides.slide()
def leads_summit(slide: Box):
    slide.box().image("images/leads-summit.png")


@slides.slide(bg_color="#E69601")
def rustnl(slide: Box):
    slide.box(width=sw(1600)).image("images/rustnl.png")


@slides.slide()
def rustnl_venue(slide: Box):
    slide.box(width=sw(1600)).image("images/rustnl-venue.png")


@slides.slide()
def rustnl_day1_morning(slide: Box):
    slide.box(p_bottom=sh(20)).text("Day 1 - morning")
    # https://youtu.be/XLefuzE-ABU?t=1682 - Makepad side screens
    slide.box(width=1000).image("images/rustnl-day1-morning.png")


@slides.slide()
def rust_in_linux_kernel(slide: Box):
    # https://github.com/Darksonn/rfcs/blob/derive-smart-pointer/text/3621-derive-smart-pointer.md
    slide.box(width=1400).image("images/rfl.png")


@slides.slide()
def mara(slide: Box):
    slide.box(width=1400).image("images/mara.png")


@slides.slide()
def rustnl_day1_afternoon(slide: Box):
    slide.box(p_bottom=sh(20)).text("Day 1 - afternoon")
    slide.box(width=800).image("images/rustnl-day1-afternoon.png")


@slides.slide()
def rustnl_industry_track(slide: Box):
    slide.box(p_bottom=sh(20)).text("Day 1 - Industry track")
    slide.box(p_bottom=sh(30)).text("~tt{https://2024.rustnl.org/industry/}", T(size=sw(40)))
    slide.box(width=800).image("images/rustnl-industry.png")


@slides.slide()
def ampere_track(slide: Box):
    slide.box().image("images/ampere.png")


# RustNL industry track State of Rust talk


@slides.slide()
def rustnl_day2_morning(slide: Box):
    # https://github.com/sophiajt/june
    slide.box(p_bottom=sh(20)).text("Day 2 - morning")
    slide.box(width=800).image("images/rustnl-day2-morning.png")


@slides.slide()
def folkert(slide: Box):
    slide.box(width=1000).image("images/folkert.png")


@slides.slide()
def rustnl_day2_afternoon(slide: Box):
    slide.box(p_bottom=sh(20)).text("Day 2 - afternoon")
    slide.box(width=800).image("images/rustnl-day2-afternoon.png")


@slides.slide()
def niko(slide: Box):
    slide.box(width=1400).image("images/niko.png")


@slides.slide()
def unconf(slide: Box):
    slide.box(width=1100).image("images/unconf.png")


@slides.slide()
def unconf_tldr(slide: Box):
    slide.box(p_bottom=sh(40)).text("TLDR")
    lst = unordered_list(slide.box())
    # https://github.com/rust-lang/rust/pull/125011
    lst.item().text("Embedded")
    embedded = lst.ul()
    embedded.item(show="next+").text("Smaller binaries")
    embedded.item(show="next+").text("~tt{static mut}")
    # https://github.com/davidlattimore/wild
    # https://www.coderemote.dev/blog/faster-rust-compiler-macro-expansion-caching/
    # Autoclone/Capture trait
    # Partial borrows
    # https://smallcultfollowing.com/babysteps//blog/2021/11/05/view-types/
    # https://hackmd.io/J5aGp1ptT46lqLmPVVOxzg?view
    lst.item(show="next+").text("UI")
    ui = lst.ul()
    ui.item(show="next+").text("Faster compiler")
    ui.item(show="next+").text("Auto cloning into closures")
    ui.item(show="next+").text("partial borrows")


@slides.slide()
def project_unconf(slide: Box):
    slide.box(p_bottom=sh(40)).text("Project unconf")
    lst = unordered_list(slide.box())
    # https://hackmd.io/@rustnl-2024-unconf/Bk5L8XqzC
    lst.item(show="next+").text("Edition system")
    # https://foundation.rust-lang.org/news/1m-microsoft-donation-to-fund-key-rust-foundation-project-priorities/
    lst.item(show="next+").text("How to reduce chaos (project management)")
    lst.item(show="next+").text("How to reduce burnout")
    lst.item(show="next+").text("Project goals")


@slides.slide()
def governance_talk(slide: Box):
    slide.box().text("Rust governance talk")
    slide.box().text("@ Rust Prague Meetup #1 2024", T(size=sw(40)))
    link = "https://youtu.be/d9_ymbFnzM4?t=1040"
    qrcode = generate_qr_code(link)
    slide.box().image(qrcode, image_type="png")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention", style=T(size=70, bold=True))

    slide.box().text("Slides were created with ~tt{github.com/spirali/elsie}",
                     style=T(size=40))


def ferris(slides: SlideDeck):
    count = sum(slide.steps() for slide in slides._slides)
    size = 80
    x_first = REFERENCE_WIDTH
    x_last = REFERENCE_WIDTH - (size * 1.05)
    y = int(REFERENCE_HEIGHT * 0.02)
    x_diff = abs(x_first - x_last)

    total_steps = 0
    for i, slide in enumerate(slides._slides):
        steps = slide.steps()
        for step in range(steps):
            progress = (total_steps + step) / count
            x = x_first - progress * x_diff
            slide.box().box(show=step + 1, x=sw(x), y=sh(y), width=sw(size), height=sh(size)).image(
                "images/ferris.svg")
        total_steps += steps


if PRODUCTION_BUILD:
    ferris(slides)

slides.render("slides.pdf")
