from typing import Optional

from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import render_bot, topic


def development(slides: Slides):
    @slides.slide()
    def development(slide: Box):
        topic(slide.box(), "Development", "hammer_and_spanner.svg")

    @slides.slide()
    def sending_a_pr(slide: Box):
        slide.box(y=20).text("Sending a PR")

        step = 1

        def img(image: str, width=1700, bot: Optional[str] = None):
            nonlocal step

            slide.box(width=width, x="[50%]", y="[50%]", show=str(step)).image(f"images/{image}.png")
            if bot is not None:
                render_bot(slide, bot, show=step)
            step += 1

        img("cache-derive-macro-pr")
        img("triagebot-review", bot="rustbot")
        img("pr-birthday")
        img("rustbot-communication", width=1200, bot="rustbot")
        img("triagebot-range-diff", bot="rustbot")
        img("perf-1", bot="perfbot")
        # img("perf-2", bot="perfbot")
        # img("perf-3", width=1100, bot="perfbot")
        img("perf-4")
        img("bors-review", width=1300, bot="bors")

    @slides.slide()
    def bors(slide: Box):
        slide.box(width=1400).image("images/no-rocket-science-rule.png")
        render_bot(slide, "bors")

    @slides.slide()
    def ci_costs(slide: Box):
        slide.box(y=50).text("CI costs")
        slide.box(width=1800).image("images/github-actions-jobs.png")

        slide.box(show="next+", p_top=100).text("For each merged PR:")
        lst = unordered_list(slide.box(show="last+"))
        lst.item(show="last+").text("~3 hours walltime", escape_char="#")
        lst.item(show="next+").text("~150 runner hours", escape_char="#")
        lst.item(show="next+").text("~600 (!) CPU hours", escape_char="#")

    @slides.slide()
    def ci_costs_2(slide: Box):
        slide.box(y=50).text("CI costs")
        slide.box().image("images/github-actions-stats.png")

    @slides.slide()
    def ci_costs_2(slide: Box):
        slide.box(y=50).text("CI costs")
        lst = unordered_list(slide.box())
        lst.item().text("$140 per merged PR")
        lst.item().text("$50 000 per month!")

    @slides.slide()
    def github(slide: Box):
        slide.box(width=1400).image("images/gh-issue-counts.png")

    @slides.slide()
    def rollups(slide: Box):
        slide.box(y=20).text("Rollups")
        slide.box(width=1300, y=140).image("images/rollup.png")
        render_bot(slide, "bors")

    @slides.slide()
    def empowering_new_contributors(slide: Box):
        slide.box().text("Empowering new contributors")

    @slides.slide()
    def empowering_contributors(slide: Box):
        step = 1

        def img(image: str, width=1700, bot: Optional[str] = None):
            nonlocal step

            slide.box(width=width, x="[50%]", y="[50%]", show=str(step)).image(f"images/{image}.png")
            if bot is not None:
                render_bot(slide, bot, show=step)
            step += 1

        img("rustc-dev-guide")
        img("x_setup", width=1600)
        img("triagebot-welcome", bot="rustbot")
        img("triagebot-merge-policy", bot="rustbot")
        img("bors-delegate", bot="bors")

    @slides.slide()
    def dev_desktops(slide: Box):
        slide.box(width=1700).image("images/dev-desktops.png")

    @slides.slide()
    def imposter_syndrome(slide: Box):
        slide.box(width=1700).image("images/imposter-syndrome.png")

    @slides.slide()
    def thanks(slide: Box):
        slide.box(width=1800).image("images/thanks-rlo.png")

    @slides.slide()
    def bors_thanks(slide: Box):
        slide.box(width=1800).image("images/bors-thanks.png")
