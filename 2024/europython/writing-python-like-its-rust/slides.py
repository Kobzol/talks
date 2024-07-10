import datetime
import math
from typing import Tuple

import elsie
from elsie import SlideDeck, TextStyle, Arrow
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from soundness import soundness
from type_hints import type_hints
from utils import LOWER_OPACITY, dimmed_list_item, \
    generate_qr_code, with_bg, create_grid, code, INVISIBLE_SPACE

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=sw(72)))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.update_style("code", T(size=sw(80)))
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")

IMG_BG_COLOR = "#DDDDDD"


@slides.slide()
def intro(slide: Box):
    """
    Based on my blog post, 60k visitors.
    """
    slide.box(width=sw(1600), show="1-2").image("images/blog-post.png")
    slide.box(x=0, y=sh(100), width="100%", height=sh(300), show="1").rect(bg_color="white")
    slide.box(x=0, y=sh(600), width="100%", height=sh(300), show="1").rect(bg_color="white")


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100))
    line = row.box(padding=40, width=sw(100), height=sh(500))
    line.fbox().rect(bg_color="black")
    right = row.box()
    return (left, right)


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=55))

    content = slide.box(x=sw(80))

    content.fbox(p_bottom=sh(30)).text("Jakub Beránek", T(align="left", size=sw(80), bold=True))
    gh = content.box(x=0, horizontal=True, p_bottom=sh(5))
    gh.box(width=sw(50)).image("images/github-logo.png")
    gh.box(p_left=sw(20)).text("github.com/kobzol", style=T(size=sw(50)))
    email = content.box(x=0, horizontal=True, p_bottom=sh(40))
    email.box(width=sw(50)).text("@", style=T(size=sw(70), bold=True))
    email.box(p_left=sw(20)).text("jakub@berankovi.net", style=T(size=sw(50)))

    content.box(x=0, width=sw(600), height=sw(2)).rect(bg_color="black")

    deadline = datetime.datetime(year=2024, month=8, day=31)
    presentation_day = datetime.datetime(year=2024, month=7, day=10)
    days_left = (deadline - presentation_day).days

    lst = unordered_list(content.box(x=0, p_top=sh(40)))
    dimmed_list_item(lst, f"PhD student ({days_left} days left), teacher @ VSB-TUO university", show=2)
    dimmed_list_item(lst, "Researcher @ IT4Innovations HPC center", show=3)
    lst.item(show="last+").text("Rust Project open-source contributor")
    lst2 = lst.ul()
    lst2.item(show="next+").text("Compiler performance")
    lst2.item(show="next+").text("Infrastructure")

    # Link: https://www.rust-lang.org/governance/teams/infra
    # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
    offset_x = sw(820)
    height = sh(940)
    with_bg(
        slide.box(x=offset_x, y=sh(50), width=sw(1090), height=height, show="5"), bg_color=IMG_BG_COLOR
    ).image("images/wg-perf.png")
    with_bg(
        slide.box(x=offset_x, y=sh(50), width=sw(1090), height=height, show="6"), bg_color=IMG_BG_COLOR
    ).image("images/team-infra.png")


def logo(slide: Box, image: str):
    slide.box(x=sw(100), y=sh(100), width=sw(300)).image(image)


@slides.slide()
def how_i_used_to_write_python(slide: Box):
    """
    Some of you might think - YEAAAH!
    Duh/obviously.
    """
    logo(slide, "images/python-logo.png")
    slide.box(show="next+").text("How I used to write Python:")
    lst = unordered_list(slide.box(show="next+", p_top=sh(40)))
    dimmed_list_item(lst, "No type hints", show=3)
    dimmed_list_item(lst, "Dictionaries everywhere", show=4)
    dimmed_list_item(lst, '"Stringly typed"', show=5)
    lst.item(show="last+").text("Monkey patching")

    # quotation(slide.box(x="[50%]", y="[50%]"), "Duh", "Some Python programmer (probably)")


@slides.slide()
def python_symptoms(slide: Box):
    """
    Skill issue
    """
    logo(slide, "images/python-logo.png")
    slide.box().text("Symptoms:")
    lst = unordered_list(slide.box(p_top=sh(40)))
    dimmed_list_item(lst, "Easy to cause bugs", show=2)
    dimmed_list_item(lst, "(Too) many runtime crashes", show=3)
    dimmed_list_item(lst, "Hard to understand", show=4)
    lst.item(show="last+").text("Difficult to refactor")

    radius = 20
    rotation = -20
    box = slide.box(show="next+", x="[50%]", y="[50%]")
    box.rect(rotation=rotation, bg_color="red", color="black", stroke_width=sw(10), rx=radius, ry=radius)
    box.box(padding=sw(20)).text("SKILL ISSUE?", style=T(color="white"), rotation=rotation)


@slides.slide()
def rust(slide: Box):
    logo(slide, "images/rust-logo.png")
    slide.box(show="next+").text("My experience with Rust:")
    lst = unordered_list(slide.box(show="next+", p_top=sh(40)))
    item_0 = dimmed_list_item(lst, "<compiling>", show=3)
    item_1 = dimmed_list_item(lst, "<compiling>", show=4)
    item_2 = dimmed_list_item(lst, "<fighting the compiler>", show=5)
    lst.item(show="last+").text("~bold{It just works!}")

    # wrapper = slide.box(show="next+", width="fill")
    # offset_x_start = item_0.x("100%").add(sw(400))
    # offset_x_end = offset_x_start.add(sw(200))
    # end_y = item_2.y("50%").add(sh(150))
    # wrapper.line([
    #     (offset_x_start, item_1.y("50%")),
    #     (offset_x_end, item_1.y("50%")),
    #     (offset_x_end, end_y),
    # ], color="red", stroke_width=sw(10), end_arrow=Arrow(size=sw(30)))
    # wrapper.box(x=sw(1000), y=sh(50)).text("Low-latency bug detection", T(color="red"))


@slides.slide()
def why_to_write_python_like_rust(slide: Box):
    slide.box(p_bottom=sh(60)).text("Why write Python like Rust (and how?)", T(size=sw(80)))
    slide.box(width=sw(900), show="next+").image("images/python-rust-meme-2.jpeg")


@slides.slide()
def disclaimer(slide: Box):
    slide.box(p_bottom=sh(40)).text("(disclaimer)", style=T(size=sw(90)))
    slide.box().text("These are just my opinions :)", T(size=sw(60)))


@slides.slide()
def step_1_use_types(slide: Box):
    slide.update_style("default", T(size=sw(80)))
    slide.box(p_bottom=sh(40)).text("Step 1", T(size=sw(100), bold=True))
    slide.box().text("Type hints, type hints, type hints")


type_hints(slides)


@slides.slide()
def step_2_dataclasses(slide: Box):
    slide.update_style("default", T(size=sw(80)))
    slide.box(p_bottom=sh(40)).text("Step 2", T(bold=True))
    slide.box().text("Use ~emph{dataclasses}")


@slides.slide()
def dataclasses(slide: Box):
    slide.update_style("code", T(size=sw(40)))
    slide.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")

    grid = create_grid(slide)

    width = sw(920)

    def show_and_fade(box: Box, code_contents: str):
        wrapper = box.box()
        code(wrapper.box(show=str(box.current_fragment())), code_contents, width=width)
        code(wrapper.overlay(show="next+"), code_contents, code_style="code_muted", width=width)

    show_and_fade(grid.top_left.box(y="[90%]"), f"""
def get_person() -> Tuple[str, int]:
  ...
{INVISIBLE_SPACE}
{INVISIBLE_SPACE}
""")
    show_and_fade(grid.top_right.box(show="last+", y="[90%]"), f"""
def get_person() -> Dict[str, Any]:
  ...
{INVISIBLE_SPACE}
{INVISIBLE_SPACE}
""")
    code(grid.bottom_left.box(show="last+", y="[10%]"), f"""
def get_person() -> Person:
  ...
{INVISIBLE_SPACE}
{INVISIBLE_SPACE}
""", width=width)
    code(grid.bottom_right.box(show="next+", y="[10%]"), """
@dataclass
class Person:
  name: str
  age: int
""", width=width)


@slides.slide()
def step_3_soundness(slide: Box):
    slide.update_style("default", T(size=sw(80)))
    slide.box(p_bottom=sh(40)).text("Step 3", T(bold=True))
    slide.box().text("Embrace ~emph{soundness}")


soundness(slides)


@slides.slide()
def summary(slide: Box):
    slide.update_style("default", T(size=sw(80)))
    slide.box(p_bottom=sh(80)).text("Summary", T(size=sw(100), bold=True))
    lst = unordered_list(slide.box())
    lst.item(show="next+").text("Step 1: Use type hints")
    # lst2 = lst.ul()
    # lst2.item(show="next+").text("Type-checking in CI", T(size=sw(60)))
    lst.item(show="next+").text("Step 2: Use dataclasses")
    lst.item(show="next+").text("Step 3: Make code hard to misuse")
    lst.item(show="next+").text("Step 4: ???")
    lst.item(show="next+").text("Step 5: Profit!")


@slides.slide()
def why_not_just_use_rust(slide: Box):
    """
    Easy to prototype, useful libraries (data science, machine learning).
    From my experience, using dictionaries and string typing does not save time
    """
    slide.box().text("Why not just use Rust?", T(size=sw(100)))


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention!", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:", T(size=sw(60)))
    qr = generate_qr_code("https://github.com/kobzol/talks/blob/main/2024/europython/writing-python-like-its-rust/",
                          scale=16)
    slide.box().image(qr, image_type="png")

    slide.box(p_bottom=sh(40)).text("Make slides with Python using ~tt{github.com/spirali/nelsie}",
                     style=T(size=60))

    slide.fbox(p_right=sw(40)).text("Several used icons are from the Twemoji icon pack", T(size=sw(40), align="right"))


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


def print_stats(slides: SlideDeck, minutes: int):
    step_count = sum(slide.steps() for slide in slides._slides)
    slide_count = len(slides._slides)

    seconds = minutes * 60
    print(f"{slide_count} slides, {math.floor(seconds / slide_count)}s per slide")
    print(f"{step_count} steps, {math.floor(seconds / step_count)}s per step")


if PRODUCTION_BUILD:
    ferris(slides)
    print_stats(slides, minutes=30)

slides.render("slides.pdf")
