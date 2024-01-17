import math
from typing import Tuple

import elsie
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from history import history
from utils import LOWER_OPACITY, dimmed_list_item, \
    generate_qr_code, quotation, code

PRODUCTION_BUILD = True
SHOW_PRIVATE = False

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=60))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")


@slides.slide()
def intro(slide: Box):
    slide.box(p_bottom=sh(60), width=sw(300)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("Rust governance", style=T(bold=True))
    slide.box().text("Kuba Beránek", style=T(size=40))


def two_column_layout(parent: Box) -> Tuple[Box, Box]:
    row = parent.box(width="fill", horizontal=True)
    left = row.box(width=sw(1100))
    line = row.box(padding=40, width=sw(100), height=sh(500))
    line.fbox().rect(bg_color="black")
    right = row.box()
    return (left, right)


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=40))

    content = slide.box()
    (left, right) = two_column_layout(content)

    gh = right.box(horizontal=True, p_bottom=sh(20))
    gh.box(width=sw(80)).image("images/github-logo.png")
    gh.box(p_left=sw(40)).text("github.com/kobzol", style=T(size=50, bold=True))

    gh_qr = generate_qr_code("https://github.com/kobzol")
    right.box().image(gh_qr, image_type="png")

    left.box(x=0, p_bottom=sh(40)).text("Kuba Beránek", T(align="left", size=50, bold=True))
    lst = unordered_list(left.box(x=0))
    dimmed_list_item(lst, "PhD student, teacher @ VSB-TUO", show=2)
    dimmed_list_item(lst, "Researcher @ IT4Innovations", show=3)
    dimmed_list_item(lst, "HPC, distributed systems, code optimization,\nmachine learning,…",
                     show=4)
    lst.item(show="last").text("Rust user & contributor")


@slides.slide()
def teams(slide: Box):
    content = slide.box()
    height = 960
    reference = content.box(height=sh(height)).image("images/wg-perf.png")
    offset = 30

    # Link: https://www.rust-lang.org/governance/teams/infra
    # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Binary%20size%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Parallel%20rustc%20working%20group
    for (index, image) in enumerate((
            "wg-parallel-rustc",
            "wg-binary-size",
            "team-infra",
    )):
        content.box(
            show="next+",
            x=reference.x("0").add(offset * (index + 1)),
            y=reference.y("0").add(offset * (index + 1)),
            height=sh(height - (30 * (index - 1)))
        ).image(f"images/{image}.png")


@slides.slide()
def what_is_governance(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(60)).text("What is governance?", T(size=80, bold=True))
    content.box(show="next+").text("Decision-making process")
    content.box(show="next+").text("designed to evolve <X>")


@slides.slide()
def governance_types(slide: Box):
    """
    - being able to make (both important and unimportant) decisions, in a distributed fashion, quickly
    - be transparent and inclusive
    """
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Governance modes for languages", T(size=80))
    lst = unordered_list(content.box())
    dimmed_list_item(lst, "Company-backed - Kotlin, C#", show=2)
    dimmed_list_item(lst, "Design by committee - C, C++", show=3)
    dimmed_list_item(lst, "BDFL - ex-Python, Ruby",
                     show=4)
    lst.item(show="last").text("Open RFC process - Rust, Python")


@slides.slide()
def rust_history(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(80)).text("Rust governance history", T(size=80))


history(slides)


@slides.slide()
def governance_diagram(slide: Box):
    slide.update_style("default", T(size=sw(40)))
    content = slide.fbox()
    content.box(p_y=sw(20)).text("Rust governance diagram", style=T(size=sw(60)))
    canvas = content.fbox()

    def item(x: int, y: int, label: str) -> Box:
        box = canvas.box(x=sw(x), y=sw(y), show="next+")
        box.rect(color="black", stroke_width=4)
        box.box(padding=sw(20)).text(label)
        return box

    # Top level governance
    foundation = item(x=50, y=50, label="Rust foundation")
    foundation.box(width="fill").rect(color="black").box(padding=sw(20), show="next+").text(
        "Project directors", style=T(size=sw(30)))
    foundation.box(width="fill").rect(color="black").box(padding=sw(20),
                                                         show="next+").text(
        "Member directors", style=T(size=sw(30)))
    council = item(x=500, y=50, label="Leadership council")
    canvas.box(show="last+").line(points=[
        foundation.p("100%", "20%"),
        council.p("0", "50%")
    ], stroke_width=2)

    # Teams
    lang_team = item(x=500, y=250, label="Lang team")
    canvas.box(show="last+").line(points=[
        council.p("50%", "100%"),
        lang_team.p("50%", "0")
    ], stroke_width=2)
    compiler_team = item(x=800, y=250, label="Compiler team")
    canvas.box(show="last+").line(points=[
        council.p("50%", "100%"),
        compiler_team.p("50%", "0")
    ], stroke_width=2)
    other_teams = item(x=1180, y=250, label="8+ other teams")
    canvas.box(show="last+").line(points=[
        council.p("50%", "100%"),
        other_teams.p("50%", "0")
    ], stroke_width=2)

    # WGs
    wg_compiler_perf = item(x=500, y=500, label="Compiler performance WG")
    canvas.box(show="last+").line(points=[
        compiler_team.p("50%", "100%"),
        wg_compiler_perf.p("50%", "0")
    ], stroke_width=2)
    wg_llvm = item(x=1100, y=500, label="LLVM WG")
    canvas.box(show="last+").line(points=[
        compiler_team.p("50%", "100%"),
        wg_llvm.p("50%", "0")
    ], stroke_width=2)
    other_wgs = item(x=1400, y=500, label="Other WGs")
    canvas.box(show="last+").line(points=[
        compiler_team.p("50%", "100%"),
        other_wgs.p("50%", "0")
    ], stroke_width=2)
    canvas.box(show="next+", x=sw(400), y=sh(0), width=sw(1400), height=sh(800)).rect(
        color="black",
        stroke_width=2,
        stroke_dasharray=8
    )
    canvas.box(show="last+", x=sw(900), y=sh(700)).text('"Rust Project"', style=T(size=sw(60)))


@slides.slide()
def team_introspection(slide: Box):
    """
    https://www.rust-lang.org/governance
    """
    content = slide.box()
    content.box(width=sw(1500)).image("images/teams.png")


@slides.slide()
def team_stats(slide: Box):
    content = slide.box()
    content.box().text("140 teams")
    content.box(show="next+").text("46 working groups")
    content.box(show="next+").text("480+ team/WG members")


@slides.slide()
def team_automation(slide: Box):
    content = slide.fbox(p_top=sh(40))
    content.box(p_bottom=sh(20)).text("Automating team member permissions")
    content.box(p_bottom=sh(60)).text("~link{https://github.com/rust-lang/team}")
    canvas = content.fbox()
    canvas.box(y=0, width=sw(1600), show="next").image("images/team-automation.png")
    canvas.overlay().box(show="next", width=sw(1000)).image(
        "images/team-wg-compiler-performance.png")
    canvas.overlay().box(show="next+", width=sw(1000)).image("images/bors-approve.png")


@slides.slide()
def how_do_changes_happen(slide: Box):
    slide.update_style("default", style=T(size=sw(50)))
    content = slide.box()
    content.box(p_bottom=sh(40)).text("How do changes happen?", style=T(size=sw(60)))
    lst = unordered_list(content.box())
    lst.item(show="next+").text("MCP (Major Change Proposal)")
    lst.item(show="next+").text("ACP (API Change Proposal)")
    lst.item(show="next+").text("FCP (Final Comments Period)")
    lst.item(show="next+").text("~bold{RFC (Request For Comments)}")


@slides.slide()
def rfc_process(slide: Box):
    """
    https://github.com/rust-lang/rust/issues/87517
    https://github.com/rust-lang/rust/pull/86735
    https://github.com/rust-lang/rust/pull/94457

    - consensus within the subteam
    - if no consensus => leader decides, should consult with the core team
    - every design or implementation choice carries a trade-off and numerous costs. There is seldom a right answer.
    Once a majority of reviewers approve (and at most 2 approvals are outstanding)
    """
    slide.update_style("default", style=T(size=sw(50)))
    content = slide.box()
    content.box(p_bottom=sh(40)).text("RFC process", style=T(size=sw(60)))
    row = content.box(horizontal=True)
    left = row.box(p_right=sw(50))
    right = row.box(width=sw(1000), y=sh(300))
    lst = ordered_list(left.box())

    items = [
        ("Discuss on Zulip/Rust forum", "rfc-step-1.png"),
        ("Write RFC", "rfc-step-2.png"),
        ("Receive comments", "rfc-step-3.png"),
        ("Modify RFC", "rfc-step-4.png"),
        ("If concerns, goto 3.", None),
        ("Vote", "rfc-step-5.png"),
        ("FCP (Final Comment Period)", "rfc-step-6.png"),
        ("Wait 10 days", "rfc-step-7.png"),
        ("Implement the feature", "rfc-step-8.png"),
        ("Stabilize the feature", "rfc-step-9.png"),
        ("????", None),
        ("Profit", None)
    ]
    rows = []
    for (index, (text, image)) in enumerate(items):
        index = index + 2
        item = lst.item(show=f"{index}+")
        item.text(text)
        rows.append(item)
        if image is not None:
            right.overlay(show=str(index)).image(f"images/{image}")

    durations = [
        ((0, 7), "RFC acceptance: 4 months"),
        ((8, 8), "Implementation + approval: 1 month"),
        ((9, 9), "Stabilization: 9 months")
    ]
    for ((start_index, end_index), label) in durations:
        start = rows[start_index]
        end = rows[end_index]
        x = 900
        x_offset = 1000
        y_start = start.y("50%")
        y_end = end.y("50%")
        wrapper = slide.overlay(show="next")
        wrapper.line([
            (sw(x), y_start),
            (sw(x_offset), y_start),
            (sw(x_offset), y_end),
            (sw(x), y_end),
        ], stroke_width=sw(8))
        y = start.y("0") if start_index == end_index else y_start.map(lambda v: sh((v + y_end.eval()) / 2))
        wrapper.box(x=sw(x_offset + 50), y=y).text(label)


@slides.slide()
def cargo_fcp(slide: Box):
    slide.update_style("default", T(size=sw(50)))
    content = slide.fbox(p_top=sh(40))
    content.box(p_bottom=sh(40)).text("Changing Cargo defaults (FCP)", T(size=sw(60)))
    canvas = content.fbox(width=sw(1600))

    for i in range(1, 6):
        canvas.overlay(show=str(i)).image(f"images/cargo-debuginfo-{i}.png")
    canvas.box(show="next").text("Less than a month")
    canvas.overlay(show="next").image("images/cargo-binary-size.png")
    canvas.overlay(show="next").image("images/cargo-perf.png")


@slides.slide()
def handling_conflicts(slide: Box):
    content = slide.box()
    content.box().text("How to handle conflicts?")


@slides.slide()
def great_int_debate(slide: Box):
    content = slide.box()
    content.box(p_bottom=sh(40)).text("Great int debate (2014)")
    quotation(content.box(show="next+"),
              """We have been reading these threads and have also done a lot
of internal experimentation, and we believe we’ve come to a final
decision on the fate of integers in Rust.""",
              "Core team (2014)", size=sw(56))


@slides.slide()
def no_new_rationale(slide: Box):
    """
    https://aturon.github.io/tech/2018/05/25/listening-part-1/
    """
    content = slide.box()
    content.box(p_bottom=sh(40)).text("No new rationale")
    content.box(show="next+").text(
        """decisions must be made only on the basis of rationale
already debated in public (to a steady state)""",
        T(size=sw(50)))


@slides.slide()
def await_syntax(slide: Box):
    """
    https://boats.gitlab.io/blog/post/await-decision/
    https://boats.gitlab.io/blog/post/await-decision-ii/
    """
    slide.update_style("code", style=T(size=sw(70)))
    content = slide.box()
    content.box(p_bottom=sh(40)).text("~tt{Await}ing a solution (2018/2019)")
    code(content.box(show="next+"), """
await!(fut);
await fut;
await { fut };
fut.await;
fut.await();
fut.await!;
fut@await;
""")


@slides.slide()
def await_discussion(slide: Box):
    canvas = slide.fbox()
    canvas.overlay(show="1").box(width=sw(1600)).image("images/await-discussion-1.png")
    canvas.overlay(show="next").box(width=sw(1600)).image("images/await-discussion-2.png")


@slides.slide()
def await_solution(slide: Box):
    canvas = slide.fbox()
    canvas.overlay(show="1").box(width=sw(1400)).image("images/await-reaction-1.png")
    canvas.overlay(show="1").line([
        (sw(350), sh(270)),
        (sw(1130), sh(270))
    ], color="red", stroke_width=sw(14))
    canvas.overlay(show="next").box(width=sw(1000)).image("images/await-reaction-2.png")


@slides.slide()
def graydon_conflicts(slide: Box):
    """
    - https://graydon2.dreamwidth.org/307105.html
    - unresolved conflict => one party leaves
    - burnout
    - people who do the work get to decide (unfair?)
      - attend every city meeting to push your goal
    - Graydon's suggestion: hire professionals
    - transparency
    """
    content = slide.box()
    content.box(p_bottom=sh(40)).text("Unresolved conflicts")

    lst = unordered_list(content.box())
    lst.item(show="next+").text("Burnout")
    lst.item(show="next+").text("One party leaves")
    lst.item(show="next+").text("Most work done => most voting rights?")
    lst.item(show="next+").text("Transparency")


@slides.slide()
def how_to_get_something_done(slide: Box):
    slide.update_style("default", T(size=sw(60)))
    content = slide.fbox(p_top=sh(40))
    content.box(p_bottom=sh(40)).text("How to get something done?", T(size=sw(60)))
    canvas = content.fbox()

    lst = unordered_list(canvas.box())
    # LTO
    lst.item().text("Poke someone to do it")
    canvas.overlay(show="next").box(width=sw(1400)).image("images/lto-pr.png")
    canvas.overlay(show="next").box(width=sw(1400)).image("images/lto-results.png")
    # Cargo Docker caching
    lst.item(show="next+").text("Summarize the current state")
    # https://hackmd.io/jgkoQ24YRW6i0xWd73S64A
    # 22-page document
    canvas.overlay(show="next").box(width=sw(1400)).image("images/cargo-docker-caching.png")
    # Cargo debuginfo stripping, Clippy lint, Rust annual survey, GSoC 2024
    lst.item(show="next+").text("Do it :-)")
    images = [
        "cargo-debuginfo-1.png",
        "cargo-debuginfo-5.png",
        # https://github.com/rust-lang/rust-clippy/pull/12077
        "clippy-lint-question.png",
        "clippy-lint-pr.png",
        # https://github.com/rust-lang/surveys/pull/234
        "survey-question.png",
        "survey-pr.png",
        # https://hackmd.io/hJhkRIJ5RneLXkQp9p8Xng
        "gsoc-question.png",
        "gsoc-hackmd.png"
    ]
    for image in images:
        canvas.overlay(show="next").box(width=sw(1400)).image(f"images/{image}")


@slides.slide()
def how_to_join(slide: Box):
    slide.update_style("link", T(bold=False))
    slide.update_style("default", T(size=sw(50)))
    content = slide.box()
    content.box(p_bottom=sh(40)).text("How to join the fray?", T(size=sw(60)))
    lst = unordered_list(content.box())
    lst.item(show="next+").text("Lurk, observe, engage @ Zulip")
    lst.ul().item().text("~link{https://rust-lang.zulipchat.com}")
    lst.item(show="next+").text("Find easy issues @ GitHub")
    lst.ul().item().text("~link{https://github.com/rust-lang/rust/labels/E-easy}")
    lst.item(show="next+").text("Study")
    sublist = lst.ul()
    sublist.item(show="next+").text("Forge: ~link{https://forge.rust-lang.org/}")
    sublist.item(show="next+").text("Rustc dev guide: ~link{https://rustc-dev-guide.rust-lang.org/}")
    sublist.item(show="next+").text("Stdlib dev guide: ~link{https://std-dev-guide.rust-lang.org/}")


if SHOW_PRIVATE:
    @slides.slide()
    def invitation(slide: Box):
        content = slide.fbox()
        content.overlay(show="1").box(width=sw(1600)).image("images/wg-compiler-perf-invitation.png")
        content.overlay(show="next").box(width=sw(1600)).image("images/infra-invitation.png")


@slides.slide()
def rust_needs_you(slide: Box):
    slide.box(width=sw(800)).image("images/contribute-meme.png")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:")
    qr = generate_qr_code(
        "https://github.com/kobzol/talks/tree/main/2024/rust-prague/rust-governance/",
        scale=14)
    slide.box().image(qr, image_type="png")

    slide.box().text("Slides were created with ~tt{github.com/spirali/elsie}",
                     style=T(size=40))


def ferris(slides: SlideDeck):
    count = sum(slide.steps() for slide in slides._slides)
    size = 80
    x_first = REFERENCE_WIDTH
    x_last = REFERENCE_WIDTH - (size * 1.05)
    y = int(REFERENCE_HEIGHT * 0.02)
    x_diff = abs(x_first - x_last)

    total_steps = 0
    for i, slide in enumerate(slides._slides):
        steps = slide.steps()
        for step in range(steps):
            progress = (total_steps + step) / count
            x = x_first - progress * x_diff
            slide.box().box(show=step + 1, x=sw(x), y=sh(y), width=sw(size), height=sh(size)).image(
                "images/ferris.svg")
        total_steps += steps


def print_stats(slides: SlideDeck, minutes: int):
    step_count = sum(slide.steps() for slide in slides._slides)
    slide_count = len(slides._slides)

    seconds = minutes * 20
    print(f"{slide_count} slides, {math.floor(seconds / slide_count)}s per slide")
    print(f"{step_count} steps, {math.floor(seconds / step_count)}s per step, {step_count / slide_count:.2f} steps per slide")


if PRODUCTION_BUILD:
    ferris(slides)
    print_stats(slides, minutes=40)

slides.render("slides.pdf")
