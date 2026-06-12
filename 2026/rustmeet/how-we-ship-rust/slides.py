import json
import math
import random
import subprocess
from typing import List, Tuple

import elsie
from elsie import Arrow, SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from ci import ci
from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from context import context
from dist import dist
from implementation import implementation
from pr_experience import pr_experience
from proposal import proposal
from tests import tests
from utils import BUILD_ICON, CI_ICON, COLOR_ORANGE, DESIGN_ICON, LOWER_OPACITY, \
    MIGRATION_COUNTERS, RELEASE_ICON, REVIEW_ICON, \
    TEST_ICON, \
    generate_qr_code, \
    iterate_grid

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=60))
slides.update_style("code", T(size=50))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")
slides.set_style("small", TextStyle(size=50), base="default")


@slides.slide(bg_color="#EFC9BD")
def intro(slide: Box):
    slide.box(p_bottom=sh(60), width=sw(300)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("How we ship the Rust toolchain", style=T(size=70, bold=True))


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=60))

    content = slide.box()

    content.box(p_bottom=200).text("Jakub Beránek", T(align="left", bold=True))
    lst = unordered_list(content.box())
    lst.item().text("Open source contributor @ Rust Project")
    lst2 = lst.ul()
    lst2.item().text("Infrastructure, Compiler, Leadership Council", "small")
    lst2.item().text("Sovereign Tech Fellow", "small")
    lst.item().text("Teacher @ VSB-TUO (Czech Republic university)")

    gh = content.box(horizontal=True, p_top=200)
    gh.box(width=100).image("images/github-logo.png")
    gh.box(p_left=40).text("github.com/kobzol", style=T(bold=True))


# @slides.slide()
# def teams(slide: Box):
#     content = slide.box()
#     height = 1000
#
#     # Link: https://www.rust-lang.org/governance/teams/infra
#     # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
#     # Link: https://www.rust-lang.org/governance/teams/compiler#Binary%20size%20working%20group
#     # Link: https://www.rust-lang.org/governance/teams/compiler#Parallel%20rustc%20working%20group
#     for (index, image) in enumerate((
#             "wg-perf",
#             "team-infra",
#             "leadership-council"
#     )):
#         content.box(
#             show=str(index + 1),
#             x="[50%]",
#             y="[50%]",
#             height=sh(height - (30 * (index - 1)))
#         ).image(f"images/{image}.png")

@slides.slide(bg_color="black")
def rust_project(slide: Box):
    slide.box().image("images/allhands-celebration.jpg")


context(slides)


def talk_map(slides: SlideDeck, target: int = 0):
    slide = slides.new_slide()
    slide.box(y=100).text("Let's ship a new feature to Rust users!", T(size=80))

    steps = [
        (DESIGN_ICON, "Design"),
        (BUILD_ICON, "Implementation"),
        (TEST_ICON, "Testing"),
        (REVIEW_ICON, "Pull request"),
        (CI_ICON, "CI"),
        (RELEASE_ICON, "Release"),
    ]

    width = 500
    height = 300
    start_pos = (100, 300)
    positions = list(
        iterate_grid(rows=2, cols=3, width=width, height=height, p_vertical=50, p_horizontal=80))
    positions = [(start_pos[0] + positions[i][1], start_pos[1] + positions[i][0]) for i in
                 (0, 3, 4, 1, 2, 5)]

    boxes = []
    for (index, ((icon, name), (x, y))) in enumerate(zip(steps, positions)):
        active = index == target
        shown = index <= target or index == len(steps) - 1
        color = "black"
        if not shown:
            icon = "red-question-mark.svg"
            color = "white"
        box = slide.box(width=width, height=height, x=x, y=y)
        image_box = box.box(width=100).image(f"images/{icon}")
        textbox = box.box().text(name, T(size=50, color=color, bold=active))
        if active:
            box.box(width=max(width * 0.75, textbox._box.layout._width.compute(1, 1) * 1.1),
                    height=height * 0.7, x="[50%]", y="[50%]").rect(rx=30, ry=30, color="black",
                                                                    stroke_width=6)
        boxes.append(image_box)

    arrow = Arrow(size=30)
    for index in range(len(boxes) - 1):
        start = boxes[index]
        end = boxes[index + 1]

        dir = {
            0: "down",
            1: "right",
            2: "up",
            3: "right",
        }
        dir = dir[index % 4]
        if dir == "down":
            start = start.p("50%", "200%")
            end = (end.x("50%"), end.y("0").add(-50))
        elif dir == "right":
            start = start.p("270%", "50%")
            end = (end.x("0").add(-150), end.y("50%"))
        elif dir == "up":
            start = (start.x("50%"), start.y("0").add(-50))
            end = end.p("50%", "200%")
        else:
            assert False

        slide.box().line((
            start,
            end
        ), color="black", stroke_width=10, end_arrow=arrow)

    if target == 6:
        row = slide.box(horizontal=True, y="[95%]")
        for _ in range(3):
            row.box().image("images/tada.png")


# for i in range(6):
#     talk_map(slides, target=i)

talk_map(slides, target=0)
proposal(slides)

talk_map(slides, target=1)
implementation(slides)

talk_map(slides, target=2)
tests(slides)

talk_map(slides, target=3)
pr_experience(slides)

talk_map(slides, target=4)
ci(slides)

talk_map(slides, target=5)
dist(slides)

talk_map(slides, target=6)


@slides.slide()
def recap(slide: Box):
    rng = random.Random()
    rng.seed(42)

    tools = [
        "rfcbot",
        "josh-sync",
        "bootstrap",
        "compiletest",
        "tidy",
        "triagebot",
        "rust-log-analyzer",
        "rustc-perf",
        "crater",
        "citool",
        "bors",
        "team",
        "thanks",
        "opt-dist",
        "rustup",
        "promote-release"
    ]

    centers = []

    def is_close(point: Tuple[int, int], offset: int) -> bool:
        (x1, y1) = point
        for (x2, y2) in centers:
            if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < offset:
                return True
        return False

    padding = 120
    for tool in tools:
        while True:
            x = rng.randint(padding, WIDTH - 300)
            y = rng.randint(padding, HEIGHT - padding - 40)
            rotation = rng.randint(-30, 30)
            pos = (x, y)

            if not is_close(pos, 270):
                break
        slide.box(x=x, y=y, show="1+" if tool == tools[0] else "next+").text(tool,
                                                                             rotation=rotation)
        centers.append(pos)


@slides.slide()
def migration_counter(slide: Box):
    slide.box(p_bottom=40).text("Rewrite counter", T(size=80))

    map = {
        ("make", "rust"): "Makefile => Rust",
        ("bash", "python"): "Bash => Python",
        ("python", "rust"): "Python => Rust",
    }

    lst = unordered_list(slide.box(p_bottom=80))
    items = sorted(MIGRATION_COUNTERS.items(), key=lambda v: list(map).index(v[0]))
    for (languages, count) in items:
        text = map[languages]
        row = lst.item(show="next+").box(horizontal=True)
        row.box(width=500).text(f"{text}: ")
        row.box(width=100).text(f"{count}x", T(align="right"))

    row = slide.box(horizontal=True, show="next+")
    row.box().text("Conclusion: write your tooling in", T(size=80))
    row.box(width=30)
    row.box(width=120).image("images/rust-logo.png")


@slides.slide()
def rust_infra_team(slide: Box):
    """
    t-infra: 8 people, 3.5 FTE
    t-docs-rs: 2 people, 1 FTE
    t-release: 5 people (3 unique), 1 FTE
    t-crates-io: 6 people, 2.5 FTE

    Some of them have overlap (also with many other teams), many are volunteers or not very active.

    I have never worked in a big company, but let me assure you, their infra team is much larger
    than six people.
    The people are volunteers, and not on-call, and we need automation for that.
    """
    slide.box().image("images/team-infra.png")
    slide.box(width=1400, show="next+", x="[50%]", y="[50%]").image("images/team-bootstrap.png")
    slide.box(width=1400, show="next+", x="[50%]", y="[50%]").image("images/team-bors.png")
    slide.box(width=1400, show="next+", x="[50%]", y="[50%]").image("images/team-triagebot.png")
    slide.box(show="next+", p_top=60).text(
        "~2-3 people working full-time on internal infra & tooling", escape_char="#")


@slides.slide()
def rfmf(slide: Box):
    slide.box().text("Rust Foundation Maintainer Fund", T(size=80))
    link = "https://github.com/sponsors/rustfoundation"

    qr = generate_qr_code(link, scale=18)
    slide.box().image(qr, image_type="png")

    slide.box().text(f"~tt{{{link}}}")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention!", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:")
    qr = generate_qr_code(
        "https://github.com/kobzol/talks/blob/main/2026/rustmeet/how-we-ship-rust",
        scale=14)
    slide.box().image(qr, image_type="png")

    slide.box(p_bottom=20).text("Blog: ~tt{kobzol.github.io}")

    slide.box().text("Slides were programmed using ~tt{github.com/spirali/elsie}",
                     style=T(size=40))
    if PRODUCTION_BUILD:
        output = subprocess.check_output(["tokei", "--output=json", "."])
        output = json.loads(output)
        lines = int(output["Python"]["code"])
        slide.box().text(f"({lines} lines of Python)",
                         style=T(size=40))
    slide.box(p_top=20).text("Several emojis were used from the Noto Emoji pack", style=T(size=36))


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


def page_numbering(slides: List[Box]):
    slide_count = len(slides)

    numbering_start = 2
    numbering_end = slide_count - 1

    width = 135
    height = 60
    margin = 20

    for i, slide in enumerate(slides):
        if numbering_start <= (i + 1) <= numbering_end:
            box = slide.box(x=sw(REFERENCE_WIDTH - width - margin),
                            y=sh(REFERENCE_HEIGHT - height - margin),
                            width=sw(width),
                            height=sh(height)).rect(
                bg_color=COLOR_ORANGE, rx=5, ry=5
            )
            box.fbox(padding=5).text(f"{i + 1}/{slide_count}",
                                     style=TextStyle(color="white", size=sw(40), align="right"))


if PRODUCTION_BUILD:
    ferris(slides)
    print_stats(slides, minutes=60)

# if PRODUCTION_BUILD:
#     slides.render("slides.pdf", slide_postprocessing=page_numbering)
# else:
slides.render("slides.pdf")
