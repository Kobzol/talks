from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG_COLOR, INTELLIJ_BG_COLOR, chapter, dimmed_list_items, quotation


def homu(slides: Slides):
    @slides.slide()
    def homu_troubles(slide: Box):
        chapter(slide, "The homu years")

    # @slides.slide(bg_color=GITHUB_BG_COLOR)
    # def kobzol_activity(slide: Box):
    #     slide.box(width=1800).image("images/kobzol-2025-github-activity.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_usage(slide: Box):
        slide.box(width=1700).image("images/homu-2015-github-activity.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_bugs(slide: Box):
        """
        https://github.com/rust-lang/homu/issues/47
        https://github.com/rust-lang/homu/issues/75
        https://github.com/rust-lang/homu/issues/205
        https://github.com/rust-lang/homu/issues/214
        https://github.com/rust-lang/homu/issues/216
        https://github.com/barosl/homu/issues/48
        https://github.com/barosl/homu/issues/94
        https://github.com/barosl/homu/issues/106
        https://github.com/barosl/homu/issues/149
        """
        bugs = [1, 3, 8, 4, 5]
        col = slide.box()
        for (index, bug) in enumerate(bugs):
            col.box(x=0, show=f"{index + 1}+").image(f"images/homu-bug-{bug}.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_bug(slide: Box):
        slide.box(width=1500).image("images/homu-bug-9-full.png")

    width = 1600

    @slides.slide()
    def approve_try_build(slide: Box):
        """
        https://rust-lang.zulipchat.com/#narrow/channel/242791-t-infra/topic/bors.20merged.20PR.20without.20running.20all.20tests/near/455247371
        https://github.com/rust-lang/homu/issues/47

        Urban legends, tribal knowledge.
        """
        quotation(
            slide.box(width=width),
            "Thou shalt not approve a PR with an ongoing try build.",
            "An ancient Rust proverb (origin unknown)"
        )

    @slides.slide()
    def unapprove_tested_build(slide: Box):
        quotation(
            slide.box(width=width),
            "Nor shall you unapprove a PR that is being tested.",
            "An ancient Rust proverb (origin unknown)",
        )

    # r- retry vs retry r-

    @slides.slide(bg_color="#1C1C1C")
    def homu_stuck(slide: Box):
        slide.box(width=600).image("images/homu-stuck.png")

    @slides.slide(bg_color="#171819")
    def synchronize_button(slide: Box):
        slide.box(width=1400).image("images/homu-synchronize-1.png")
        slide.box(x=675, y=190, width=120).image("images/skull.svg")
        slide.box(x=470, y=210, width=190, height=80).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=INTELLIJ_BG_COLOR)
    def synchronize_impl_1(slide: Box):
        slide.box(x=100, width=1800).image("images/homu-synchronize-code-1.png")

    @slides.slide(bg_color=INTELLIJ_BG_COLOR)
    def synchronize_impl_2(slide: Box):
        slide.box(x=100, width=1400).image("images/homu-synchronize-code-2.png")

    @slides.slide(bg_color="#1C1C1C")
    def synchronize_warning(slide: Box):
        slide.box(width=1600).image("images/homu-synchronize-warning.png")
        slide.box(x=300, y=550, width=1250, height=130).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def synchronize_guide_1(slide: Box):
        slide.box(width=1600).image("images/homu-synchronize-docs-1.png")

    @slides.slide(bg_color="#0F141A")
    def synchronize_guide_2(slide: Box):
        slide.box(width=1100, p_bottom=30).image("images/homu-synchronize-docs-2.png")
        slide.box(show="next+").text("(the guide had 10 steps)", T(color="white"))

    @slides.slide()
    def synchronize_button_red(slide: Box):
        slide.box(width=1800).image("images/homu-synchronize-2.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def issue_tracker(slide: Box):
        slide.box(width=1500).image("images/homu-issue-tracker.png")

    @slides.slide(bg_color="#0D1017")
    def lockfile(slide: Box):
        slide.box(p_bottom=20).text('homu "lockfile"', T(color="white"))
        slide.box(width=1400).image("images/homu-lockfile.png")
        slide.box(x=450, y=585, width=400, height=350).rect(color="red", stroke_width=4)

    @slides.slide(bg_color=INTELLIJ_BG_COLOR)
    def homu_code_1(slide: Box):
        slide.box(width=1600).image("images/homu-code-1.png")

    @slides.slide(bg_color=INTELLIJ_BG_COLOR)
    def homu_code_2(slide: Box):
        slide.box(width=1600).image("images/homu-code-2.png")

    @slides.slide()
    def homu_issues(slide: Box):
        slide.box(p_bottom=100).text("homu issues", T(size=80))

        lst = unordered_list(slide.box())
        dimmed_list_items(lst, 2, [
            "Various unhandled GitHub race conditions",
            "Legacy GitHub integration (no GitHub app)",
            "Scary to (re)deploy",
            "No type hints",
            "(Almost) no tests",
        ], dim_last=True)
        lst.item(show="last+").text("We couldn't fully trust it", T(bold=True))

    @slides.slide(bg_color="#F6F6EF")
    def trust(slide: Box):
        """
        https://news.ycombinator.com/item?id=21586256
        """
        slide.box(width=1800).image("images/bors-hackernews.png")
        y = 525
        slide.box(x=0, y=0).line(((125, y), (195, y)), color="red", stroke_width=4)
        slide.box(x=0, y=0).line(((680, y), (1100, y)), color="red", stroke_width=4)
        y = 560
        slide.box(x=0, y=0).line(((990, y), (1400, y)), color="red", stroke_width=4)

    @slides.slide()
    def github_incident(slide: Box):
        """
        https://www.githubstatus.com/incidents/zsg1lk7w13cf
        """
        slide.box(width=1800).image("images/github-incident.png")
        y = 780
        slide.box(x=0, y=0).line(((1070, y), (1770, y)), color="red", stroke_width=4)
