import json
import math
import os
import subprocess
from pathlib import Path
from typing import List, Optional

import elsie
from PIL import Image
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from bors import bors
from bors_plan import bors_plan
from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from history import history
from homu import homu
from porting_process import porting_process
from utils import COLOR_ORANGE, GITHUB_BG_COLOR, LOWER_OPACITY, generate_qr_code, iterate_grid

PRODUCTION_BUILD = True

BG_COLOR = "#FFA700"

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=60))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.update_style("code", T(size=50))
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")
slides.set_style("small", TextStyle(size=50), base="default")


fps_box: Optional[Box] = None


@slides.slide(bg_color=BG_COLOR)
def intro(slide: Box):
    global fps_box

    slide.box(p_bottom=sh(60), width=sw(300)).image("images/bors.png")
    slide.box(p_bottom=sh(40)).text(
        "Rewriting bors: how hard can it be?",
        style=T(size=70, bold=True)
    )

    fps_box = slide.box(x="[99%]", y="[99%]")


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=60))

    content = slide.box()

    content.box(p_bottom=200).text("Jakub Beránek", T(align="left", bold=True))
    lst = unordered_list(content.box())
    lst.item().text("Open source contributor @ Rust Project")
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

history(slides)
homu(slides)
bors_plan(slides)
bors(slides)
porting_process(slides)


@slides.slide(bg_color=GITHUB_BG_COLOR)
def bors_gsoc_contributors(slide: Box):
    slide.update_style("default", T(color="white"))

    row = slide.box(horizontal=True)
    row.box(p_right=500).text("Sakibul Islam")
    row.box().text("Võ Hoàng Long")
    slide.box(width=1800).image("images/bors-gsoc-contributors.png")


@slides.slide()
def rust_infra_team(slide: Box):
    slide.box(width=1300).image("images/team-infra.png")


def get_bors_contributors_image_path() -> str:
    width = 90
    height = 90
    rows = 9
    cols = 12
    padding = 5
    images = sorted([f"contributors/avatars/{file}" for file in os.listdir("contributors/avatars")],
                    key=lambda v: v.lower())
    assert rows * cols == len(images)

    def generate(path: Path):
        img = Image.new("RGBA", ((width + padding) * cols, (height + padding) * rows), "WHITE")
        white_bg = Image.new("RGBA", (width, height), "WHITE")
        for (image, (row, col)) in zip(images,
                                       iterate_grid(rows, cols, width, height, p_horizontal=padding,
                                                    p_vertical=padding)):
            avatar = Image.open(image).resize((width, height)).convert("RGBA")
            avatar = Image.alpha_composite(white_bg, avatar)
            img.paste(avatar, (col, row))
        img.convert("RGBA").save(path)

    key = Path(f"images/bors-contributors.png")
    if not key.is_file():
        generate(key)

    return str(key)


@slides.slide()
def bors_contributors(slide: Box):
    row = slide.box(horizontal=True, p_bottom=50)
    row.box(p_right=20).text("bors contributors")
    row.box(width=100).image("images/heart.svg")

    slide.box().image(get_bors_contributors_image_path())


@slides.slide()
def bors_thanks(slide: Box):
    slide.box(width=1800).image("images/bors-thanks.png")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention!", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:")
    qr = generate_qr_code("https://github.com/Kobzol/talks/blob/main/2026/rustweek/rewriting-bors/slides.pdf",
                          scale=14)
    slide.box().image(qr, image_type="png")

    slide.box().text("Slides were programmed using ~tt{github.com/spirali/elsie}",
                     style=T(size=40))
    if PRODUCTION_BUILD:
        output = subprocess.check_output(["tokei", "--output=json", "."])
        output = json.loads(output)
        lines = int(output["Python"]["code"])
        slide.box().text(f"({lines} lines of Python)",
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

    seconds = minutes * 60
    fps = step_count / seconds
    fps_box.text(f"@{fps:.2f} FPS", T(size=50))


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
    print_stats(slides, minutes=30)

# if PRODUCTION_BUILD:
#     slides.render("slides.pdf", slide_postprocessing=page_numbering)
# else:
slides.render("slides.pdf")
