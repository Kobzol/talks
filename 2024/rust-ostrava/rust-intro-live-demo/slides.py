import io
from typing import Tuple

import elsie
import pandas as pd
from elsie import Arrow, SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from utils import LOWER_OPACITY, code, dimmed_list_item, generate_qr_code

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
    row.box(width=sw(400), p_right=sw(60)).image("images/tmo-logo.png")
    row.box(width=sw(400), p_right=sw(60)).image("images/rust-logo.png")
    row.box(width=sw(400), p_right=sw(60)).image("images/ferris-cz.png")
    row.box(width=sw(600)).image("images/espressif.png")
    slide.box(p_bottom=sh(40)).text("TechMeetup Ostrava: Rust", style=T(bold=True))


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100), height="fill")
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

    left.box(x=0, p_bottom=sh(40)).text("Kuba Beránek", T(align="left", size=50, bold=True))
    lst = unordered_list(left.box(x=0))
    lst.item(show="next+").text("PhD/teaching/work @ VSB-TUO, IT4Innovations")
    lst.item(show="next+").text("Maintainer @ Rust Project")


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
def rust_czech_republic(slide: Box):
    slide.box().image("images/ferris-cz.png")


@slides.slide()
def rust_meetups_in_czech_republic(slide: Box):
    content = slide.fbox()
    content.fbox(width=sw(1400)).image("images/rust-brno.png")
    content.overlay(show="next+").image("images/rust-bratislava.png")
    content.overlay(show="next+").box(width=sw(1600)).image("images/meetup-1.jpg")
    content.overlay(show="next+").box(width=sw(1400)).image("images/meetup-braiins-1.png")


@slides.slide()
def rustlangcz(slide: Box):
    content = slide.fbox()
    left, right = two_column_layout(content)
    left.box(p_bottom=sh(80)).text("~tt{rustlang.cz}", T(size=100))
    qr = generate_qr_code(
        "https://rustlang.cz",
        scale=16
    )
    right.image(qr, image_type="png")


@slides.slide()
def techmeetup_talk(slide: Box):
    content = slide.fbox()
    left, right = two_column_layout(content)
    # left.box(width=sw(1000)).image("images/techmeetup-conf-intro-slide.png")
    left.box().text("Rust - programovací jazyk pro klidný spánek", T(size=sw(50), bold=True))
    left.box().text("TechMeetup conference Ostrava 3. 11. 2023", T(size=sw(46)))
    left.box(p_top=sh(40)).text("Intro talk about Rust, recording on YouTube", T(size=sw(40)))
    qr = generate_qr_code(
        "https://www.youtube.com/watch?v=bGVYof8WBSI",
        scale=16
    )
    right.image(qr, image_type="png")


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
    row = content.box(horizontal=True)
    row.box(width=sw(300), p_right=sw(40)).image("images/ferris-2.png")
    row.box(width=sw(250)).image("images/rust-logo.png")
    code(content.box(p_top=sh(40)), """fn main() {
    println!("Hello TechMeetup!");    
}""")


@slides.slide()
def trifecta(slide: Box):
    slide.box(width=sw(1800)).image("images/rust-trifecta.png")


@slides.slide()
def areas(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Use-cases for Rust", T(size=80, bold=True))
    lst = unordered_list(content.box())

    topics = (
        "Web services (REST, GraphQL, backend, …)",
        "Cloud functions, serverless",
        "WebAssembly, web frontend",
        "Libraries",
        "CLI applications, tooling, infrastructure",
        "Data analysis, perf. critical Python/Node.js",
        "Embedded"
    )
    for (index, topic) in enumerate(topics):
        dimmed_list_item(lst, topic, show=index + 2)
    lst.item(show="last").text("...")


@slides.slide()
def companies(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Who uses Rust?", T(size=80, bold=True))
    lst = unordered_list(content.box())
    lst.item(show="next+").text("Google, Meta, Amazon, Microsoft, Linux, ...")
    lst.item(show="next+").text("Cloudflare, Dropbox, Discord, Figma, NPM, ...")
    lst.item(show="next+").text(
        "CDN77, Microsoft, Espressif, Hardwario, Edhouse,\n"
        "Rockwell, SatoshiLabs, Braiins, IT4Innovations, ...")
    lst.item(show="next+").text("and many others")


@slides.slide()
def crates_io_stats(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(40)).text("~tt{crates.io}", T(size=sw(80)))
    content.box(width=sw(1400)).image("images/crates.io-stats.png")


def render_plot(data):
    import seaborn as sns
    import matplotlib.pyplot as plt

    data["date"] = pd.to_datetime(data["date"])

    plt.clf()
    with plt.xkcd():
        px = 1 / plt.rcParams["figure.dpi"]
        plt.figure(figsize=(1200 * px, 700 * px))

        ax = sns.lineplot(data=data, x="date", y="count")
        ax.tick_params(labelsize=20)
        ax.set_xlabel("Year", fontsize=20)
        ax.set_ylabel("Count", fontsize=20)
        ax.ticklabel_format(style="plain", axis="y")
        ax.set_xlim(pd.Timestamp("2014-07-01"), pd.Timestamp("2024-04-14"))

        buffer = io.BytesIO()

        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
    return buffer


def growth(slides: SlideDeck):
    # 10. 4. 2024: 152268925
    counts = [
        ("Crate count (140k+)", "data/crates-per-month.csv"),
        ("Crate downloads (60B+)", "data/crate-downloads-per-month.csv"),
    ]
    for (title, data) in counts:
        slide = slides.new_slide()
        slide.box().text(title)
        df = pd.read_csv(data)
        plot = render_plot(df)
        slide.box().image(plot, image_type="png")


growth(slides)


@slides.slide()
def stack_overflow_survey(slide: Box):
    content = slide.box()
    content.box(width=sw(1400)).image("images/stack-overflow-streak.png")


@slides.slide()
def usage_1(slide: Box):
    # https://www.jetbrains.com/lp/devecosystem-2023/languages/
    left, right = two_column_layout(slide.box())
    left.box(width=sw(900)).image("images/rust-usage-1.png")
    right.box().text("JetBrains Ecosystem survey", T(size=sw(50)))
    y = 815
    left.line(((sw(1050), sh(y)), (sw(950), sh(y))), stroke_width=20, color="red",
                 end_arrow=Arrow(size=30))


@slides.slide()
def usage_2(slide: Box):
    # https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/
    left, right = two_column_layout(slide.box())
    left.box(width=sw(1100)).image("images/rust-usage-2.png")
    right.box().text("Statista.com", T(size=sw(50)))
    y = 850
    left.line(((sw(50), sh(y)), (sw(150), sh(y))), stroke_width=20, color="red",
              end_arrow=Arrow(size=30))

# Usage by programmers, crate downloads, stars on GitHub
# 90k+ stars, 140k+ crates, 60+ billion crate downloads
# JetBrains 2023 ecosystem survey: 10% used Rust, 10% plan to use Rust
# JetBrains: Trust in Rust: A story of growth
# https://github.blog/2023-11-08-the-state-of-open-source-and-ai/
# GitHub: Rust continues to rise


@slides.slide()
def live_demo(slide: Box):
    slide.box(p_bottom=sh(60)).text("Live demo", T(size=sw(90)))
    slide.box(show="next+").text("~bold{Goal}: implement a web app in Rust")
    slide.box(show="next+").text("From scratch, in 45 minutes")
    slide.box(show="next+").text("…what could go wrong?")


@slides.slide()
def rust_web_app_demo(slide: Box):
    content = slide.fbox()
    left, right = two_column_layout(content)
    left.box(p_bottom=sh(80)).text("~tt{github.com/kobzol/rust-web-app-demo}", T(size=40))
    qr = generate_qr_code(
        "https://github.com/kobzol/rust-web-app-demo",
        scale=16
    )
    right.image(qr, image_type="png")


qr_code_width = 750


@slides.slide()
def how_to_start(slide: Box):
    content = slide.box()
    (left, right) = two_column_layout(content)

    left.box(p_bottom=sh(40)).text("The Rust Programming Language", T(size=54))
    left.box(width=sw(600)).image("images/trpl.png")

    qr = generate_qr_code("https://doc.rust-lang.org/book/", scale=16)
    right.box(width=sw(qr_code_width)).image(qr, image_type="png")


@slides.slide()
def how_to_start_fei_course(slide: Box):
    content = slide.box()
    (left, right) = two_column_layout(content)

    left.box(p_bottom=sh(40)).text("Rust course @ FEI VSB-TUO", T(size=54))
    left.box().text("~tt{github.com/kobzol/rust-course-fei}", T(size=42))

    qr = generate_qr_code("https://github.com/kobzol/rust-course-fei", scale=16)
    right.box(width=sw(qr_code_width)).image(qr, image_type="png")


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
