from typing import List, Optional

from elsie import Slides
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG_COLOR, Timeline, bors_impl, bors_impl_counter, chapter

HISTORY_TIMELINE: Optional[Timeline] = None


def get_history_timeline() -> Timeline:
    global HISTORY_TIMELINE

    assert HISTORY_TIMELINE is not None
    return HISTORY_TIMELINE


def history(slides: Slides):
    global HISTORY_TIMELINE

    @slides.slide()
    def what_is_bors(slide: Box):
        chapter(slide, "What is bors, anyway?")

    @slides.slide(bg_color="#2B2B2B")
    def bors_origin(slide: Box):
        """
        https://graydon2.dreamwidth.org/1597.html
        25 years ago Graydon was working on a complex project with many integration tests
        """
        slide.box(width=1500).image("images/graydon-blog.png")

    @slides.slide(bg_color="#2B2B2B")
    def not_rocket_science(slide: Box):
        slide.box(width=1700).image("images/graydon-not-rocket-science.png")

    success = "green"
    failure = "red"
    merged = "#8957E5"

    dim = 150
    c_x = 800
    base_y = 880
    x_offset = 200
    y_offset = 150

    def circle(slide: Box, x: int, y: int, text: str, color: str, border: str = "black",
               show: str = "1+",
               text_color: str = "white",
               border_dash: Optional[str] = None) -> Box:
        pr = slide.box(x=x, y=y, width=dim, height=dim, show=show)
        pr.ellipse(color=border, bg_color=color, stroke_width=6, stroke_dasharray=border_dash)
        pr.text(text, T(size=40, color=text_color, bold=True))
        return pr

    def arrow(slide: Box, src, dst, show: str = "1+", src_y="50%", dst_y="50%", z_level=-1):
        slide.fbox(x=0, y=0, show=show, z_level=z_level).line((
            (src.x("50%"), src.y(src_y)),
            (dst.x("50%"), dst.y(dst_y)),
        ), color="black", stroke_width=6)

    def commit(slide: Box, anchor: Box, message: str, show: str = "1+", anchor_left: bool = True):
        width = 500
        x = anchor.x("0%").add(-width) if anchor_left else anchor.x("100%").add(50)
        box = slide.box(x=x, y=anchor.y("0%"), height=60, show=show).rect(color="black",
                                                                          stroke_width=6)
        inner = box.box(p_y=10, p_x=30)
        inner.text(message, T(align="left", size=50))

    # @slides.slide()
    # def merge_conflicts(slide: Box):
    #     """
    #     https://bors.tech/essay/2017/02/02/pitch/index.html
    #     """
    #     main1 = circle(slide, c_x, base_y, "main", color=success)
    #
    #     pr1 = circle(slide, c_x - x_offset, base_y - y_offset, "PR #8", color=success, show="1-2")
    #     circle(slide, c_x - x_offset, base_y - y_offset, "PR #8", color=merged, show="3+")
    #     commit(slide, pr1, "Remove function\nfoo")
    #     arrow(slide, main1, pr1, show="1+")
    #
    #     pr2 = circle(slide, c_x + x_offset, base_y - y_offset, "PR #3", color=success, show="2-3")
    #     commit(slide, pr2, "Update function\nfoo", anchor_left=False, show="2-3")
    #     arrow(slide, main1, pr2, show="2-3")
    #
    #     main2 = circle(slide, c_x, base_y - int(y_offset * 2), "main", show="3+", color=success)
    #     arrow(slide, main1, main2, show="last+")
    #     arrow(slide, pr1, main2, show="last+")
    #
    #     pr2_merge_conflict = circle(slide, c_x + x_offset, base_y - int(y_offset * 3), "PR #3",
    #                                 color="white", border="red",
    #                                 text_color="black",
    #                                 border_dash="16", show="next+")
    #     commit(slide, pr2_merge_conflict, "Update function\nfoo", anchor_left=False, show="last+")
    #     arrow(slide, main2, pr2_merge_conflict, show="last+")
    #
    #     row = slide.box(y=50, show="last+").fbox(horizontal=True, p_bottom=10)
    #     row.box(p_right=30).text("Merge conflict", T(align="left", size=70))
    #     row.box(width=80).image("images/checkmark.png")

    @slides.slide()
    def semantic_conflicts(slide: Box):
        main1 = circle(slide, c_x, base_y, "main", color=success)

        pr1 = circle(slide, c_x - x_offset, base_y - y_offset, "PR #8", color=success, show="1-2")
        circle(slide, c_x - x_offset, base_y - y_offset, "PR #8", color=merged, show="3+")
        commit(slide, pr1, "Remove function\nfoo")
        arrow(slide, main1, pr1, show="1+")

        pr2 = circle(slide, c_x + x_offset, base_y - y_offset, "PR #5", color=success, show="2-3")
        commit(slide, pr2, "Add new usage of\nfunction foo", anchor_left=False, show="2-3")
        arrow(slide, main1, pr2, show="2-3")

        main2 = circle(slide, c_x, base_y - int(y_offset * 2), "main", show="3+", color=success)
        arrow(slide, main1, main2, show="last+")
        arrow(slide, pr1, main2, show="last+")

        pr2_rebased = circle(slide, c_x + x_offset, base_y - int(y_offset * 3), "PR #5",
                             color="white", text_color="black",
                             border=success, show="next+", border_dash="16")
        commit(slide, pr2_rebased, "Add new usage of\nfunction foo", anchor_left=False,
               show="last+")
        arrow(slide, main2, pr2_rebased, show="last+")

        main3 = circle(slide, c_x, base_y - int(y_offset * 4), "main", show="next+", color=failure)
        arrow(slide, main2, main3, show="last+")
        arrow(slide, pr2_rebased, main3, show="last+")

        # row = slide.box(y=50, show="last+").fbox(horizontal=True, p_bottom=10)
        # row.box(p_right=30).text("Semantic conflict", T(align="left", size=70))
        # row.box(width=80).image("images/cross.png")

    # @slides.slide(bg_color=GITHUB_BG_COLOR)
    # def pr_up_to_date(slide: Box):
    #     """
    #     Manually rebase every PR before merging, which is as annoying as it sounds.
    #     """
    #     slide.box(width=1700).image("images/pr-up-to-date.png")

    @slides.slide()
    def bors(slide: Box):
        slide.set_style("green", T(color=success))

        slide.box().text("bors", T(size=80))
        slide.box().text("=", T(size=80))
        slide.box().text("(GitHub) bot that automates merging PRs")
        slide.box().text("so that ~tt{main} stays ~green{green}")

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def homu_first_approval(slide: Box):
        slide.box(width=1700).image("images/homu-first-approval.png")

    @slides.slide()
    def how_bors_works(slide: Box):
        slide.box(y=100).text("Bors PR queue", T(size=80))

        width = 800
        row = slide.box(x=700, width=width, height=120, horizontal=True)
        row.rect(color="black", stroke_width=4)

        boxes: List[Box] = []
        box_count = 5
        for item in range(box_count):
            pr_box = row.box(height="100%", width=width / box_count)
            pr_box.rect(color="black", stroke_width=4)
            boxes.append(pr_box)

        def draw(index: int, pr: int, show: str, testing: bool = False):
            box = boxes[index]
            inner = box.overlay(show=show)
            if testing:
                inner.rect(bg_color="white", color="black", stroke_width=8, stroke_dasharray="8")

            inner.box(padding=15).text(f"#{pr}")

        def draw_prs(prs: List[int], show: str, testing: bool = False):
            for i in range(len(prs)):
                draw(i, prs[i], show=show, testing=testing and i == 0)

        offset_y = 150

        main = circle(slide, 200, 850, "main", color=success)

        prs = [1, 8, 3, 14, 28]
        for (i, pr) in enumerate(prs):
            draw(i, pr, "1")

        test_x = main.x("100%").add(100)
        test_y = main.y("0").add(-offset_y)

        # merge first PR
        draw_prs(prs, show="2", testing=True)
        pr1 = circle(slide, test_x, test_y, f"#{prs[0]}", color="white", text_color="black",
                     show="2", border_dash="8")
        pr1_success = circle(slide, test_x, test_y, f"#{prs[0]}", color=success, show="3+")
        arrow(slide, main, pr1, show="2+")
        main2 = circle(slide, main.x("0"), main.y("0").add(-offset_y * 2), "main", color=success,
                       show="3+")
        arrow(slide, main, main2, show="last+")
        arrow(slide, pr1_success, main2, show="last+")
        draw_prs(prs[1:], show="last")

        # fail second PR
        draw_prs(prs[1:], show="4", testing=True)
        pr2 = circle(slide, test_x, test_y.add(-offset_y * 2), f"#{prs[1]}", color="white",
                     text_color="black", show="last", border_dash="8")
        arrow(slide, main2, pr2, show="last+")
        circle(slide, test_x, test_y.add(-offset_y * 2), f"#{prs[1]}", color=failure, show="next+")
        draw_prs(prs[2:], show="last")
        draw_prs(prs[2:], show="6", testing=True)
        pr3 = circle(slide, test_x, test_y.add(-offset_y * 3.5), f"#{prs[2]}", color="white",
                     text_color="black", show="last", border_dash="8")
        arrow(slide, main2, pr3, show="last+")

    # @slides.slide()
    # def bors_queue_webpage(slide: Box):
    #     slide.box(width=1800).image("images/bors-queue-1.png")

    timeline = Timeline(slides, start=2013, end=2026)
    HISTORY_TIMELINE = timeline

    def year_2013(box: Box):
        """
        https://github.com/graydon/bors

        Bors is both a concept and a specific implementation of it.
        As you can see below (spoiler alert), it was not the last bors implementation that saw the
        light of the day.
        """
        bors_impl(box, "graydon/bors", "February 2013", "python-logo.svg", "1.2k")
        bors_impl_counter(box)

    def year_2014(box: Box):
        """
        https://github.com/barosl/homu
        https://news.ycombinator.com/item?id=9206121
        https://internals.rust-lang.org/t/upcoming-automation-changes/1335
        """
        box.box(width=1800, show="1").image("images/homu-announcement-2.png")
        box.box(x=125, y=405, width=960, height=50, show="1").rect(color="red", stroke_width=8)
        bors_impl(box.box(x="[50%]", y="[20%]", show="next+"), "barosl/homu", "December 2014",
                  "python-logo.svg", "1.8k")
        bors_impl_counter(box)

        lst = unordered_list(box.box(y="[70%]"))
        lst.item(show="next+").text("Stateful")
        lst.item(show="next+").text("Try builds")
        lst.item(show="next+").text("Rollups")

    def year_2015(box: Box):
        """
        https://github.com/servo/homu
        https://github.com/rust-lang/homu

        Everyone seems to want to customize bors to fit their development methods.
        Homu is an implementation of bors.
        """
        row = box.box(horizontal=True)
        bors_impl(row.box(p_right=50), "servo/homu", "December 2015", "python-logo.svg", "3.4k")
        bors_impl_counter(box, show="1")
        bors_impl(row.box(show="next+"), "rust-lang/homu", "December 2015", "python-logo.svg",
                  "4.4k", stroke_width=8)
        bors_impl_counter(box, show="2")

    timeline.render_year(2013, year_2013)
    timeline.render_year(2014, year_2014)
    timeline.render_year(2015, year_2015)

    # rust-community/homu
    # AelitaBot/aelita
