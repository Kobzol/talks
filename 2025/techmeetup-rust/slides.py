import math
from typing import List

import elsie
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from deployment import deployment
from development import development
from governance import governance
from maintenance import maintenance
from open_source import open_source
from utils import COLOR_ORANGE, LOWER_OPACITY, generate_qr_code, topic

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=60))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")
slides.set_style("small", TextStyle(size=50), base="default")


@slides.slide()
def intro(slide: Box):
    slide.box(p_bottom=sh(60), width=sw(300)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("How Rust does open-source", style=T(size=70, bold=True))


@slides.slide()
def techmeetup_2023(slide: Box):
    slide.box(width="100%").image("images/techmeetup-2023.png")


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=60))

    content = slide.box()

    content.box(p_bottom=200).text("Kuba Beránek", T(align="left", bold=True))
    lst = unordered_list(content.box())
    lst.item().text("Teaching @ VSB-TUO")
    lst.item().text("Research @ IT4Innovations")
    lst.item().text("Open-source contributor @ Rust Project")

    gh = content.box(horizontal=True, p_top=200)
    gh.box(width=100).image("images/github-logo.png")
    gh.box(p_left=40).text("github.com/kobzol", style=T(bold=True))


@slides.slide()
def teams(slide: Box):
    content = slide.box()
    height = 1000

    # Link: https://www.rust-lang.org/governance/teams/infra
    # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Binary%20size%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Parallel%20rustc%20working%20group
    for (index, image) in enumerate((
            "wg-perf",
            "team-infra",
            "leadership-council"
    )):
        content.box(
            show=str(index + 1),
            x="[50%]",
            y="[50%]",
            height=sh(height - (30 * (index - 1)))
        ).image(f"images/{image}.png")


@slides.slide()
def talk_contents(slide: Box):
    slide.update_style("default", T(size=66))

    row = slide.box(horizontal=True, y="[50%]")
    left = row.box(p_right=100)
    left.box(width=300).image("images/rust-logo.png")

    main = row.box()
    topic(main, "Governance", "lawyer.svg")
    topic(main, "Development", "hammer_and_spanner.svg", show="next+")
    topic(main, "Deployment", "package.svg", show="next+")
    topic(main, "Maintenance", "broom.svg", show="next+")

    aux = row.box(p_left=100)
    topic(aux, "Open-source", "heart.svg", show="next+")
    topic(aux, "Automation", "robot.svg", show="next+")

governance(slides)
development(slides)
deployment(slides)
maintenance(slides)
open_source(slides)

@slides.slide()
def open_source(slide: Box):
    row = slide.box(horizontal=True)
    row.box(width=300, p_right=50).image("images/rust-logo.png")
    row.box(p_right=50).text("is open-source =", T(size=100))
    row.box(width=150).image("images/heart.svg")

    slide.box(show="next+", p_top=50).text("~link{rust-lang.zulipchat.com}")
    slide.box(show="next+", p_top=50).text("~link{rustlang.cz}")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention!", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:")
    qr = generate_qr_code("https://github.com/kobzol/talks/blob/main/2025/techmeetup-rust/",
                          scale=14)
    slide.box().image(qr, image_type="png")

    slide.box().text("Slides were programmed using ~tt{github.com/spirali/elsie}",
                     style=T(size=40))
    slide.box(p_top=40).text("Several emojis were used from the Noto Emoji pack", style=T(size=36))


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
    print_stats(slides, minutes=40)

# if PRODUCTION_BUILD:
#     slides.render("slides.pdf", slide_postprocessing=page_numbering)
# else:
slides.render("slides.pdf")
