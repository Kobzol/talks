from typing import List, Optional

from elsie import Slides
from elsie.boxtree.box import Box
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG, INTELLIJ_BG, REVIEW_ICON, bors_tag, chapter, code, crater_tag, \
    migration, quotation, \
    render_tag, \
    rustc_perf_tag, triagebot_config_tag, triagebot_tag


def pr_experience(slides: Slides):
    chapter_name = "Pull request experience"

    @slides.slide()
    def opening_a_pr(slide: Box):
        chapter(slide, chapter_name, REVIEW_ICON, sub="Meeting your reviewer")

    @slides.slide(bg_color=GITHUB_BG)
    def opening_a_pr(slide: Box):
        slide.box(width=1800).image("images/first-pr.png")

    @slides.slide(bg_color=GITHUB_BG)
    def assignment(slide: Box):
        """
        There is a lot to unpack here.
        """
        triagebot_tag(slide)
        slide.box(width=1600).image("images/triagebot-first-message-1.png")
        slide.fbox(x=250, y=170, width=1000, height=80, show="next+").rect(color="red",
                                                                           stroke_width=8)

    @slides.slide(bg_color=INTELLIJ_BG)
    def triagebot_autolabel(slide: Box):
        triagebot_config_tag(slide)
        slide.box(width=800, x=100).image("images/triagebot-autolabel.png")

    @slides.slide(bg_color="#161923")
    def triage_pr_status(slide: Box):
        render_tag(slide, "Forge", kind="docs")
        slide.box(width=1500, x=300).image("images/triage-pr-status.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rustbot_author(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1700).image("images/triagebot-author.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rustbot_ready(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1700).image("images/triagebot-ready.png")

    @slides.slide(bg_color=GITHUB_BG)
    def assignment_2(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1500, y=120).image("images/triagebot-first-message-2.png")
        slide.fbox(x=220, y=220, width=1500, height=800).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=INTELLIJ_BG)
    def triagebot_assign(slide: Box):
        triagebot_config_tag(slide)
        slide.box(width=1700, x=100).image("images/triagebot-assign-owners.png")

    @slides.slide(bg_color="#2C2A26")
    def triagebot_review_stats(slide: Box):
        """
        Integration with Zulip.
        """
        slide.box(width=1200).image("images/triagebot-review-stats.png")
        slide.box(width=340, height=230, x=480, y=390).rect(bg_color="red")
        slide.box(width=380, height=85, x=480, y=750).rect(bg_color="red")
        slide.box(width=380, height=40, x=480, y=970).rect(bg_color="red")

    @slides.slide(bg_color=GITHUB_BG)
    def team_db(slide: Box):
        render_tag(slide, "team", kind="config")

        slide.box(p_bottom=40).text("~link{https://github.com/rust-lang/team}", T(color="white"))
        slide.box(width=1600).image("images/team-automation.png")

    @slides.slide(bg_color="#1E1F22")
    def team_db_infra_team(slide: Box):
        render_tag(slide, "team", kind="config")
        slide.box(width=1600).image("images/team-db-infra.png")

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_warnings(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1800).image("images/triagebot-warnings.png")
        slide.box(width=1180, height=140, x=230, y=340, show="1").rect(color="red", stroke_width=8)
        slide.box(width=1540, height=200, x=230, y=480, show="next").rect(color="red",
                                                                          stroke_width=8)
        slide.box(width=700, height=150, x=230, y=680, show="next").rect(color="red",
                                                                         stroke_width=8)

    @slides.slide()
    def dealing_with_github(slide: Box):
        chapter(slide, chapter_name, REVIEW_ICON, sub="Dealing with GitHub's quirks")

    @slides.slide(bg_color=GITHUB_BG)
    def load_more_comments(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1200).image("images/rfc-load-more-comments.png")

    @slides.slide(bg_color=GITHUB_BG)
    def view_more_comments_link(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1800).image("images/triagebot-view-all-comments-link.png")
        slide.box(x=200, y=510, width=210, height=60).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_comment_viewer(slide: Box):
        """
        Comment viewer
        https://triagebot.infra.rust-lang.org/gh-comments/rust-lang/rfcs/pull/3955

        Loads much faster than GitHub, works even when GitHub is down (but its API still works),
        allows expanding all comments and threads and has a thread viewer.
        """
        triagebot_tag(slide)
        slide.box(p_bottom=40).text("Triagebot comment viewer", T(color="white"))
        slide.box(width=1700).image("images/triagebot-comment-viewer.png")

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_range_diff_link(slide: Box):
        triagebot_tag(slide, show="3+")
        slide.box(width=1800).image("images/triagebot-range-diff-link.png")
        slide.box(x=90, y=500, width=1700, height=400, show="1").rect(bg_color=GITHUB_BG)
        slide.box(width=1800, x="[50%]", y="[50%]", show="2").image(
            "images/github-compare-changes.png")
        slide.box(x=70, y=400, width=800, height=60, show="2").rect(color="red", stroke_width=8)

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_range_diff(slide: Box):
        """
        Diff viewer
        https://triagebot.infra.rust-lang.org/gh-range-diff/rust-lang/rust/5ea817c65e4896167300b7d2550781b98da9901a..c240b2b37c4ea30ca305d592ba87015b01e5e921/042c759f774872cf2f94c6685ce87e24c046c722..08cf89c12179a07534ed23dcd7fd8dd97f6f9632
        """
        triagebot_tag(slide)
        slide.box(p_bottom=40).text("Triagebot (range-)diff viewer", T(color="white"))
        slide.box(width=1300).image("images/triagebot-range-diff.png")

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_view_changes_since_this_review(slide: Box):
        triagebot_tag(slide)
        slide.box(width=1800, y=150).image("images/triagebot-view-changes-since-this-review.png")
        slide.box(x=220, y=850, width=420, height=60).rect(color="red", stroke_width=8)

    @slides.slide(bg_color=GITHUB_BG)
    def rust_log_analyzer(slide: Box):
        render_tag(slide, "rust-log-analyzer")
        slide.box(width=1800).image("images/rla-expanded.png")

    @slides.slide(bg_color="#010409")
    def github_actions_web_log(slide: Box):
        slide.box(width=1800).image("images/github-web-log.png")
        slide.box(x=100, y=700).text("???", T(color="red", bold=True))

    @slides.slide(bg_color="#010409")
    def github_actions_plain_log(slide: Box):
        slide.box(width=1800).image("images/github-plain-log.png")

    @slides.slide(bg_color=GITHUB_BG)
    def triagebot_log_viewer(slide: Box):
        """
        Log viewer
        https://triage.rust-lang.org/gha-logs/rust-lang/rust/79499390709
        """
        triagebot_tag(slide)
        slide.box(p_bottom=40).text("Triagebot log viewer", T(color="white"))
        slide.box(width=1800).image("images/triagebot-log-viewer.png")

    @slides.slide()
    def benchmarking(slide: Box):
        chapter(slide, chapter_name, REVIEW_ICON, sub="Running benchmarks")

    @slides.slide()
    def rustc_perf_dashboard(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1800).image("images/rustc-perf-dashboard.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rustc_perf_request(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1600).image(f"images/rustc-perf-enqueue.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rustc_perf_build_finished(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1600).image(f"images/rustc-perf-try-build-completed.png")

    @slides.slide()
    def rustc_perf_queue(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1600).image(f"images/rustc-perf-queue.png")

    @slides.slide(bg_color=GITHUB_BG)
    def rustc_perf_result_table(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1200).image(f"images/rustc-perf-result-table.png")

    @slides.slide()
    def rustc_perf_compare(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1600).image(f"images/rustc-perf-compare.png")

    @slides.slide()
    def rustc_perf_compare_details(slide: Box):
        rustc_perf_tag(slide)
        slide.box(width=1400, x=400).image(f"images/rustc-perf-compare-details.png")

    @slides.slide()
    def checking_backwards_compatibility(slide: Box):
        chapter(slide, chapter_name, REVIEW_ICON, sub="Checking backwards compatibility")

    @slides.slide()
    def crater(slide: Box):
        """
        Enables things like the new trait solver or the never type stabilization
        """
        slide.box(p_bottom=40).text("Crater", T(size=80))
        slide.box().text("For every stable release (or on-demand):")
        slide.box(show="next+").text(
            "test ~all Rust code on GitHub and crates.io (~600k Rust crates)", escape_char="#")

    @slides.slide(bg_color=GITHUB_BG)
    def crater_request(slide: Box):
        crater_tag(slide)
        slide.box(width=1300, show="1-3").image(f"images/crater-1.png")
        slide.box(x=320, y=260, width=1300, height=800, show="1").rect(bg_color=GITHUB_BG)
        slide.box(x=320, y=680, width=1300, height=380, show="2").rect(bg_color=GITHUB_BG)

    @slides.slide(bg_color=GITHUB_BG)
    def crater_result(slide: Box):
        crater_tag(slide)
        slide.box(width=1300).image(f"images/crater-2.png")

    @slides.slide(bg_color=GITHUB_BG)
    def crater_pr(slide: Box):
        crater_tag(slide)
        slide.box(width=1300).image(f"images/crater-3.png")

    @slides.slide(bg_color=GITHUB_BG)
    def crater_pr_list(slide: Box):
        crater_tag(slide)
        slide.box(width=1100).image(f"images/crater-4.png")

    @slides.slide()
    def merge_queue(slide: Box):
        chapter(slide, chapter_name, REVIEW_ICON, sub="Merge queue")

    @slides.slide()
    def no_rocket_science(slide: Box):
        quotation(slide.box(), """
~bold{The Not Rocket Science Rule Of Software Engineering:}
Automatically maintain a repository of code that always passes all the tests.
""", "Graydon Hoare (creator of Rust)", size=50)

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

    # @slides.slide(bg_color=GITHUB_BG)
    # def pr_up_to_date(slide: Box):
    #     """
    #     Manually rebase every PR before merging, which is as annoying as it sounds.
    #     """
    #     slide.box(width=1700).image("images/pr-up-to-date.png")

    @slides.slide()
    def bors(slide: Box):
        slide.set_style("green", T(color=success))

        slide.box(p_bottom=40).text("bors", T(size=80))
        slide.box().text("(GitHub) bot that automates merging PRs")
        slide.box().text("so that ~tt{main} stays ~green{green}")

    @slides.slide()
    def how_bors_works(slide: Box):
        bors_tag(slide)
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

    @slides.slide()
    def bors_queue(slide: Box):
        bors_tag(slide)
        slide.box(width=1800).image("images/bors-queue-1.png")

    @slides.slide(bg_color=GITHUB_BG)
    def bors_approve(slide: Box):
        bors_tag(slide)
        slide.box(width=1400).image("images/bors-approve.png")

    @slides.slide(bg_color="#1E1F22")
    def team_db_bors_permissions(slide: Box):
        render_tag(slide, "team", kind="config")
        slide.box(width=1600).image("images/team-db-infra.png")
        slide.box(x=260, y=660, width=360, height=220).rect(color="red", stroke_width=8)

    # @slides.slide(bg_color=GITHUB_BG)
    # def bors_delegate(slide: Box):
    #     bors_tag(slide)
    #     slide.box(width=1600).image("images/bors-delegate.png")

    def bors_impl(box: Box, name: str, date: str, icon: str, lines: str, stroke_width: int = 4):
        height = 50
        parent = box.box(width=700)
        radius = 20
        parent.rect(color="black", stroke_width=stroke_width, rx=radius, ry=radius)
        wrapper = parent.box(padding=50)

        def line(**kwargs) -> Box:
            return wrapper.box(width="100%", height=height, horizontal=True, **kwargs)

        namebox = line(p_bottom=40)
        namebox.box().text(name, "tt")

        langbox = line()
        langbox.box(width=100, p_right=100).image(f"images/{icon}")
        langbox.box().text(f"{lines} lines")

        parent.box(x="[3%]", y="[3%]").text(date, T(size=46))

    @slides.slide()
    def bors_implementations(slide: Box):
        migration(slide.box(p_bottom=40, show="4+"), ["python", "rust"])

        row = slide.box(horizontal=True)

        padding = 20
        bors_impl(row.box(), "graydon/bors", "2013", "python-logo.svg", "1.2k")
        row.box(padding=padding)
        bors_impl(row.box(show="2+"), "barosl/homu", "2014", "python-logo.svg", "1.8k")

        slide.box(height=padding * 2)
        row = slide.box(horizontal=True)
        bors_impl(row.box(show="3+"), "rust-lang/homu", "2015", "python-logo.svg", "4.4k")
        row.box(padding=padding)
        bors_impl(row.box(show="4+"), "rust-lang/bors", "2022", "rust-logo.png", "28.7k")

#     @slides.slide()
#     def final_bors_test(slide: Box):
#         slide.update_style("code", T(size=38))
#         code(slide.box(), """
# #[sqlx::test]
# async fn unapprove_lacking_permissions(pool: sqlx::PgPool) {
#     run_test(pool, async |ctx| {
#         ctx.approve(()).await?;
#         ctx.post_comment(Comment::from("@bors r-")
#             .with_author(User::unprivileged())
#         ).await?;
#         insta::assert_snapshot!(
#             ctx.get_next_comment_text(()).await?,
#             @"@unprivileged-user: :key:
#             Insufficient privileges: not in review users"
#         );
#
#         ctx
#             .get_pr(())
#             .await
#             .expect_approved_by(&User::default_pr_author().name);
#         Ok(())
#     })
#     .await;
# }
# """)

    @slides.slide(bg_color="#392B10")
    def rustweek_bors(slide: Box):
        slide.box(width=1700).image("images/rustweek-bors-talk.png")
