from typing import Optional

from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.text.textstyle import TextStyle as T
from elsie.ext import ordered_list, unordered_list

from utils import DESIGN_ICON, ZULIP_BG, code, dimmed_list_item, quotation, render_tag, chapter, \
    triagebot_tag


def proposal(slides: Slides):
    # @slides.slide()
    # def discussing_the_design(slide: Box):
    #     chapter(slide, "Discussing the design", DESIGN_ICON)

    @slides.slide(bg_color=ZULIP_BG)
    def zulip(slide: Box):
        """
        Web-public, doesn't require login.
        """
        slide.box(p_bottom=40).text("~tt{https://rust-lang.zulipchat.com}", T(color="white"))
        slide.box(width=1600).image("images/zulip-channels.png")

    @slides.slide(bg_color="#1C1C1C")
    def zulip_meetings(slide: Box):
        slide.box(width=1100, y=160, show="1").image("images/zulip-meetings.png")
        slide.box(width=1600, y=160, show="2").image("images/zulip-design-read.png")
        triagebot_tag(slide)

    @slides.slide()
    def how_to_change_something_in_rust(slide: Box):
        """
        You're not going to write an RFC to fix a typo in the documentation.
        """
        slide.update_style("default", T(size=50))
        slide.box(p_bottom=80).text("What discussions need to happen?", T(size=80))

        items = [
            '"Simple" change => ask on Zulip, send a pull request',
            "Stdlib API change => ACP (API Change Proposal)",
            "Compiler changes => MCP (Major Change Proposal)",
            "Language/governance change => RFC (Request for Comments)"
        ]

        lst = unordered_list(slide.box())
        for (index, item) in enumerate(items):
            dimmed_list_item(lst, item, last=item == items[-1], show=index + 2)

    @slides.slide()
    def rfc_process(slide: Box):
        slide.set_style("small", T(size=50))
        slide.box(p_bottom=20).text("Rust RFC process", T(bold=True))

        quotation(slide.box(p_top=50, show="next+"), """The “RFC” (request for comments) process is intended to provide a consistent
and controlled path for new features to enter the language and standard libraries,
so that all stakeholders can be confident about the direction the language is evolving in.""", "Rust RFC#2", size=40)

        lst = unordered_list(slide.box(p_top=40))
        lst.item(show="next+").text("Technical (e.g. new language features)", "small")
        lst.item(show="next+").text("Non-technical (e.g. changes to governance)", "small")
        lst.item(show="next+").text("\"One-way door\" decisions", "small")

    def rfc_header(slide: Box, text: str, step: Optional[int]) -> Box:
        row = slide.box(y=50, horizontal=True)
        text = f"RFC step {step}: {text}" if step is not None else text
        row.box().text(text, T(size=70))
        return row

    @slides.slide()
    def rfc_0(slide: Box):
        rfc_header(slide, "Vibe-check", step=0)
        slide.box(width=1600).image("images/rfc-step-0.png")

    @slides.slide()
    def rfc_1(slide: Box):
        # Backwards compatibility
        rfc_header(slide, "Write the RFC", step=1)
        lst = ordered_list(slide.box())

        parts = [
            "Motivation",
            "Guide-level explanation (how to teach this?)",
            "Reference-level explanation",
            "Drawbacks",
            "Rationale and alternatives",
            "Prior art",
            "Unresolved questions",
            "Future possibilities"
        ]
        for (step, part) in enumerate(parts, start=2):
            dimmed_list_item(lst, part, show=step, last=part == parts[-1])

    @slides.slide()
    def rfc_2(slide: Box):
        rfc_header(slide, "Propose the RFC with a PR", step=2)
        slide.box(width=1300).image("images/rfc-step-2.png")

    @slides.slide()
    def rfc_3(slide: Box):
        rfc_header(slide, "Receive (a LOT of) comments", step=3)

        wrapper = slide.box(x="[50%]")
        for i in range(1, 4):
            wrapper.box(width=600, x=i*50, show=f"{1+i}-{4}").image(f"images/rfc-comment-count-{i}.png")
        # slide.box(show="next", x="[50%]", y="[50%]", width=1700).image("images/rfc-load-more-comments.png")

        for i in range(1, 4):
            slide.box(show="next", x="[50%]", y="[50%]", width=1700).image(f"images/rfc-comment-{i}.png")

    @slides.slide()
    def rfc_4(slide: Box):
        rfc_header(slide, "Integrate feedback & repeat", step=4)
        slide.box(width=1600).image("images/rfc-step-4.png")

    @slides.slide()
    def rfc_5(slide: Box):
        rfc_header(slide, "Vote", step=5)
        slide.box(width=1000, x="[50%]", y="[50%]", show="1").image("images/rfc-fcp-1.png")
        slide.box(width=1700, x="[50%]", y=170, show="next+").image("images/rfc-fcp-2.png")
        render_tag(slide, "rfcbot")

    @slides.slide()
    def rfcbot_second_account(slide: Box):
        render_tag(slide, "rfcbot")
        slide.box(width=1700, x="[50%]", y=170).image("images/rfcbot-second-account.png")

    @slides.slide(bg_color="#1C1C1C")
    def rfcbot_overflow_1(slide: Box):
        render_tag(slide, "rfcbot")
        slide.box(width=1700).image("images/rfcbot-overflow-1.png")

    @slides.slide(bg_color="#1C1C1C")
    def rfcbot_overflow_2(slide: Box):
        render_tag(slide, "rfcbot")
        slide.box(width=1700).image("images/rfcbot-overflow-2.png")

    @slides.slide()
    def consensus(slide: Box):
        render_tag(slide, "rfcbot")
        rfc_header(slide, "Achieving consensus", step=None)

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("At most two votes missing")
        lst.item(show="next+").text("No concerns")
        slide.box(width=1700, p_top=50, show="last+").image("images/rfc-concern.png")

    @slides.slide()
    def rfc_6(slide: Box):
        render_tag(slide, "rfcbot")
        rfc_header(slide, "FCP (Final Comment Period)", step=6)
        slide.box(width=1700).image("images/rfc-step-6.png")

        lst = unordered_list(slide.box(p_top=50))
        lst.item(show="next+").text("Lasts for 10 days")
        lst.item(show="next+").text("Last chance for someone to object")
        lst.item(show="next+").text("Announced in various communication channels")

    @slides.slide()
    def rfc_7(slide: Box):
        render_tag(slide, "rfcbot")
        row = rfc_header(slide, "RFC done", step=7)
        row.box(p_left=50, width=150).image("images/tada.png")
        slide.box(width=1600).image("images/rfc-step-7.png")
        slide.box(p_top=40, show="next+").text("(this can take months or even years)")
        slide.box(show="next+").text("Next step: (find someone to) implement it")

#     @slides.slide()
#     def when_things_go_wrong(slide: Box):
#         slide.box().text("Sometimes, making decisions is ~emph{hard}")
#
#     @slides.slide()
#     def great_int_debate(slide: Box):
#         content = slide.box()
#         content.box(p_bottom=40).text("Great int debate (2014)")
#         quotation(content.box(show="next+"),
#                   """We have been reading these threads and have also done a lot
# of internal experimentation, and we believe we’ve come to a final
# decision on the fate of integers in Rust.""",
#                   "Core team (2014)", size=56)
#
#     @slides.slide()
#     def no_new_rationale(slide: Box):
#         """
#         https://aturon.github.io/tech/2018/05/25/listening-part-1/
#         """
#         content = slide.box()
#         content.box(p_bottom=40).text("\"No new rationale\" rule")
#         quotation(content.box(),
#                   """Decisions must be made only on the basis of rationale
#       already debated in public (to a steady state).""")
#
#     @slides.slide()
#     def await_syntax(slide: Box):
#         """
#         https://boats.gitlab.io/blog/post/await-decision/
#         https://boats.gitlab.io/blog/post/await-decision-ii/
#         """
#         slide.update_style("code", style=T(size=70))
#         content = slide.box()
#         content.box(p_bottom=40).text("~tt{Await}ing a solution (2018/2019)")
#         codebox = code(slide.box(show="next+", x=400), """
# await!(fut);
# await fut;
# await { fut };
# fut.await;
# fut.await();
# fut.await!;
# fut@await;
# """, return_codebox=True)
#         line = codebox.line_box(1)
#         slide.box(show="next+").line(
#             [(line.x("100%").add(50), line.y("50%")),
#              (line.x("75%"), line.y("50%"))],
#             stroke_width=20,
#             color="blue",
#             end_arrow=Arrow(size=30)
#         )
#         slide.box(x=line.x("100%").add(80), y=line.y(0), show="last+").text("Rust community wanted this")
#
#         line = codebox.line_box(3)
#         slide.box(show="next+").line(
#             [(line.x("100%").add(50), line.y("50%")),
#              (line.x("75%"), line.y("50%"))],
#             stroke_width=20,
#             color="red",
#             end_arrow=Arrow(size=30)
#         )
#         slide.box(x=line.x("100%").add(80), y=line.y(0), show="last+").text("Lang team wanted this")
#
#     @slides.slide()
#     def await_discussion(slide: Box):
#         slide.box(width=1600).image("images/await-discussion.png")
#
#     @slides.slide()
#     def await_solution(slide: Box):
#         """
#         I was also wrong
#         """
#         canvas = slide.fbox()
#         canvas.overlay(show="1").box(width=1400).image("images/await-reaction-1.png")
#         canvas.overlay(show="1").line([
#             (350, 270),
#             (1130, 270)
#         ], color="red", stroke_width=14)
#         canvas.overlay(show="next").box(width=1000).image("images/await-reaction-2.png")
