import pandas as pd
from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG, dimmed_list_item, quotation, render_plot, source


def context(slides: Slides):
    @slides.slide()
    def how_do_we_ship_rust(slide: Box):
        slide.box().text("How do we ship Rust?", T(size=80))

    TERMINAL_BG = "#2E3436"

    @slides.slide(bg_color=TERMINAL_BG)
    def rustup_update(slide: Box):
        slide.box(width=1800).image("images/rustup-update.png")

        heights = [452] + [40] * 2 + [41] * 5 + [38] * 2 + [0]
        y_start = 140
        for (index, height) in enumerate(heights):
            y = y_start + sum(heights[:index])
            slide.box(x=60, y=y, width=1850, height=sum(heights[index:]), show=f"{index + 1}").rect(bg_color=TERMINAL_BG)

    @slides.slide()
    def shipping_rust(slide: Box):
        slide.box(p_bottom=40).text("What does it ~emph{mean} to ship Rust?", T(size=80))

        items = [
            "Discussing",
            "Implementing",
            "Reviewing",
            "Testing",
            "Integrating",
            "Deploying"
        ]

        lst = unordered_list(slide.box())
        for (index, item) in enumerate(items):
            dimmed_list_item(lst, item, last=item==items[-1], show=index + 2)
        slide.box(show="next+", p_top=40).text("changes to the Rust toolchain")

    @slides.slide()
    def rust_is_big(slide: Box):
        """
        Big on the outside, big on the inside.
        """
        rows = [
            "There are many changes",
            "shipped to many Rustaceans",
            "every single day"
        ]
        for (index, row) in enumerate(rows, start=1):
            slide.box(show=f"{index}+").text(row, T(size=80))

    @slides.slide()
    def stackoverflow_survey(slide: Box):
        """
        https://survey.stackoverflow.co/2023/#most-popular-technologies-language-prof
        A lot of people and companies are using Rust.
        """
        img = slide.box(width=1200).image("images/stackoverflow-survey.png")
        text = img.box(x=1350, y=700).text("~15%", escape_char="_")
        img.line((
            (text.x("0%"), text.y("100%").add(10)),
            (text.x("100%").add(-600), text.y("100%").add(10)),
        ), stroke_width=8, color="red", end_arrow=Arrow(size=30))
        source(slide, "Stack Overflow Developer Survey 2025")

    @slides.slide(bg_color=GITHUB_BG)
    def github_rust_repos(slide: Box):
        slide.box(width=1800).image("images/github-rust-repos.png")
        slide.fbox(x=540, y=170, width=190, height=60).rect(color="red", stroke_width=8)

    # @slides.slide()
    # def crate_count(slide: Box):
    #     slide.box().text("Crate count (270k+)")
    #     df = pd.read_csv("data/crates-per-month.csv")
    #     plot = render_plot(df)
    #     slide.box().image(plot, image_type="png")
    #
    # @slides.slide()
    # def crate_downloads(slide: Box):
    #     slide.box().text("Crate downloads (315B+)")
    #     df = pd.read_csv("data/crate-downloads-per-month.csv")
    #     plot = render_plot(df, ylabel="Count (billions)")
    #     slide.box().image(plot, image_type="png")
    #

    @slides.slide()
    def rust_toolchain_downloads(slide: Box):
        """
        https://app.datadoghq.com/dashboard/g3b-bag-mx9/content-delivery-networks?fromUser=false&refresh_mode=sliding&from_ts=1779780556183&to_ts=1779784156183&live=true
        https://app.datadoghq.com/dashboard/dsc-cnx-2cd/rustc-downloads-versions-and-targets?fromUser=false&fullscreen_end_ts=1779785026401&fullscreen_paused=false&fullscreen_refresh_mode=sliding&fullscreen_section=overview&fullscreen_start_ts=1779781426401&fullscreen_widget=3303264091969212&refresh_mode=sliding&from_ts=1779780568972&to_ts=1779784168972&live=true
        """
        slide.box().text("Rust toolchain downloads (1 hour)")
        slide.box(width=1100).image("images/toolchain-downloads.png")
        slide.box().text("~14 TiB/hour", escape_char="#")

    @slides.slide()
    def rust_inside_infra_size(slide: Box):
        """
        https://github.com/rust-lang/infra-team/tree/main/service-catalog
        """
        slide.box(p_bottom=60).text("A lot of stuff is happening within Rust!", T(size=70))

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("300+ Rust Project members")
        lst.item(show="next+").text("5 GitHub organizations")
        lst.item(show="next+").text("300+ repositories")
        lst.item(show="next+").text("~tt{rust-lang/rust}")
        lst2 = lst.ul(indent=40)
        lst2.item(show="next+").text("1.1k+ open PRs", "small")
        lst2.item(show="next+").text("11k+ open issues", "small")
        lst2.item(show="next+").text("~30-40 PRs merged every day", escape_char="#", style="small")

    @slides.slide()
    def impostor_syndrome(slide: Box):
        quotation(slide.box(), """…we don't think it's sufficient to build robust systems by only
including people who don't make mistakes; we think it's better
to ~bold{provide tooling and process to catch and prevent mistakes}.
""", 'Jane Losare-Lusby', size=50)
        source(slide, "https://blog.rust-lang.org/inside-rust/2022/04/19/imposter-syndrome")

    @slides.slide()
    def infrastructure(slide: Box):
        slide.box().text("Automation and infrastructure\nthat helps us ship Rust every day", T(size=80))
        slide.box(p_top=80, show="next+").text("(and how it has evolved over time)", T(size=60))
