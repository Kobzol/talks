from typing import Optional

from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG_COLOR, chapter, \
    iterate_grid


def porting_process(slides: Slides):
    @slides.slide()
    def deploying_bors(slide: Box):
        chapter(slide, "Shipping bors")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def tracking_issue(slide: Box):
        """
        https://github.com/rust-lang/infra-team/issues/168
        """
        slide.box(width=1800, p_bottom=50).image("images/bors-migration-tracking-issue-1.png")
        row = slide.box(horizontal=True, show="next+")

        width = 600
        for i in range(3, 6):
            row.box(width=width, y=0).image(f"images/bors-migration-tracking-issue-{i}.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def automate_repos(slide: Box):
        slide.box(width=1800).image("images/port-automate-repositories.png")

    # @slides.slide(bg_color=GITHUB_BG_COLOR)
    # def automate_repos_rust(slide: Box):
    #     slide.box(width=1400).image("images/port-rust-repository-team.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def move_repos_to_mq(slide: Box):
        slide.box(width=1300).image("images/port-reduce-bors-repositories.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def rust_lang_ci(slide: Box):
        slide.box(width=1600).image("images/port-rust-lang-ci.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_2_try(slide: Box):
        """
        Since October 2023.
        """
        slide.box(width=1400).image("images/port-bors2-try.png")
        slide.box(x="[90%]", y="[5%]").text("October 2023", T(color="white"))

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_arbitrary_try_builds(slide: Box):
        """
        https://rust-lang.zulipchat.com/#narrow/channel/242791-t-infra/topic/.E2.9C.94.20ci.20broken.3F/with/438529306
        """
        slide.box(width=1600).image("images/arbitrary-try-build-1.png")

    @slides.slide(bg_color="#1A1A1A")
    def bors_fail_1(slide: Box):
        slide.box(width=1600).image("images/bors-fail-1.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_fail_2(slide: Box):
        slide.box(width=1800).image("images/bors-fail-2.png")
        slide.box(x=0, y=0, show="next+").line([
            (1100, 150),
            (1200, 150),
            (1200, 900),
            (1100, 900),
        ], color="red", stroke_width=8)
        slide.box(x=1250, y=470, show="last+").text("~30 minutes", escape_char="#",
                                                    style=T(color="red"))
        slide.box(x=685, y=840, width=150, height=40).rect(bg_color=GITHUB_BG_COLOR)

    # @slides.slide(bg_color="#1A1A1A")
    # def bors_fail_3(slide: Box):
    #     slide.box(width=1600).image("images/bors-fail-3.png")

    # @slides.slide(bg_color=GITHUB_BG_COLOR)
    # def bors_fail_4(slide: Box):
    #     slide.box(width=1600).image("images/arbitrary-try-build-2.png")

    @slides.slide(bg_color="#1A1A1A")
    def port_new_bors_try_build_default(slide: Box):
        """
        Since July 2025.
        https://rust-lang.zulipchat.com/#narrow/channel/242791-t-infra/topic/Migrating.20bors.20try.20to.20new.20bors/with/530118648
        https://github.com/rust-lang/bors/pull/352
        """
        slide.box(width=1800).image("images/port-new-bors-try-build-default.png")
        slide.box(x="[90%]", y="[5%]").text("July 2025", T(color="white"))

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_disable_try_builds(slide: Box):
        """
        https://github.com/rust-lang/homu/pull/236
        Very sophisticated method to disable try builds in homu.
        """
        slide.box(width=1800).image("images/homu-disable-try-builds.png")

    @slides.slide(bg_color="#181A1B")
    def bors_gsoc(slide: Box):
        """
        https://blog.rust-lang.org/2025/11/18/gsoc-2025-results/#implement-merge-functionality-in-bors
        """
        slide.box(width=1600).image("images/bors-gsoc.png")
        slide.box(x="[95%]", y="[10%]", width=300).image("images/gsoc-logo.svg")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def christmas_sprint(slide: Box):
        slide.box(width=1200).image("images/christmas-sprint.png")
        slide.box(x=1200, y=440, width=150, height=400).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def pause_resume(slide: Box):
        """
        https://github.com/rust-lang/bors/pull/529
        """
        slide.box(width=1600).image("images/bors-pause-resume.png")

    def render_switch(
            command: Optional[str],
            bors_active: bool = True,
            homu_active: bool = True,
            bors_cmd_active: bool = True,
            homu_cmd_active: bool = True
    ):
        def get_color(active: bool) -> str:
            if active:
                return "black"
            return "#CCCCCC"

        def bot(parent: Box, name: str, active: bool) -> Box:
            text = name if active else f"{name}\n(inactive)"
            box = parent.box(y=0, width=300)
            box.text(text, T(opacity=1 if active else 0.4))
            return box

        slide = slides.new_slide()
        top = slide.box()
        if command is not None:
            top.text(command, "tt")

        offset_y = 150
        splitter = (top.x("50%"), top.y("100%").add(offset_y))
        slide.box().line((
            (top.x("50%"), top.y("100%").add(10)),
            splitter
        ), color="black", stroke_width=8)

        slide.box(height=300)
        row = slide.box(horizontal=True, height=200)
        bors = bot(row, "bors", bors_active)
        row.box(width=300)
        homu = bot(row, "homu", homu_active)

        arrow = Arrow(size=40)
        if bors_cmd_active:
            slide.box().line((
                (splitter[0], splitter[1]),
                (bors.x("50%"), splitter[1]),
                (bors.x("50%"), splitter[1].add(offset_y))
            ), color=get_color(bors_cmd_active), stroke_width=8, end_arrow=arrow)
        if homu_cmd_active:
            slide.box().line((
                (splitter[0], splitter[1]),
                (homu.x("50%"), splitter[1]),
                (homu.x("50%"), splitter[1].add(offset_y))
            ), color=get_color(homu_cmd_active), stroke_width=8, end_arrow=arrow)

    # render_switch(command="<command>")
    # render_switch(command="@bors2 pause", homu_cmd_active=False)
    # render_switch(command="@bors2 pause", homu_cmd_active=False, bors_active=False)
    # render_switch(command="@bors treeclosed=1000", bors_active=False)
    # render_switch(command="@bors treeclosed=1000", bors_active=False, homu_active=False)
    # render_switch(command="@bors2 resume", bors_active=False, homu_active=False,
    #               homu_cmd_active=False)
    # render_switch(command="@bors2 resume", homu_active=False, homu_cmd_active=False)

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_homu_compat(slide: Box):
        width = 1800
        slide.box(width=width, x="[50%]", y=300, show="1").image("images/bors-homu-compat-1.png")
        slide.box(width=width, x="[50%]", y=300, show="2").image("images/bors-homu-compat-2.png")
        slide.box(x=230, y=675, width=1350, height=100, show="last+").rect(
            color="red",
            stroke_width=8
        )

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def gh_statistics(slide: Box):
        slide.box(width=1600).image("images/kobzol-january-github-contributions.png")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_first_merged_pr(slide: Box):
        row = slide.box(horizontal=True, p_bottom=20)
        for _ in range(3):
            row.box(p_right=20).image("images/tada.svg")
        slide.box(width=1700, p_bottom=50).image("images/bors-first-merged-pr-header.png")
        slide.box(width=1700).image("images/bors-first-merged-pr.png")
        slide.box(x="[90%]", y="[5%]").text("January 2026", T(color="white"))

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def cleanup(slide: Box):
        slide.box(width=1600).image("images/bors-cleanup.png")

    @slides.slide(bg_color="#2E3436")
    def committer_email(slide: Box):
        """
        The bors@rust-lang.org e-mail address is load-bearing in a surprising amount of places
        There was a ~week where the e-mail address was wrong
        """
        slide.box(x=100, p_bottom=50).image("images/homu-merge-commit.png")
        slide.box(x=100, show="next+").image("images/bors-merge-commit.png")
        slide.box(x=90, y=230, width=600, height=45, show="next+").rect(color="red", stroke_width=8)
        slide.box(x=90, y=645, width=1300, height=45, show="last+").rect(
            color="red",
            stroke_width=8
        )

    @slides.slide()
    def hardcoded_email_meme(slide: Box):
        slide.box(width=900).image("images/hardcoded-email-meme.jpeg")

    @slides.slide(bg_color="#0D1117")
    def hardcoded_email(slide: Box):
        for i in range(1, 4):
            x = 100 if i == 1 else 65
            slide.box(x=x, width=1800, show=f"{i}+", p_bottom=20).image(
                f"images/bors-hardcoded-email-{i}.png"
            )
        slide.box(x=990, y=160, width=440, height=40).rect(color="red", stroke_width=4)
        slide.box(x=850, y=520, width=325, height=40, show="2+").rect(color="red", stroke_width=4)
        slide.box(x=640, y=900, width=340, height=40, show="3+").rect(color="red", stroke_width=4)

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_final_message(slide: Box):
        slide.box(width=1500, p_bottom=50).image("images/homu-final-message.png")
        slide.box(x=310, y=310, width=1200, height=120).rect(color="red", stroke_width=8)
        slide.box(width=1500).image("images/homu-archival.png")

    @slides.slide()
    def homu_legacy(slide: Box):
        """
        First PR merged by homu: https://github.com/rust-lang/rust/pull/21267 (19. 1. 2015)
        bd8a43c668ba93d29e9671c0c8dc6b67428bf492
        Last PR merged by homu: d9617c8d9a55773a96b61ba3a4acb107d65615c1 (7. 1. 2026)
        d9617c8d9a55773a96b61ba3a4acb107d65615c1
        First PR merged by new bors: https://github.com/rust-lang/rust/pull/150759 (7. 1. 2026)
        84c84421cc5cd8a416f58c77face28e79f6fac96
        git log bd8a43c668ba93d29e9671c0c8dc6b67428bf492..d9617c8d9a55773a96b61ba3a4acb107d65615c1 --oneline --merges --grep "Auto merge of #" | wc -l
        34786 merged PRs (2015 - 2026)

        Give a round of applause for homu!
        """
        slide.box(y=100).text("homu legacy", T(size=80))

        width = 1200
        slide.box(width=width).text("First PR:   #21267 (19. 1. 2015) - ~tt{bd8a43c6}",
                                    T(align="left"))
        slide.box(width=width, p_bottom=100, show="next+").text(
            "Last PR: #150310 (7. 1. 2026) - ~tt{d9617c8d}", T(align="left"))

        slide.box(p_bottom=20, show="next+").text("~tt{rust-lang/rust} and subtrees:")

        width = 300
        height = 50
        wrapper = slide.box(width=800, x="[50%]")
        cells = iterate_grid(3, 2, width=width, height=height, p_horizontal=50, p_vertical=10)
        items = ("34786", "merges", "38592", "PRs rolled up", "277779", "merged commits")
        for (index, (item, (row, col))) in enumerate(zip(items, cells)):
            step = f"{3 + index // 2}+"
            align = "left"
            style = "default"
            if index % 2 == 0:
                align = "right"
                style = "tt"

            wrapper.box(
                show=step, x=col, y=row, width=width, height=height
            ).text(
                item,
                slides.get_style(style).compose(T(align=align))
            )

    @slides.slide()
    def bors_result(slide: Box):
        slide.box(p_bottom=40).text("Result?")
        slide.box(show="next+", p_bottom=40).text("It just works!", T(bold=True))
        slide.box(show="next+").text("It became boring technology")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def github_uptime(slide: Box):
        """
        It just works, even though GitHub hasn't seen its best days recently.
        """
        slide.box(width=1600).image("images/github-uptime.png")

    @slides.slide()
    def bors_queue(slide: Box):
        """
        Implemented nice to have features.
        """
        slide.box(width=1900).image("images/bors-queue-2.png")

    # timeline = get_history_timeline()
    #
    # def year_2023(box: Box):
    #     box.box().text("October 2023: @bors2 try")
    #
    # def year_2025(box: Box):
    #     box.box().text("July 2025: new bors used for all try builds")
    #
    # def year_2026(box: Box):
    #     box.box().text("January 2026: new bors replaced homu completely")
    #
    #     arrow = Arrow(size=30)
    #     size = 50
    #     x_offset = 50
    #
    #     end = 1900
    #     y_contributions = 280
    #     x_contributions = 1225
    #     box.box(x=0, y=0, show="next+").line((
    #         (x_contributions, 50),
    #         (x_contributions, y_contributions),
    #         (end, y_contributions)
    #     ), color="black", stroke_width=8, end_arrow=arrow)
    #     box.box(x=x_contributions + x_offset, y=y_contributions + 20, show="last+").text(
    #         "My Rust contributions",
    #         T(size=size))
    #
    #     y_bors = 150
    #     x_bors = 1375
    #     box.box(x=0, y=0, show="next+").line((
    #         (x_bors, 50),
    #         (x_bors, y_bors),
    #         (end, y_bors)
    #     ), color="black", stroke_width=8, end_arrow=arrow)
    #     box.box(x=x_bors + x_offset, y=y_bors + 20, show="last+").text("New bors lifetime",
    #                                                                    T(size=size))
    #
    # timeline.render_year(2023, year_2023)
    # timeline.render_year(2025, year_2025)
    # timeline.render_year(2026, year_2026)
