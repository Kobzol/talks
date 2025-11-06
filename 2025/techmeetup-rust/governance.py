import os
from pathlib import Path
from typing import List, Optional

from PIL import Image
from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie import TextStyle as T
from elsie.boxtree.boxitem import BoxItem
from elsie.ext import ordered_list, unordered_list

from history import history
from utils import dimmed_list_item, render_bot, code, iterate_grid, quotation, topic


def governance(slides: Slides):
    @slides.slide()
    def what_is_governance(slide: Box):
        topic(slide.box(), "Governance", "lawyer.svg")
        slide.box(p_bottom=60, show="next+").text("…what's that?!")
        slide.box(show="next+").text("Decision-making process")
        box = slide.box(width=500, x=500)
        box.overlay(show="next").text("designed to evolve <something>")
        box.overlay(show="next+").text("designed to evolve <a programming language>")
        slide.box(show="next+", p_top=150).text("Have you ever tried to ~emph{change} your favourite programming language?", "small")

    def governance_title(slide: Box, text: str) -> BoxItem:
        return slide.box(y=100).text(text, T(size=70, bold=True))
    
    
    def governance_logos(parent: Box, logos: List[str], width=160) -> List[BoxItem]:
        offset = 100
        boxes = []
        for logo in logos:
            boxes.append(parent.box(width=width).image(logo))
            parent.box(width=offset)
        return boxes
    
    
    @slides.slide()
    def company_backed(slide: Box):
        governance_title(slide, "Company-backed")
    
        row = slide.box(horizontal=True)
        governance_logos(row, [
            "images/csharp-logo.svg",
            "images/typescript-logo.svg",
            "images/go-logo.svg",
        ])
        slide.box(show="next+", p_top=100).text("…get hired by Microsoft/Google (?)")
    
    
    @slides.slide()
    def committee(slide: Box):
        governance_title(slide, "Design by committee")
    
        # Famously/infamously
        # Similar to company owned, but it's multiple companies
        row = slide.box(horizontal=True)
        governance_logos(row, [
            "images/c-logo.svg",
            "images/cpp-logo.svg",
            "images/javascript-logo.png",
        ])
        slide.box(show="next+", p_top=100).text("(ISO) standardization process")
    
    @slides.slide()
    def iso_standardization_process(slide: Box):
        slide.box().text("C++ ISO standardization process (shortened version)")
    
        process = [
            "Get invited to a mailing list",
            "Request a paper number from a registrar by e-mail",
            "Write a paper with some proposal",
            "Address the paper to a study group",
            ["Submit the paper by e-mail before a deadline", "4-6 weeks before the next meeting, otherwise it will be discarded"],
            [
                "Ensure it is presented at a study group",
                "by attending a committee meeting",
                "or finding someone to present it",
            ],
            "Find a champion to support your paper",
            ["Attend a committee meeting",
             "as a guest, or",
             "by becoming an ISO National Body representative, or",
             "by joining on behalf of a company (1-10k $USD yearly fee)"
             ],
        ]
    
        lst_text_size = 50
        lst = ordered_list(slide.box())
        for item in process:
            if isinstance(item, list):
                lst.item(show="next+").text(item[0], T(size=lst_text_size))
                wrapper = lst.ul()
                for subitem in item[1:]:
                    wrapper.item().text(subitem, T(size=int(lst_text_size * 0.8)))
            else:
                lst.item(show="next+").text(item, T(size=lst_text_size))
        slide.box(show="next+", x=1300, y=475).text(
            "9. If the paper is decided to be worthy,\n"
            "it is moved along to a higher group",
            rotation=90
        )
        slide.box(show="next+", x=-350, y=460).text(
            "10. If there are concerns, resolve them\nand GOTO step 4",
            rotation=-90
        )
        slide.box(show="next+", x=1000, y=650).text("11. Wait ~3 years for the next C++", T(size=50), escape_char="#")
        slide.box(show="last+", x=1600, y=800).text("standard", rotation=90)
        slide.box(show="next+", x=700, y=870).text("12. Wait for implementation in a major compiler", T(size=45), escape_char="#")
    
    
    @slides.slide()
    def bdfl(slide: Box):
        box = governance_title(slide, "BDFL")
        box.box(y=100).text("(Benevolent Dictator For Life)")
    
        row = slide.box(horizontal=True)
        logos = governance_logos(row, [
            "images/ruby-logo.svg",
            "images/zig-logo.svg",
            "images/python-logo.svg",
        ])
        python = logos[2]
        slide.box(x=python.x("50%").add(-150), y=python.y("100%")).text("(1995-2018)")
    
        box = slide.box(show="next+", p_top=100).text("~#bribe{Bribe} Befriend the BDFL (?)")
        bribe = box.inline_box("#bribe")
        slide.box(show="last").line(
            [(bribe.x("0"), bribe.y("55%")),
             (bribe.x("100%"), bribe.y("55%"))]
        , color="black", stroke_width=6)

    @slides.slide()
    def open_source_rfc(slide: Box):
        governance_title(slide, "Open-source RFC process")
    
        row = slide.box(horizontal=True)
        logos = governance_logos(row, [
            "images/rust-logo.png",
            "images/php-logo.svg",
            "images/python-logo.svg",
        ], width=200)
        python = logos[2]
        slide.box(x=python.x("50%").add(-90), y=python.y("100%")).text("(2018+)")
    
        slide.box(show="next+", p_top=100).text("Propose changes with RFCs")
        slide.box(show="next+").text("Gain voting rights by contributing")

    @slides.slide()
    def rust_governance_history(slide: Box):
        slide.box().text("Evolution of Rust governance", T(size=80))

    history(slides)

    @slides.slide()
    def rust_teams(slide: Box):
        # Teams are independent
        slide.box(width=1500, show="1-2").image("images/rust-teams.png")
        slide.box(width=500, height=300, x=220, y=40, show="1").rect(bg_color="#2E2459")

    def get_rust_project_image_path() -> str:
        width = 65
        height = 65
        rows = 15
        cols = 26
        padding = 5
        images = sorted([f"avatars/{file}" for file in os.listdir("avatars")])
        assert rows * cols == len(images)

        def generate(path: Path):
            img = Image.new("RGBA", ((width + padding) * cols, (height + padding) * rows), "WHITE")
            white_bg = Image.new("RGBA", (width, height), "WHITE")
            for (image, (row, col)) in zip(images, iterate_grid(rows, cols, width, height, p_horizontal=padding, p_vertical=padding)):
                avatar = Image.open(image).resize((width, height)).convert("RGBA")
                avatar = Image.alpha_composite(white_bg, avatar)
                img.paste(avatar, (col, row))
            img.convert("RGBA").save(path)

        key = Path(f"images/w{width}-h{height}-r{rows}-c{cols}-p{padding}.png")
        if not key.is_file():
            generate(key)

        return str(key)

    @slides.slide()
    def rust_project_structure(slide: Box):
        # Working with people that I don't know personally
        # Rust Project: governance, maintenance, development, deployment
        # Rust Foundation: infrastructure, domains, legal, conferences, community, funding
        slide.box(show="1", x="[50%]", y=-100, width=2500).image("images/org-chart-1.png")
        box = slide.box(show="2+", x="[50%]", y=0, width=1800).image("images/org-chart-2.png")

        slide.box(show="next+", x=55, y=80, width=1800, height=500).rect(
            color="black",
            stroke_width=2,
            stroke_dasharray=8
        )
        project = slide.box(x=box.x("0%"), y=box.y("90%"), show="last+")
        project.fbox().text("Rust Project", T(align="left"))
        small = T(size=40, align="left")
        project.fbox().text("~300 people, ~100 teams", small, escape_char="#")
        slide.box(show="next", x="[50%]", y="[50%]", z_level=1).image(get_rust_project_image_path())
        project.fbox(show="next+").text("Development, maintenance, governance, …", small, escape_char="#")

        rf = slide.box(p_top=700, show="next+").image("images/rust-foundation-logo.png")
        arrow = Arrow(size=20)
        slide.box(show="last+").line((
            (box.x("50%"), box.y("100%").add(-60)),
            (rf.x("50%"), rf.y("0").add(-20))
        ), start_arrow=arrow, end_arrow=arrow, stroke_width=6)
        slide.box(show="last+").text("Legal, infra, domains, trademark, funding, …", small)

        contributors = slide.box(x=1200, y=800, show="next+").text("(Hundreds of) contributors", "small")
        slide.box(show="last+").line((
            (box.x("75%"), box.y("100%").add(-60)),
            (contributors.x("50%"), contributors.y("0").add(-20))
        ), start_arrow=arrow, end_arrow=arrow, stroke_width=6)

        slide.box(x="[98%]", y="[98%]").text("Source: Rust Org Chart by Eric Huss", T(size=30))

    @slides.slide()
    def team_db(slide: Box):
        header = slide.box(y=100)
        header.box(p_top=100).text("~link{https://github.com/rust-lang/team}")
        slide.box(y="[50%]", width=1600, show="1").image("images/team-automation.png")
        slide.box(show="next+", y=300, width=1600).image(
            "images/team-db-infra.png")
        render_bot(slide, "sync-team")

    @slides.slide()
    def zulip(slide: Box):
        """
        Web-public, doesn't require login.
        """
        slide.box(y=50).text("Zulip", T(bold=True))
        slide.box(width=1700, y=140).image("images/zulip-channels.png")

    @slides.slide()
    def zulip_meetings(slide: Box):
        slide.box(y=50).text("Async chat meetings", T(bold=True))
        slide.box(width=1100, y=160, show="1").image("images/zulip-meetings.png")
        slide.box(width=1600, y=160, show="2").image("images/zulip-design-read.png")
        render_bot(slide, "rustbot")

    @slides.slide()
    def how_to_change_something_in_rust(slide: Box):
        slide.box(p_bottom=80).text("How to change something in Rust?", T(bold=True))
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("\"Simple\" change => send a pull request")
        lst.item(show="next+").text("Complex change => write an RFC")

    @slides.slide()
    def rfc_process(slide: Box):
        slide.set_style("small", T(size=50))
        slide.box(p_bottom=20).text("Rust RFC process", T(bold=True))
        slide.box().text("(RFC = Request for Comments)")

        quotation(slide.box(p_top=50, show="next+"), """The “RFC” (request for comments) process is intended to provide a consistent
and controlled path for new features to enter the language and standard libraries,
so that all stakeholders can be confident about the direction the language is evolving in.""", "Rust RFC#2", size=40)

        lst = unordered_list(slide.box(p_top=40))
        lst.item(show="next+").text("Technical (e.g. new language features)", "small")
        lst.item(show="next+").text("Non-technical (e.g. changes to governance)", "small")
        lst.item(show="next+").text("\"One-way door\" decisions", "small")

    def rfc_header(slide: Box, text: str, step: Optional[int]) -> Box:
        row = slide.box(y=50, horizontal=True)
        text = f"Step {step}: {text}" if step is not None else text
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
        slide.box(show="next", x="[50%]", y="[50%]", width=1700).image("images/rfc-load-more-comments.png")

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
        render_bot(slide, "rfcbot")

    @slides.slide()
    def consensus(slide: Box):
        rfc_header(slide, "Consensus", step=None)

        lst = unordered_list(slide.box())
        lst.item(show="next+").text("At most two votes missing")
        lst.item(show="next+").text("No concerns")
        slide.box(width=1600, p_top=50, show="last+").image("images/rfc-concern.png")

        # quotation(slide.box(show="next+", x="[50%]", y="[50%]"),
        #           """Respect that people have differences of opinion and that every design
# or implementation choice carries a trade-off and numerous costs.
# There is seldom a right answer.""",
#                   "Rust Code of Conduct", size=50)

    @slides.slide()
    def rfc_6(slide: Box):
        rfc_header(slide, "FCP (Final Comment Period)", step=6)
        slide.box(width=1700).image("images/rfc-step-6.png")

        lst = unordered_list(slide.box(p_top=50))
        lst.item(show="next+").text("Lasts for 10 days")
        lst.item(show="next+").text("Last chance for someone to object")
        lst.item(show="next+").text("Announced in various communication channels")

    @slides.slide()
    def rfc_7(slide: Box):
        row = rfc_header(slide, "RFC done", step=7)
        row.box(p_left=50, width=150).image("images/tada.png")
        slide.box(width=1600).image("images/rfc-step-7.png")
        slide.box(p_top=40, show="next+").text("(this can take months or even years)")
        slide.box(show="next+").text("Next step: (find someone to) implement it")

    @slides.slide()
    def when_things_go_wrong(slide: Box):
        slide.box().text("Sometimes, making decisions is ~emph{hard}")

    @slides.slide()
    def great_int_debate(slide: Box):
        content = slide.box()
        content.box(p_bottom=40).text("Great int debate (2014)")
        quotation(content.box(show="next+"),
                  """We have been reading these threads and have also done a lot
of internal experimentation, and we believe we’ve come to a final
decision on the fate of integers in Rust.""",
                  "Core team (2014)", size=56)

    @slides.slide()
    def no_new_rationale(slide: Box):
        """
        https://aturon.github.io/tech/2018/05/25/listening-part-1/
        """
        content = slide.box()
        content.box(p_bottom=40).text("\"No new rationale\" rule")
        quotation(content.box(),
            """Decisions must be made only on the basis of rationale
already debated in public (to a steady state).""")

    @slides.slide()
    def await_syntax(slide: Box):
        """
        https://boats.gitlab.io/blog/post/await-decision/
        https://boats.gitlab.io/blog/post/await-decision-ii/
        """
        slide.update_style("code", style=T(size=70))
        content = slide.box()
        content.box(p_bottom=40).text("~tt{Await}ing a solution (2018/2019)")
        codebox = code(slide.box(show="next+", x=400), """
await!(fut);
await fut;
await { fut };
fut.await;
fut.await();
fut.await!;
fut@await;
""", return_codebox=True)
        line = codebox.line_box(1)
        slide.box(show="next+").line(
            [(line.x("100%").add(50), line.y("50%")),
             (line.x("75%"), line.y("50%"))],
            stroke_width=20,
            color="blue",
            end_arrow=Arrow(size=30)
        )
        slide.box(x=line.x("100%").add(80), y=line.y(0), show="last+").text("Rust community wanted this")

        line = codebox.line_box(3)
        slide.box(show="next+").line(
            [(line.x("100%").add(50), line.y("50%")),
            (line.x("75%"), line.y("50%"))],
            stroke_width=20,
            color="red",
            end_arrow=Arrow(size=30)
        )
        slide.box(x=line.x("100%").add(80), y=line.y(0), show="last+").text("Lang team wanted this")

    @slides.slide()
    def await_discussion(slide: Box):
        slide.box(width=1600).image("images/await-discussion.png")

    @slides.slide()
    def await_solution(slide: Box):
        """
        I was also wrong
        """
        canvas = slide.fbox()
        canvas.overlay(show="1").box(width=1400).image("images/await-reaction-1.png")
        canvas.overlay(show="1").line([
            (350, 270),
            (1130, 270)
        ], color="red", stroke_width=14)
        canvas.overlay(show="next").box(width=1000).image("images/await-reaction-2.png")

    @slides.slide()
    def its_hard(slide: Box):
        slide.box().text("Open-source (governance) is hard…", T(bold=True))

        lst = unordered_list(slide.box(p_top=60))
        lst.item(show="next+").text("Team-based decision-making")
        lst.item(show="next+").text("Bottom-up development")
        lst2 = lst.ul()
        lst2.item().text("Rust is NOT a company!", "small")
        lst.item(show="next+").text("With several hundreds of people")
        lst2 = lst.ul()
        lst2.item().text("Most of them unpaid volunteers", "small")
        lst.item(show="next+").text("Burnout, personal conflicts, lack of transparency, …")

        slide.box(show="next+", p_top=60).text("…but also fun & impactful!", T(bold=True))
