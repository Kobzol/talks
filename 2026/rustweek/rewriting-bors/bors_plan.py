from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from history import get_history_timeline
from utils import GITHUB_BG_COLOR, HACKMD_BG_COLOR, bors_impl, bors_impl_counter, \
    chapter, \
    dimmed_list_items, source


def bors_plan(slides: Slides):
    @slides.slide()
    def next_steps(slide: Box):
        chapter(slide, "Looking for a homu successor")

    @slides.slide(bg_color=HACKMD_BG_COLOR)
    def homu_rewrite_hackmd(slide: Box):
        """
        https://hackmd.io/wJm0ZqqPR-iDWHhlEC789Q
        """
        slide.box(width=1300).image("images/homu-rewrite-hackmd.png")

    timeline = get_history_timeline()

    def year_2016(box: Box):
        """
        https://github.com/bors-ng/bors-ng
        """
        bors_impl(box, "bors-ng/bors-ng", "December 2016", "elixir-logo.svg", "23.2k")
        bors_impl_counter(box)

    def year_2019(box: Box):
        """
        https://github.com/bors-rs/bors
        """
        bors_impl(box, "bors-rs/bors", "November 2019", "rust-logo.png", "10k")
        bors_impl_counter(box)

    def year_2021(box: Box):
        """
        https://www.reddit.com/r/rust/comments/qi5xhv/github_testing_a_native_borslike_feature
        """
        box.box(width=1200, show="1").image("images/github-merge-queue-announcement.png")
        box.box(width=1400, x="[50%]", y="[50%]", show="2").image(
            "images/graydon-merge-queue-reaction.png")

    def year_2022(box: Box):
        box.box(p_bottom=40).text("Existing solutions:", T(size=75))
        lst = unordered_list(box.box())
        item1 = lst.item(show="next+").text("bors-rs/bors")
        item2 = lst.item(show="next+").text("bors-ng/bors-ng")

        x = item1.x("100%").add(175)
        width = 65
        box.box(x=x, y=item1.y("0"), width=width, show="2+").image("images/cross.png")
        box.box(x=x, y=item2.y("0"), width=width, show="last+").image("images/cross.png")

    def year_2023(box: Box):
        box.box(width=1600).image("images/bors-ng-deprecation.png")

    timeline.render_year(2016, year_2016)
    timeline.render_year(2019, year_2019)
    timeline.render_year(2021, year_2021)
    timeline.render_year(2022, year_2022)
    timeline.render_year(2023, year_2023)

    @slides.slide()
    def merge_queues(slide: Box):
        """
        why not MQs? speculative execution, too expensive for us
        merge latency
        """
        slide.box(p_bottom=100).text("What about GitHub merge queues?")

    @slides.slide(bg_color=HACKMD_BG_COLOR)
    def merge_queue_hackmd(slide: Box):
        slide.box(width=1200).image("images/merge-queue-hackmd.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def rustc_pr_count(slide: Box):
        slide.box(width=1300).image("images/rust-pr-count.png")

    @slides.slide()
    def rustc_pr_tracking(slide: Box):
        slide.box(width=1800).image("images/rustc-pr-tracking.png")
        slide.box(x="[90%]", y="[10%]").text("30-35 PRs/day", T(color="red"))
        source(slide, "Rustc PR tracking")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def ci_job_statistics(slide: Box):
        slide.box(width=1800).image("images/gh-jobs-statistics.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def ci_usage_statistics(slide: Box):
        slide.box(width=1700).image("images/gh-usage-statistics.png")

    @slides.slide()
    def github_agreement(slide: Box):
        slide.box(width=1600).image("images/github-agreement.png")

    @slides.slide()
    def marco_optimizations(slide: Box):
        """
        At most 8 PRs merged per day.
        """
        slide.box(width=1600).image("images/marco-optimizations.png")
        source(slide, 'How We Made the Rust CI 75% Cheaper by Marco Ieni @ RustConf 2025')

    @slides.slide()
    def pr_batching(slide: Box):
        slide.box().text("We need to batch PRs to merge >8 PRs/day")

    @slides.slide()
    def merge_queue_animation(slide: Box):
        slide.box(y=100).text("How GitHub merge queue does batching")

        width = 800
        row = slide.box(width=width, horizontal=True)
        row.rect(color="black", stroke_width=4)

        prs = [8, 3, 14, 28, 42]
        boxes = []
        for item in range(len(prs)):
            pr_box = row.box(height="100%", width=width / len(prs))
            pr_box.rect(color="black", stroke_width=4)
            boxes.append(pr_box)
            pr_box = pr_box.box(padding=15)
            pr = prs[item]
            pr_box.text(f"#{pr}")

        def mark(start: int, end: int, text: str, up: bool, show: str, offset: int = 0):
            y_offset = 20 + offset
            y_start = boxes[0].y("0").add(-y_offset) if up else boxes[0].y("100%").add(y_offset)
            y_offset = -50 if up else 50

            slide.box(show=show).line((
                (start, y_start),
                (start, y_start.add(y_offset)),
                (end, y_start.add(y_offset)),
                (end, y_start)
            ), color="black", stroke_width=4)
            text_x = end.map(lambda v: start.eval() + (v - start.eval()) / 2 - 100)
            text_y = y_start.add(y_offset * 3 + 10) if up else y_start.add(y_offset + 10)
            slide.box(show=show, x=text_x, y=text_y).text(text)

        mark(boxes[0].x("0"), boxes[0].x("100%"), "CI run 1", up=False, show="2+")
        mark(boxes[0].x("0"), boxes[1].x("100%"), "CI run 2", up=True, show="3+")
        mark(boxes[0].x("0"), boxes[2].x("100%"), "CI run 3", up=False, show="4", offset=150)

    @slides.slide()
    def rollup_creation(slide: Box):
        slide.box().text("How bors/homu does batching")

        slide.box(width=1800).image("images/rollup-creation.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def rollup(slide: Box):
        slide.box(width=1400).image("images/rollup.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def rollup_45_prs(slide: Box):
        """
        https://github.com/rust-lang/rust/pull/19958
        """
        slide.box(width=1700, p_bottom=40).image("images/rollup-45-prs.png")
        slide.box().text("Rollup of 45 PRs!", T(color="white"))

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def rollup_history(slide: Box):
        slide.box(x=100, width=1000).image("images/rollup-history.png")

    @slides.slide()
    def merge_queues(slide: Box):
        slide.box(p_bottom=40).text("GitHub merge queue problems", T(size=80))
        lst = unordered_list(slide.box())
        dimmed_list_items(lst, 1, [
            "Wastes CI compute",
            "Not configurable enough (no rollups)"
        ])

    @slides.slide(bg_color="#F5E8BA")
    def riir(slide: Box):
        slide.box(width=700).image("images/riir.png")

    @slides.slide()
    def why_a_rewrite(slide: Box):
        """
        https://news.ycombinator.com/item?id=21586256
        """
        slide.box(p_bottom=50).text("Why a rewrite?", T(size=80))

        lst = unordered_list(slide.box())
        dimmed_list_items(lst, 2, [
            "Own our code",
            "Error recovery & better race condition handling",
            "Integration tests",
            "Make contributions possible (and easy!)",
            "~bold{Build trust}"
        ])

    @slides.slide(bg_color="#2C2A26")
    def weekend_project(slide: Box):
        slide.box(width=1700).image("images/weekend-project-redacted.png")

    @slides.slide()
    def weekend_project(slide: Box):
        slide.box(width=800).image("images/programmers-credo.jpg")
        source(slide, "Pinboard")

    def bors(box: Box):
        """
        Bors stack: tokio + axum + octocrab
        Web application that listens for webhooks and uses the GitHub API.

        By the way, I don't know what it is about winder and December, but there seems to be
        something in the air that causes people to implement a new version of bors.

        graydon/bors - February 2013
        barosl/homu - December 2014
        servo/homu - December 2015
        rust-lang/homu - December 2015
        bors-ng/bors-ng - December 2016
        bors-rs/bors - November 15 2019
        rust-lang/bors - December 30 2022
        """
        bors_impl(box, "rust-lang/bors", "December 2022", "rust-logo.png", "28.7k")
        bors_impl_counter(box)

        y = 220
        width = 400
        items = [
            (-110, "February"),
            (25, "December"),
            (145, "December"),
            (280, "December"),
            (680, "November"),
            (1075, "December"),
        ]
        wrapper = box.fbox(x=0, y=0, show="next+")
        for (x, month) in items:
            wrapper.box(x=x, y=y, width=width).text(month, T(align="right", bold=True),
                                                    rotation=-90)

    timeline.years.pop()  # remove 2023 year
    timeline.render_year(2022, bors)
