import math
from typing import List, Literal, Optional, Tuple

import elsie
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from ergonomics import ergonomics
from history import history
from performance import performance
from reliability import reliability
from sections import SectionManager
from utils import COLOR_ORANGE, LOWER_OPACITY, QUOTATION_BG, code, dimmed_list_item, \
    generate_qr_code, quotation

"""
TODO: add links to articles
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
    """
    Why do tech companies use it?
    Why do programmers like it?
    Why could it be useful to you?
    Why not use it?
    """
    slide.box(p_bottom=sh(60), width=sw(300)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("Co vám může nabídnout Rust?", style=T(bold=True))
    slide.box().text("Kuba Beránek", style=T(size=40))


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100))
    line = row.box(padding=40, width=sw(100), height=sh(500))
    line.fbox().rect(bg_color="black")
    right = row.box()
    return (left, right)


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=40))

    content = slide.box()
    (left, right) = two_column_layout(content)

    gh = right.box(horizontal=True, p_bottom=sh(20))
    gh.box(width=sw(80)).image("images/github-logo.png")
    gh.box(p_left=sw(40)).text("github.com/kobzol", style=T(size=50, bold=True))

    gh_qr = generate_qr_code("https://github.com/kobzol")
    right.box().image(gh_qr, image_type="png")

    left.box(x=0, p_bottom=sh(40)).text("Kuba Beránek", T(align="left", size=50, bold=True))
    lst = unordered_list(left.box(x=0))
    dimmed_list_item(lst, "PhD student, teacher @ VSB-TUO", show=2)
    dimmed_list_item(lst, "Researcher @ IT4Innovations", show=3)
    dimmed_list_item(lst, "HPC, distributed systems, code optimization,\nmachine learning,…",
                     show=4)
    lst.item(show="last").text("Rust project contributor")


@slides.slide()
def teams(slide: Box):
    content = slide.box()
    height = 960
    reference = content.box(height=sh(height)).image("images/wg-perf.png")
    offset = 30

    # Link: https://www.rust-lang.org/governance/teams/infra
    # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Binary%20size%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Parallel%20rustc%20working%20group
    for (index, image) in enumerate((
            # "wg-parallel-rustc",
            # "wg-binary-size",
            "team-infra",
    )):
        content.box(
            show="next+",
            x=reference.x("0").add(offset * (index + 1)),
            y=reference.y("0").add(offset * (index + 1)),
            height=sh(height - (30 * (index - 1)))
        ).image(f"images/{image}.png")


@slides.slide()
def rust_features(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Rust in a nutshell", T(size=80, bold=True))
    lst = unordered_list(content.box())

    topics = (
        "Static + strong typing",
        "OOP + FP paradigms",
        "Syntax based on C",
        "Compiled to native code",
        "No GC, minimal runtime",
        "Integrated package manager"
    )
    for (index, topic) in enumerate(topics):
        dimmed_list_item(lst, topic, show=index + 2)
    lst.item(show="last").text("Friendly community")


@slides.slide()
def hello_world(slide: Box):
    slide.update_style("code", T(size=50))

    content = slide.box()
    content.box(width=sw(300)).image("images/ferris-2.png")
    code(content.box(), """fn main() {
    println!("Hello TechMeetup!");    
}""")


@slides.slide()
def rust_history(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Rust history and testimonials", T(size=80))


history(slides)


@slides.slide()
def rust_slogan(slide: Box):
    slide.box(width=sw(1400)).image("images/rust-slogan.png")


def trifecta(slides: SlideDeck,
             type: Optional[Literal["reliability", "performance", "ergonomics"]] = None):
    slide = slides.new_slide()
    slide.box(width=sw(1800)).image("images/rust-trifecta.png")

    bg_color = "white"
    stroke_width = 8
    if type == "reliability":
        slide.box(x=sw(670), y=sh(370), width=sw(570), height=sh(400)).rect(color=bg_color,
                                                                            stroke_width=stroke_width)
    elif type == "performance":
        slide.box(x=sw(70), y=sh(370), width=sw(580), height=sh(430)).rect(color=bg_color,
                                                                           stroke_width=stroke_width)
    elif type == "ergonomics":
        slide.box(x=sw(1280), y=sh(370), width=sw(570), height=sh(470)).rect(color=bg_color,
                                                                             stroke_width=stroke_width)
    else:
        assert type is None


section_manager = SectionManager()

trifecta(slides)

trifecta(slides, "reliability")

with section_manager.start_section(slides, "Reliability"):
    reliability(slides)

trifecta(slides, "performance")

with section_manager.start_section(slides, "Performance"):
    performance(slides)

trifecta(slides, "ergonomics")

with section_manager.start_section(slides, "Ergonomics"):
    ergonomics(slides)

if PRODUCTION_BUILD:
    section_manager.apply(slides)

trifecta(slides)


@slides.slide()
def why_not_rust(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(40)).text("Why not Rust?", T(bold=True))

    lst = unordered_list(content, show=None)
    dimmed_list_item(lst, "Learning curve", show=2, highlight_steps=4)

    google_survey = slide.overlay(show="3-4")
    google_survey.box(width=sw(1400)).image("images/google-rust-learning-curve.png")
    # Source: https://opensource.googleblog.com/2023/06/rust-fact-vs-fiction-5-insights-from-googles-rust-journey-2022.html
    quotation(google_survey.overlay().box(show="4"), """More than 2/3 of respondents are confident in contributing
to a Rust codebase within two months or less when learning Rust.""", "Google")
    l2 = lst.ul()
    dimmed_list_item(l2, "Functional paradigm", show=5, highlight_steps=1)
    dimmed_list_item(l2, "No inheritance :-)", show=6)

    dimmed_list_item(lst, "Programming workflow", show=7, highlight_steps=2)
    l2 = lst.ul()
    dimmed_list_item(l2, "Compile -> Run cycle", show=8, highlight_steps=1)
    dimmed_list_item(l2, "More development up front,\nless production bugs", show=9)

    dimmed_list_item(lst, "Ecosystem", show=10, highlight_steps=1)
    l2 = lst.ul()
    dimmed_list_item(l2, "Symfony/Django/Spring/ASP.NET (?)", show=11)

    lst.item(show="last").text("Job Market")


@slides.slide()
def usecase_example(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(40)).text("Where to try Rust?", T(bold=True))

    lst = unordered_list(content)
    dimmed_list_item(lst, "Libraries", show=2)

    topics = ("CLI applications", "Web services (REST, GraphQL, …)", "WebAssembly",
              "Cloud functions, serverless",
              "Tooling, infrastructure", "Data analysis", "Perf. critical Python/Node.js",
              "Embedded")
    for (index, topic) in enumerate(topics):
        dimmed_list_item(lst, topic, show=index + 3)
    lst.item(show="last").text("...")


def accelerate_code(parent: Box, code_left: str, code_right: str, language: str):
    left_code_width = sw(800)
    row = parent.box(horizontal=True)
    left = row.box(width=left_code_width)
    code(left.box(), code_left, width=left_code_width)

    row.box(show="next", padding=20).text("+", T(size=160))

    right_code_width = sw(900)
    right = row.box(show="last", width=sw(right_code_width))
    code(right.box(), code_right, language=language, width=right_code_width)


@slides.slide()
def accelerate_nodejs(slide: Box):
    slide.update_style("code", T(size=30))

    content = slide.box()
    content.box(p_bottom=sh(40)).text("Accelerate Node.js", T(bold=True))
    qr = generate_qr_code("https://napi.rs/")
    slide.box(x=sw(1400), y=0).image(qr, image_type="png")

    accelerate_code(content, """use napi_derive::napi;

#[napi]
fn fibonacci(n: u32) -> u32 {
    match n {
        1 | 2 => 1,
        _ => fibonacci(n - 1) +
             fibonacci(n - 2),
    }
}""", """import { fibonacci } from './rusty.js'

console.log(fibonacci(5))""", language="js")


@slides.slide()
def accelerate_nodejs(slide: Box):
    slide.update_style("code", T(size=30))

    content = slide.box()
    content.box(p_bottom=sh(40)).text("Accelerate Python", T(bold=True))
    qr = generate_qr_code("https://pyo3.rs/")
    slide.box(x=sw(1400), y=0).image(qr, image_type="png")

    accelerate_code(content, """use pyo3::pyfunction;

#[pyfunction]
fn fibonacci(a: u32) -> u32 {
    match n {
        1 | 2 => 1,
        _ => fibonacci(n - 1) +
             fibonacci(n - 2),
    }
}""", """import rusty
print(rusty.fibonacci(5))""", language="python")


qr_code_width = 500


@slides.slide()
def how_to_start(slide: Box):
    content = slide.box()
    (left, right) = two_column_layout(content)

    left.box(p_bottom=sh(40)).text("The Rust Programming Language", T(size=54))
    left.box(width=sw(600)).image("images/trpl.png")

    qr = generate_qr_code("https://doc.rust-lang.org/book/", scale=16)
    right.box(width=sw(qr_code_width)).image(qr, image_type="png")


@slides.slide()
def how_to_start(slide: Box):
    content = slide.box()
    (left, right) = two_column_layout(content)

    left.box(p_bottom=sh(40)).text("Rust course @ FEI VSB-TUO", T(size=54))
    left.box().text("~tt{github.com/kobzol/rust-course-fei}", T(size=42))

    qr = generate_qr_code("https://github.com/kobzol/rust-course-fei", scale=16)
    right.box(width=sw(qr_code_width)).image(qr, image_type="png")


@slides.slide()
def aoc(slide: Box):
    content = slide.box()
    (left, right) = two_column_layout(content)

    left.box(show="next+", p_bottom=sh(20)).text("Advent of Code")
    left.box(width=sw(900)).image("images/advent-of-code.png")

    wrapper = slide.overlay(show="next").box()
    wrapper.rect(bg_color=QUOTATION_BG)
    wrapper = wrapper.box(padding=20, horizontal=True)
    wrapper.box().image("images/rust-logo.png")
    wrapper.box(padding=20).text("♥", T(color="red", size=200))
    wrapper.box().image("images/advent-of-code-logo.png")

    qr = generate_qr_code("https://adventofcode.com/", scale=16)
    right.box(width=sw(qr_code_width)).image(qr, image_type="png")


@slides.slide()
def meetup(slide: Box):
    content = slide.box()
    row = content.box(horizontal=True)
    row.box(width=sw(500)).image("images/techmeetup.png")
    row.box(p_left=sw(40), p_right=sw(40)).text("+", T(size=200))
    row.box(width=sw(500)).image("images/rust-logo.png")
    content.box(p_top=sh(40), show="next+").text("Beginning of 2024 (?)")
    content.box(show="last+").text("Stay tuned :-)")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Děkuji za pozornost", style=T(size=70, bold=True))

    slide.box().text("Slidy jsou dostupné zde:")
    qr = generate_qr_code("https://github.com/kobzol/talks/blob/main/2023/techmeetup-rust/",
                          scale=14)
    slide.box().image(qr, image_type="png")

    slide.box().text("Slidy byly vytvořeny pomocí ~tt{github.com/spirali/elsie}",
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
