import datetime
import io
from typing import Callable

import pandas as pd
from elsie import SlideDeck, TextStyle as T
from elsie.boxtree.box import Box

from config import sh, sw
from utils import COLOR_ORANGE, next_two_slides, quotation


def timeline(slides: SlideDeck):
    years = []

    def render_year_tick(timeline: Box, year: int):
        this_year = datetime.datetime.now().year
        first_year = 2006

        wrapper_width = sw(100)
        point_width = sw(25)
        point_height = sh(80)

        x_percent = (year - first_year) / (this_year - first_year)
        timeline_entry = timeline.box(
            width=wrapper_width,
            x=timeline.x(f"{round(x_percent * 100)}%").add(-wrapper_width / 2),
            y=timeline.y("50%").add(-point_height / 2)
        )
        entry_tick = timeline_entry.box(width=point_width, height=point_height)
        entry_tick.rect(bg_color="black")

        timeline_entry.box(p_top=sh(20)).text(str(year), style=T(size=44), rotation=-45)

        return entry_tick

    def render_year(year: int, render_fn: Callable[[Box], None]):
        slide = slides.new_slide(debug_boxes=False)

        timeline_box = slide.fbox(height=sh(140), p_top=sh(40))
        timeline = timeline_box.box(width="90%", height=sh(30))
        timeline.rect(bg_color="black")

        # Year ticks
        for y in years:
            render_year_tick(timeline, y)
        entry_tick = render_year_tick(timeline, year)
        entry_tick.overlay().rect(bg_color=COLOR_ORANGE)

        # Margin
        slide.sbox(height=sh(60))
        content_box = slide.box(width="100%", height="fill")

        render_fn(content_box)
        years.append(year)

    def year_2006(box: Box):
        box.box(p_bottom=sh(60)).text("Started as a personal project\nby Graydon Hoare (@Mozilla)")
        quotation(box.box(show="next+"),
                  "I think I named it after fungi…\n\t\tthat is \"over-engineered for survival\".",
                  "Graydon Hoare")

    def year_2010(box: Box):
        logo = box.box(width=sw(800)).image("images/rust-intro-slide.png")
        box.box(show="next+", x=logo.x("100%"), y=box.y("0%"), width=sw(400)).image(
            "images/rust-logo.png")

    def year_2015(box: Box):
        row = box.box(horizontal=True)
        row.box(p_right=sw(40)).text("Rust 1.0 released")
        row.box(width=sw(100)).image("images/tada.png")
        box.box(p_top=sw(40), show="next+").text("Strong backwards-compatibility promise", T(size=50))

    def year_2017(box: Box):
        # 2020: ~12% of Firefox is written in Rust
        box.box(width=sw(1400), show="1").image("images/rust-stylo.png")
        box.overlay(show="next").box(width=sw(1600)).image("images/vscode-ripgrep.png")

    def year_2018(box: Box):
        box.box(width=sw(1400)).image("images/rust-edition-2018.png")
        box.overlay(show="next").box(width=sw(1600)).image("images/aws-firecracker.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/rust-cloudflare.png")
        box.overlay(show="next+").box(width=sw(1400)).image("images/rust-figma.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/figma-perf.png")

    def year_2019(box: Box):
        box.box(width=sw(1400)).image("images/rust-npm.png")
        quotation(box.overlay(show="next").box(), """The good news for the npm team is that the ~bold{Rust} service has been
~bold{running} for more than one year ~bold{in production without a single alert}.
This is in stark contrast to the usual experience of deploying a Node.js service…""", "npm",
                  size=sw(50))

    def year_2020(box: Box):
        box.box(show=next_two_slides(box, start=True), width=sw(1600)).image(
            "images/dropbox-rust.png")
        quotation(box.overlay(show="last").box(), """…~bold{betting on Rust was one of the best decisions we made}.
More than performance, its ergonomics and focus on correctness
has helped us tame sync’s complexity.""", "Dropbox")

        box.overlay(show="next+").box(width=sw(1600)).image("images/discord-rust.png")
        quotation(box.overlay(show="next").box(), """Even with just basic optimization, Rust was able to outperform
the hyper hand-tuned Go version.
…~bold{we were able to beat Go on every single performance metric}.""", "Discord")

    def year_2021(box: Box):
        box.box(width=sw(1400)).image("images/rust-edition-2021.png")

    def year_2022(box: Box):
        box.box(show=next_two_slides(box, start=True), width=sw(1400)).image(
            "images/aws-cloudfront.png")
        quotation(box.overlay(show="last").box(),
                  "It is written in Rust, so it reaps some of\nits benefits such as performance,\nthread and memory-safety.",
                  "AWS")

        box.overlay(show=next_two_slides(box)).box(width=sw(1400)).image("images/meta-rust.png")
        quotation(box.overlay(show="last").box(),
                  "…we’re committing to Rust long-term\nand welcome early adopters.", "Meta")

        box.overlay(show=next_two_slides(box)).box(width=sw(1700)).image("images/rust-android.png")
        quotation(box.overlay(show="last").box(),
                  "In Android 13, about 21% (1.5 million lines)\nof all new native code (C/C++/Rust) is in Rust.",
                  "Google")

        box.overlay(show=next_two_slides(box)).box(width=sw(1600)).image(
            "images/linux-kernel-rust.png")
        quotation(box.overlay(show="last").box(), "…on the whole, I don't hate it.",
                  "Linus Torvalds")

    def year_2023(box: Box):
        box.box(show="1", width=sw(1400)).image("images/github-code-search.png")

        windows_kernel = box.overlay(show=next_two_slides(box))
        windows_kernel.box(width=sw(1000)).image("images/windows-kernel-rust.png")
        quotation(windows_kernel.overlay(show="last").box(width=sw(600)),
                  """Speaking of languages, it's time to halt starting
any new projects in C/C++ and ~bold{use Rust for those scenarios
where a non-GC language is required}. For the sake of security
and reliability, the industry should declare those languages
as deprecated.""",
                  "Mark Russinovich")

        box.overlay(show="next").box(width=sw(1200)).image("images/windows-drivers-rust.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/azure-qdk-rust.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/ferrocene-rust.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/stack-overflow-streak.png")

    render_year(2006, year_2006)
    render_year(2010, year_2010)
    render_year(2015, year_2015)
    render_year(2017, year_2017)
    render_year(2018, year_2018)
    render_year(2019, year_2019)
    render_year(2020, year_2020)
    # render_year(2021, year_2021)
    render_year(2022, year_2022)
    render_year(2023, year_2023)


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
        ax.set_xlim(pd.Timestamp("2014-07-01"), pd.Timestamp("2023-11-30"))

        buffer = io.BytesIO()

        plt.savefig(buffer, format="png")
        buffer.seek(0)
    return buffer


def growth(slides: SlideDeck):
    counts = [
        ("Crate count (120k+)", "data/crates-per-month.csv"),
        ("Crate downloads (20B+)", "data/crate-downloads-per-month.csv"),
        ("GitHub stars (80k+)", "data/rust-stars.csv")
    ]
    for (title, data) in counts:
        slide = slides.new_slide()
        slide.box().text(title)
        df = pd.read_csv(data)
        plot = render_plot(df)
        slide.box().image(plot, image_type="png")

    slide = slides.new_slide()
    box = slide.box()
    box.image("images/slashdata-survey.jpg")
    box.box(x=sw(270), y=sh(770), width=sw(800), height=sh(65)).rect(color="red", stroke_width=8)

"""
https://github.blog/2023-08-30-why-rust-is-the-most-admired-language-among-developers
https://www.technologyreview.com/2023/02/14/1067869/rust-worlds-fastest-growing-programming-language/
"""


def history(slides: SlideDeck):
    timeline(slides)
    growth(slides)
