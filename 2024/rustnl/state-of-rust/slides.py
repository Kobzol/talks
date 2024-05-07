import math
from typing import Literal, Optional, Tuple

import elsie
import pandas as pd
from elsie import Arrow, SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.slides.slide import Slide
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from sections import SectionManager
from utils import LOWER_OPACITY, dimmed_list_item, \
    generate_qr_code, quotation, render_plot, source, survey_quotation, survey_source, with_bg

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=sw(70)))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")

IMG_BG_COLOR = "#DDDDDD"


@slides.slide()
def intro(slide: Box):
    slide.update_style("default", T(size=sw(40)))
    slide.box(p_bottom=sh(60), width=sw(400)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("State of Rust", style=T(size=sw(90), bold=True))
    slide.box().text("Jakub Beránek", style=T(size=sw(50)))

    wrapper = slide.box(x="[95%]", y="[95%]")
    wrapper.box().text("With input from:")
    lst = unordered_list(wrapper.box())
    lst.item().text("Vitaly Bragilevsky")
    lst.item().text("Hugo van de Pol")
    lst.item().text("Joran Dirk Greef")


@slides.slide()
def what_why_where_who_when_how(slide: Box):
    """
    My own personal insights, experience of the Rust community (based on surveys) and testimonials
    from Rust companies.
    Elevator pitch for Rust.
    """
    lst = unordered_list(slide.box())
    items = ["What", "Why", "Where", "Who", "When"]
    for (index, item) in enumerate(items, start=1):
        lst.item(show=f"{index}+", label="", label_padding=0).text(f"{item}?")


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

    content = slide.box(x=sw(150))

    content.fbox(p_bottom=sh(30)).text("Jakub Beránek", T(align="left", size=sw(80), bold=True))
    gh = content.box(x=0, horizontal=True, p_bottom=sh(5))
    gh.box(width=sw(50)).image("images/github-logo.png")
    gh.box(p_left=sw(20)).text("github.com/kobzol", style=T(size=sw(50)))
    email = content.box(x=0, horizontal=True, p_bottom=sh(40))
    email.box(width=sw(50)).text("@", style=T(size=sw(70), bold=True))
    email.box(p_left=sw(20)).text("jakub@berankovi.net", style=T(size=sw(50)))

    content.box(x=0, width=sw(600), height=sw(2)).rect(bg_color="black")

    lst = unordered_list(content.box(x=0, p_top=sh(40)))
    dimmed_list_item(lst,
                     "PhD, teaching, research @ IT4Innovations (Czech Republic supercomputing center)",
                     show=2)
    lst.item(show="last+").text("Rust Project open-source contributor")
    lst2 = lst.ul()
    lst2.item(show="next+").text("Rust Infrastructure team (member)")
    lst2.item(show="next+").text("Rust Survey team (co-lead)")

    with_bg(
        slide.box(x=sw(1000), y=sh(50), width=sw(860), height=sh(700), show="4"), bg_color=IMG_BG_COLOR
    ).image("images/team-infra.png")
    with_bg(
        slide.box(x=sw(1000), y=sh(50), width=sw(855), height=sh(700), show="5"), bg_color=IMG_BG_COLOR
    ).image("images/annual-survey.png")


@slides.slide()
def disclaimer(slide: Box):
    """
    All claims, opinions and possible errors are my own.
    """
    slide.box(p_bottom=sh(40)).text("(disclaimer)", style=T(size=sw(90)))
    slide.box().text("All opinions (and possible errors) are my own :-)", T(size=sw(60)))


@slides.slide()
def rust_slogan(slide: Box):
    slide.box(width=sw(1400)).image("images/rust-slogan.png")


@slides.slide()
def rust_timeline(slide: Box):
    """
    To give a little bit of context.
    Rust Foundation is an independent non-profit organization that supports Rust
    (Project, process, toolchain).
    """
    slide.box(y=sh(100)).text("Rust timeline")

    point_height = sh(80)

    def render_year_tick(
            timeline: Box,
            year: int,
            text: Optional[str] = None,
            show: Optional[str] = None
    ):
        this_year = 2024
        first_year = 2006

        wrapper_width = sw(150)
        point_width = sw(25)

        x_percent = (year - first_year) / (this_year - first_year)
        timeline_entry = slide.box(
            width=wrapper_width,
            x=timeline.x(f"{round(x_percent * 100)}%").add(-point_width / 2).add(
                -wrapper_width / 2),
            y=timeline.y("50%").add(-point_height / 2),
            show=show
        )

        if text is None:
            text = str(year)
        timeline_entry.box(width=point_width, height=point_height).rect(bg_color="black")
        timeline_entry.box(p_top=sh(20)).text(text, style=T(size=sw(60)))
        return timeline_entry

    timeline_height = sh(30)
    timeline = slide.box(width="70%", x="15%", height=timeline_height)
    timeline.rect(bg_color="black")

    # Origin
    year_2006 = render_year_tick(timeline, 2006)
    slide.box(x=year_2006.x("100%"), y=timeline.y("0").add(-sh(150)), width=sw(300),
              show="next+").image("images/logos/mozilla.png")
    project_box = slide.box(x=year_2006.x("100%").add(sw(100)), y=timeline.y("100%").add(sh(100)),
                            show="next+")
    project_box.box(width=sw(200)).image("images/rust-logo.png")
    project_box.box().text("Rust Project")

    # 1.0
    year_2015 = render_year_tick(timeline, 2015, show="next+")
    slide.box(x=year_2015.x("0").add(-sw(40)), y=timeline.y("0").add(-sh(150)), show="last+").text(
        "Rust 1.0")

    # Rust Foundation
    year_2021 = render_year_tick(timeline, 2021, show="next+")
    slide.box(show="last+", x=year_2021.x("0").add(-sw(100)), y=year_2021.y("0").add(-sh(250)),
              width=sw(400)).image("images/rust-foundation-logo.png")

    render_year_tick(timeline, 2024, text="2024+", show="next+")
    slide.box(show="last+").line((
        timeline.p("100%", "50%").add(0, 0),
        timeline.p("100%", "50%").add(sw(200), 0)
    ), stroke_width=timeline_height, stroke_dasharray=10, end_arrow=Arrow(size=sw(50)))


@slides.slide()
def rust_is_here_to_stay(slide: Box):
    slide.box(p_bottom=sh(80)).text("Rust Foundation Platinum members")
    slide.box().image("images/rust-foundation-platinum-members.png")


@slides.slide()
def rust_rover(slide: Box):
    slide.box().image("images/rust-rover.png")


def trifecta(slides: SlideDeck,
             type: Optional[Literal["performance", "reliability", "productivity"]] = None):
    slide = slides.new_slide()
    img = slide.box(width=sw(1800)).image("images/rust-trifecta.png")

    bg_color = "red"
    stroke_width = sw(8)
    if type == "performance":
        x = sw(5)
    elif type == "reliability":
        x = sw(610)
    elif type == "productivity":
        x = sw(1310)
    else:
        assert type is None
        return
    img.box(x=x, y="55%", width=sw(450), height=sh(100)).rect(color=bg_color,
                                                              stroke_width=stroke_width)


trifecta(slides)
trifecta(slides, "performance")

section_manager = SectionManager()

with section_manager.start_section(slides, "Performance"):
    @slides.slide()
    def performance_by_default(slide: Box):
        """
        https://discord.com/blog/why-discord-is-switching-from-go-to-rust
        """
        box = slide.box(p_bottom=sh(40)).text("Rust programs are efficient ~bold{by default.}",
                                              T(size=sw(80))).inline_box("bold")
        box.overlay(show="1", x=-5, width="110%", height="110%").rect(bg_color="white")
        slide.box(show="3+").text('"Time-to-performance"')
        slide.box(show="next+", x="[50%]", y="[50%]", width=sw(1400)).image(
            "images/discord-rust.png")
        quotation(slide.overlay(show="next").box(), """Even with ~bold{just basic optimization},
Rust was able to ~bold{outperform the hyper hand-tuned} Go version...
 
""", "Discord")
        slide.set_style("muted", T(opacity=0.3))
        quotation(slide.overlay(show="next").box(), """~muted{Even with ~bold{just basic optimization},
Rust was able to ~bold{outperform the hyper hand-tuned} Go version...}
...we were able to beat Go on every single performance metric.""", "Discord")


    # @slides.slide()
    # def predictable(slide: Box):
    #     slide.box().text("~bold{Predictable} performance", T(size=sw(120)))
    #     chart = slide.box(show="next+", x="[50%]", y="[50%]", width=sw(1400)).image(
    #         "images/discord-response-time.png")
    #     go = chart.box(x="35%", y="30%").text("Go")
    #     chart.line((
    #         (go.x("0%"), go.y("100%")),
    #         (go.x("0%").add(-sw(100)), go.y("100%").add(sh(80))),
    #     ), color="#826EAD", stroke_width=sw(10), end_arrow=Arrow(size=sw(20)))
    #     rust = chart.box(x="55%", y="120%").text("Rust")
    #     chart.line((
    #         (rust.x("50%"), rust.y("0%")),
    #         (rust.x("50%"), rust.y("0%").add(-sh(160))),
    #     ), color="#4298CA", stroke_width=sw(10), end_arrow=Arrow(size=sw(20)))

    @slides.slide()
    def cost(slide: Box):
        """
        https://medium.com/tenable-techblog/optimizing-700-cpus-away-with-rust-dc7a000dbdb2
        Reduced CI bill and became a bit more sustainable in the process.
        """
        slide.box(show="1").text("More efficient => ~bold{cheaper} to run", T(size=sw(100)))
        slide.box(show="2", x="[50%]", y="[50%]", width=sw(1400)).image("images/rust-tenable.png")
        wrapper = slide.box(show="3+", x="[50%]", y="[50%]", horizontal=True)
        wrapper.box(width=sw(800)).image("images/tenable-cpu.png")
        wrapper.box(width=sw(800)).image("images/tenable-memory.png")
        # maybe skip
        # quotation(slide.overlay(show="4").box(), """With this small change, we were able
# to ~bold{optimize away over 700 CPU and 300GB of memory}.
# This was all implemented, tested and deployed ~bold{in two weeks.}""", "Tenable")

        # maybe skip
        # wrapper.box(width=sw(800)).image("images/rust-serverless.png")
        # slide.box(show="next+", x="[50%]", y="[50%]", width=sw(1400)).image("images/rust-figma.png")
        # table = slide.box(show="next+", x="[50%]", y="[50%]", width=sw(1400)).image(
        #     "images/figma-perf.png")
        # table.box(x="75%", y="32%", width=sw(260), height=sh(430)).rect(color="red",
        #                                                                 stroke_width=sw(8))


    @slides.slide()
    def more_than_perf(slide: Box):
        """
        https://github.blog/2023-02-06-the-technology-behind-githubs-new-code-search/
        https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine
        """
        # maybe skip
        # slide.box(show="next+", x="[50%]", y="[50%]", width=sw(1600)).image("images/github-code-search.png")
        slide.box(width=sw(1700)).image("images/dropbox-rust.png")
        quotation(slide.box(show="next+", x="[50%]", y="[50%]"), """…betting on Rust was one of the best decisions we made.
~bold{More than performance}, its ergonomics and ~bold{focus on
correctness} has helped us tame sync’s complexity.""", "Dropbox")

trifecta(slides, "reliability")

with section_manager.start_section(slides, "Reliability"):
    @slides.slide()
    def bug_free_programs(slide: Box):
        # TODO: reword?
        slide.box().text("Rust makes it easier to write ~bold{correct software}")
        slide.box(show="next+", p_bottom=sh(40)).text("by adding ~bold{guardrails}")


    @slides.slide()
    def confidence(slide: Box):
        slide.box().text("Confidence", T(size=sw(120)))
        quotation(slide.box(show="next", x="[50%]", y="[50%]"), """The language's expressiveness allows our developers to
encode constraints that ~bold{catch errors at compile time}
~bold{rather than in GitHub issues}.""", "Vercel")
        # maybe skip
        # quotation(slide.box(show="next", x="[50%]", y="[50%]"), """My biggest compliment to Rust is that ~bold{it's boring}…
        # and this is an amazing compliment.""", "NPM")
        survey_quotation(slide.overlay(show="next"),
                         "Which of the following statements about Rust do you feel are true?", """
Rust is risky to use in production""", 1.6)


    @slides.slide()
    def memory_safety(slide: Box):
        """
        Combine memory safety with performance
        """
        slide.box(show="1", x="[50%]", y="[50%]").text("Rust is memory safe by default",
                                                       T(size=sw(100)))
        row = slide.box(horizontal=True, show="next+")
        row.box(width=sw(800)).image("images/chrome-safety.png")
        row.box(width=sw(800), p_left=sw(60), show="next+").image("images/microsoft-safety.png")
        slide.box(width=sw(700), p_top=sh(60), show="next+").image("images/android-safety.png")


    @slides.slide()
    def white_house(slide: Box):
        slide.box().image("images/white-house-statement.png")


    @slides.slide()
    def android_code(slide: Box):
        slide.box(width=sw(1200)).image("images/rust-android.png")

    @slides.slide()
    def memory_safety_rewrite(slide: Box):
        slide.box(width=sw(1000), p_bottom=sh(80)).image("images/rewrite-ntp.png")
        slide.box(width=sw(1000)).image("images/rewrite-sudo.png")

    @slides.slide()
    def backwards_compabitility(slide: Box):
        slide.box(p_bottom=sh(20)).text("Stability", T(size=sw(100)))
        slide.box(show="next+", p_bottom=sh(100)).text("Rust 1.0 released in 2015 (9 years ago)")
        slide.box(show="next+", p_bottom=sh(20)).text("…without stagnation", T(size=sw(100)))
        slide.box(show="last+").text("Rust 1.78 released last week")
        survey_quotation(slide.overlay(show="next+"),
                         "Do you agree with the following statements on Rust stability?", """
~bold{Upgrading} to a new stable compiler version\n~bold{requires} either ~bold{no changes} or extremely\nsmall & easy changes to my code""",
                         97.72)

    # @slides.slide()
    # def shift_left(slide: Box):
    #     slide.box(p_bottom=sh(20)).text('"Shift-left"')
    #     lst = unordered_list(slide.box())
    #     lst.item(show="next+").text("Less bugs in production")
    #     lst.item(show="next+").text("Slightly slower development velocity")

    # @slides.slide()
    # def survey_iteration2(slide: Box):
    # slide.box(x="[50%]", y="[50%]", width=sw(1100)).image("images/rust-work-statements.png")
    # survey_source(slide)
    # @slides.slide()
    # def iteration5(slide: Box):
    #     """
    #     https://onesignal.com/blog/rust-at-onesignal/
    #     """
    #     quotation(slide.box(show="1", x="[50%]", y="[50%]"), """The type system is our ultimate
# ~bold{"move quickly and don't break things"} secret weapon.""", "OneSignal")


trifecta(slides, "productivity")

with section_manager.start_section(slides, "Productivity"):
    @slides.slide()
    def unified_tooling(slide: Box):
        """
        Familiarity - within the team and also when onboarding.
        - custom Cargo subcommands
        """
        slide.box(p_bottom=sh(60)).text("Unified tooling", T(size=sw(100)))
        lst = unordered_list(slide.box())
        lst.item(show="next+").text("Building")
        lst.item(show="next+").text("Testing")
        lst.item(show="next+").text("Dependency management")
        lst.item(show="next+").text("Documentation")
        lst.item(show="next+").text("Deployment")
        lst.item(show="next+").text("…")
        slide.box(show="next+", p_top=sh(60)).text("All with a ~bold{single tool} (Cargo)")


    @slides.slide()
    def ecosystem(slide: Box):
        slide.box(p_bottom=sh(60)).text("Package ecosystem", T(size=sw(100)))
        slide.box(width=sw(800)).image("images/crates.io-packages.png")


    @slides.slide()
    def dependencies(slide: Box):
        """
        https://www.rust-lang.org/static/pdfs/Rust-npm-Whitepaper.pdf
        """
        quotation(slide.box(), """Rust has absolutely ~bold{stunning dependency management}.""", "NPM")


# @slides.slide()
# def survey_rust_at_work(slide: Box):
#     slide.box(x="[50%]", y="[50%]", width=sw(1050)).image(
#         "images/survey-why-you-use-rust-at-work.svg")
#     slide.box(x="[4%]", y="[98%]").text("Not all answers are displayed", T(size=sw(40)))
#     survey_source(slide)


with section_manager.start_section(slides, "Trade-offs"):
    @slides.slide()
    def too_reliable(slide: Box):
        """
        Rapid prototyping, throwaway code
        """
        slide.set_style("it", T(italic=True))
        slide.box(p_bottom=sh(50)).text(
            """Rust is great for\nefficient, production-ready software""", T(size=sw(80)))
        slide.box(show="next+").text("Not ~it{all} software is like that")
        survey_quotation(slide.overlay(show="next"),
                         "Which of the following statements are reasons why you use Rust at work?", """
We find it easy to prototype with""", 14)


    @slides.slide()
    def ramp_up_time(slide: Box):
        slide.box().text("Longer initial ramp-up time")
        slide.box(width=sw(100), show="next+").image("images/hand-in-hand.png")
        slide.box(show="last+").text("Less bugs in production")

        # maybe skip
        # quotation(slide.box(show="next+", x="[50%]", y="[50%]"), """You will write a correct program, but you will have to think
# about all the angles of that correct program.""", "NPM")

        survey_quotation(slide.overlay(show="next"),
                         "Which of the following statements apply to your experience using Rust at work?", """
Overall, adopting Rust has slowed down our team""", 8.2, question_size=50)


    @slides.slide()
    def onboarding(slide: Box):
        slide.box().text("Onboarding", T(size=sw(100)))

    @slides.slide()
    def google_productivity(slide: Box):
        slide.box(x="[50%]", y="[50%]", width=sw(1600)).image(
            "images/google-survey.png")
        source(slide, "Lars Bergstrom - Beyond Safety and Speed: How Rust Fuels Team Productivity")

    # maybe skip
    # @slides.slide()
    # def survey_learning_curve(slide: Box):
    #     """
    #     Lot of great learning materials.
    #     """
        # TODO: add steps
        # slide.box(width=sw(1000)).image("images/survey-which-statements-are-true.svg")
        # survey_source(slide)
        # slide.box(x="[4%]", y="[98%]").text("Not all answers are displayed", T(size=sw(40)))

    @slides.slide()
    def ecosystem_maturity(slide: Box):
        slide.box(p_bottom=sh(40)).text("Ecosystem maturity", T(size=sw(100)))
        slide.box(show="next+").text("Many libraries, less frameworks")

    @slides.slide()
    def lego_like_ecosystem(slide: Box):
        quotation(slide.box(), "Rust has a Lego-like package ecosystem.", "Luca Palmieri")

if PRODUCTION_BUILD:
    section_manager.apply(slides)


trifecta(slides)


@slides.slide()
def stack_overflow(slide: Box):
    """
    To me, these features are nice, but we also need to see the global picture.
    """
    slide.box(width=sw(1400)).image("images/stack-overflow-streak.png")


@slides.slide()
def where_is_rust_used(slide: Box):
    slide.box().text("Where is Rust being used today?", T(size=sw(100)))


@slides.slide()
def geographical(slide: Box):
    slide.box(width=sw(1150)).image("images/survey-country.svg")
    survey_source(slide)


@slides.slide()
def areas(slide: Box):
    slide.box(width=sw(1150)).image("images/survey-areas.svg", select_fragments=[
        1,
        2,
        2,
        3,
        3,
        4,
        4,
        5,
        5
    ])
    with_bg(
        slide.box(width=sw(1700), height=sh(610), x="[50%]", y="[50%]", show="3"), bg_color=IMG_BG_COLOR
    ).image("images/github-code-search.png")
    with_bg(
        slide.box(width=sw(1700), height=sh(610), x="[50%]", y="[50%]", show="5"), bg_color=IMG_BG_COLOR
    ).image("images/rust-cloudflare.png")
    # C/C++ head start, Vendor support, qualification
    with_bg(
        slide.box(width=sw(1400), height=sh(480), x="[50%]", y=sh(50), show="7"),
        bg_color=IMG_BG_COLOR
    ).image("images/ferrocene-rust.png")
    with_bg(
        slide.box(width=sw(1400), height=sh(390), x="[50%]", y=sh(550), show="7"),
        bg_color=IMG_BG_COLOR
    ).image("images/infineon.png")
    with_bg(
        slide.box(width=sw(1800), height=sh(750), x="[50%]", y="[50%]", show="9"),
        bg_color=IMG_BG_COLOR
    ).image("images/zed.png")

    survey_source(slide)
    slide.box(x="[4%]", y="[98%]").text("Not all answers are displayed", T(size=sw(40)))


@slides.slide()
def os_windows(slide: Box):
    slide.box(width=sw(1000), x=sw(50), y=sh(100)).image("images/windows-drivers-rust.png")
    slide.box(width=sw(1000), x=sw(700), y=sh(320)).image("images/windows-kernel-rust.png")


@slides.slide()
def linux_kernel(slide: Box):
    slide.box(width=sw(1500)).image("images/linux-kernel-rust.png")
    quotation(slide.overlay(show="next+").box(), "…on the whole, I don't hate it.",
              "Linus Torvalds")


@slides.slide()
def tooling(slide: Box):
    """
    Evaluate Rust on tooling
    """
    slide.box(width=sw(1500), show="1").image("images/turborepo.png")
    slide.box(width=sw(1200), show="next", x="[50%]", y="[50%]").image("images/ruff.png")


# @slides.slide()
# def ui(slide: Box):
#     slide.box().text("User interface")
#     lst = unordered_list(slide.box())
#     lst.item().text("Web technologies (Dioxus, Tauri)")
#     lst.item().text("Native UI")
#     lst.item().text("Embedded (Dioxus, Tauri)")
#     lst.item().text("Still being figured out")


@slides.slide()
def rust_anywhere(slide: Box):
    """
    Platforms
    Code reuse
    It can be incrementally adopted into existing software
    """
    slide.set_style("italic", T(italic=True))
    slide.box(p_bottom=sh(40)).text("Rust ~italic{anywhere}", T(size=sw(100)))
    lst = unordered_list(slide.box())

    texts = [
        "Linux, Windows, macOS, …",
        "Cloud, backend, frontend, desktop, mobile, …",
        "From embedded devices to supercomputers",
        "Code reuse"
    ]
    for (step, text) in enumerate(texts, start=2):
        dimmed_list_item(lst, text, show=step)

    # Rust plays well with other languages
    lst.item(show="last+").text("Interoperable with C, C++, Python, WebAssembly, …")


@slides.slide()
def adoption_of_rust(slide: Box):
    slide.box().text("Adoption of Rust", T(size=sw(100)))


@slides.slide()
def companies(slide: Box):
    logos = [
        "aws.png",
        "google.png",
        "huawei.png",
        "meta.png",
        "microsoft.png",
        "npm.png",
        "dropbox.png",
        "discord.png",
        "cloudflare.png",
        "atlassian.png",
        "1password.png",
        "arm.png",
        "jetbrains.png",
        "figma.svg",
        "sentry.png",
        "shopify.png"
    ]
    rows = 4
    cols = 4
    assert rows * cols >= len(logos)

    width = 320
    margin_x = 50
    margin_y = 50

    for r in range(rows):
        row = slide.box(horizontal=True, p_bottom=sh(margin_y) if r < rows - 1 else 0)
        for c in range(cols):
            index = r * cols + c
            if index >= len(logos):
                break
            logo = logos[index]
            box = row.box(width=sw(width), p_right=sh(margin_x) if c < cols - 1 else 0)
            box.image(f"images/logos/{logo}")
    slide.box(y="86%").text("…", T(size=sw(100)))


@slides.slide()
def stackoverflow_survey(slide: Box):
    """
    https://survey.stackoverflow.co/2023/#most-popular-technologies-language-prof
    """
    img = slide.box(height=sh(900)).image("images/rust-usage-stackoverflow.png")
    text = img.box(x=-sw(200), y=sh(620)).text("~12%", escape_char="_")
    img.line((
        (text.x("0%"), text.y("100%").add(10)),
        (text.x("100%").add(sw(180)), text.y("100%").add(10)),
    ), stroke_width=sw(8), color="red", end_arrow=Arrow(size=sw(30)))
    source(slide, "Stack Overflow Developer Survey 2023")


@slides.slide()
def jetbrains_survey(slide: Box):
    """
    https://www.jetbrains.com/lp/devecosystem-2023/languages/#proglang7years
    """
    img = slide.box(height=sh(900)).image("images/rust-usage-jetbrains.png")
    text = img.box(x=img.x("100%").add(sw(100)), y=sh(620)).text("~10%", escape_char="_")
    img.line((
        (text.x("100%"), text.y("100%").add(10)),
        (text.x("0%").add(-sw(150)), text.y("100%").add(10)),
    ), stroke_width=sw(8), color="red", end_arrow=Arrow(size=sw(30)))
    text = img.box(show="next+", x=text.x("0%").add(sw(-140)), y=text.y("150%")).text(
        "Five years ago: 2%")
    img.box(show="last+").line((
        (text.x("100%"), text.y("100%").add(10)),
        (text.x("0%").add(-sw(560)), text.y("100%").add(10)),
    ), stroke_width=sw(8), color="red", end_arrow=Arrow(size=sw(30)))
    source(slide, "The State of Developer Ecosystem in 2023 (JetBrains)")


# @slides.slide()
# def statista_survey(slide: Box):
#     """
#     https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/
#     """
#     img = slide.box(height=sh(950)).image("images/rust-usage-statista.png")
#     text = img.box(x=-sw(200), y=sh(735)).text("~13%", escape_char="_")
#     img.line((
#         (text.x("0%"), text.y("100%").add(10)),
#         (text.x("100%").add(sw(180)), text.y("100%").add(10)),
#     ), stroke_width=sw(8), color="red", end_arrow=Arrow(size=sw(30)))
#     source(slide, "Statista.com")


# @slides.slide()
# def slashdata_survey(slide: Box):
#     """
#     https://www.developernation.net/resources/reports/state-of-the-developer-nation-q3-2021/
#     https://www.developernation.net/resources/reports/state-of-the-developer-nation-q3-2022/
#     https://www.developernation.net/resources/reports/state-of-the-developer-nation-25th-edition-q3-20231/
#     """
#     slide.box(p_bottom=sh(40)).text("Size of programming language communities")
#     row = slide.box(horizontal=True)
#     row.box(y=0).image("images/slashdata-q3-2021.png")
#     row.box(y=0).image("images/slashdata-q3-2022.png")
#     row.box(y=0).image("images/slashdata-q3-2023.png")
#
#     source(slide, "SlashData State of the Developer Nation 2021/2022/2023")

# @slides.slide()
# def job_market(slide: Box):
#     wrapper = slide.box().text("Job market")
#     Survey data?


@slides.slide()
def ecosystem_size(slide: Box):
    """
    Rust: 144,387 (https://crates.io/)
    Python: 523,534 (https://pypistats.org/)
    npm: 2 827 860 (https://www.npmjs.com/package/all-the-package-names)
    """
    slide.box(p_bottom=sh(80)).text("Package ecosystem size", T(size=sw(100)))
    lst = unordered_list(slide.box())

    items = [("Rust", "~140k"), ("Python", "~520k"), ("JavaScript", "~2,800k")]
    for (technology, size) in items:
        box = lst.item(show="next+").box(horizontal=True)
        box.box(width=sw(400)).text(technology)
        box.box(width=sw(300)).text(str(size), T(align="right"), escape_char="_")
    source(slide, "~tt{crates.io}, ~tt{pypistats.org}, ~tt{all-the-package-names}")


@slides.slide()
def package_count_growth(slide: Box):
    slide.box().text("Number of Rust packages")

    df = pd.read_csv("data/crates-per-month.csv")
    plot = render_plot(df)
    slide.box(width=sw(1400)).image(plot, image_type="png")

    source(slide, "~tt{crates.io}")


def package_download_chart(parent: Box, **box_args) -> Box:
    df = pd.read_csv("data/crate-downloads-per-month.csv")

    def formatter(value, *args) -> str:
        return f"{int(value // 10e8)} bil"

    plot = render_plot(df, yaxis_formatter=formatter)
    parent.box().text("Rust package downloads")
    box = parent.box(width=sw(1400), **box_args)
    box.image(plot, image_type="png")
    return box


def scale_chart(slide: Box, text_show: Optional[str] = "next+") -> Box:
    wrapper = slide.box()
    box = package_download_chart(wrapper)
    wrapper.box(show=text_show, x=box.x("15%"), y=box.y("60%")).text(
        "Rust is no longer ~bold{niche}…",
        T(align="left")
    )
    source(slide, "~tt{crates.io}")
    return box


@slides.slide()
def no_longer_niche(slide: Box):
    scale_chart(slide)


zoom_scale = 0.75
scaled_width = WIDTH * zoom_scale
scaled_height = HEIGHT * zoom_scale
x_offset = -800
y_offset = 300


@slides.slide(view_box=(
        -scaled_width - x_offset,
        -scaled_height - y_offset,
        scaled_width * 2 + WIDTH,
        scaled_height * 2 + HEIGHT
))
def not_yet_mainstream(slide: Box):
    """
    Choosing a technology is an investment
    """
    box = scale_chart(slide, text_show=None)

    end_point = box.p("100%", "0").add(sw(120), -sh(650))
    box.path([
        ("M",
         box.p("98%", "5%"),
         ),
        ("Q",
         box.p("100%", "0").add(sw(100), -sh(300)),
         end_point
         ),
    ], stroke_dasharray="12", color="#1F77B4", stroke_width=sw(8),
        end_arrow=Arrow(size=sw(60), angle=30, inner=0.75))
    box.box(x=end_point.x.add(sw(100)), y=end_point.y.add(sh(200))).text(
        "…but it is not yet fully ~bold{mainstream}.",
        T(align="left", size=sw(100))
    )
    box.box(x=box.x("100%"), y=box.y("0").add(-sh(50)), width=sw(300)).image("images/rust-logo.png")
    box.box(x=end_point.x.add(-sw(500)), y=end_point.y.add(-sh(200)), width=sw(300)).image(
        "images/python-logo.svg"
    )
    box.box(x=end_point.x.add(sw(200)), y=end_point.y.add(-sh(500)), width=sw(500)).image(
        "images/java-logo.svg"
    )
    box.box(x=end_point.x.add(-sw(150)), y=end_point.y.add(-sh(500)), width=sw(300)).image(
        "images/javascript-logo.svg"
    )


@slides.slide()
def competitive_advantage(slide: Box):
    """
    To sum up:
    - Rust provides great value in terms of correctness and performance.
    - But in the end, it's just a technology, it requires the right use-case and an investment.

    How? Wait for the panel.
    """
    img = slide.box(width=sw(1400)).image("images/rust-tilde.png")
    img.box(x=0, y="90%", width="100%", height=sh(20)).rect(bg_color="red")
    source(slide, "Rust Case Study: How Rust is Tilde’s Competitive Advantage")


@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(60)).text("Thank you for your attention!", style=T(size=70, bold=True))

    link = "https://blog.rust-lang.org/2024/02/19/2023-Rust-Annual-Survey-2023-results.html"
    qr_code = generate_qr_code(link)

    slide.box().text("Rust Annual Survey 2023:")
    slide.box(width=sw(600)).image(qr_code, image_type="png")

    slide.box().text("Slides were created using ~tt{github.com/spirali/elsie}",
                     style=T(size=40))


def ferris(slides: SlideDeck):
    count = sum(slide.steps() for slide in slides._slides)

    def calculate_dim(slide: Slide, progress: float) -> Tuple[float, Tuple[float, float]]:
        size = 80
        if slide.view_box is not None:
            size *= slide.view_box[2] / WIDTH
            size = sw(size)

            reference_x = slide.view_box[2] + slide.view_box[0]

            x_first = reference_x
            x_last = reference_x - (size * 1.05)
            x_diff = abs(x_first - x_last)
            x = x_first - progress * x_diff
        else:
            x_first = REFERENCE_WIDTH
            x_last = REFERENCE_WIDTH - (size * 1.05)
            x_diff = abs(x_first - x_last)
            x = x_first - progress * x_diff
            x = sw(x)
            size = sw(size)

        if slide.view_box is not None:
            y = int(HEIGHT * 0.02)
            y += slide.view_box[1] + 32
        else:
            y = int(REFERENCE_HEIGHT * 0.02)
            y = sh(y)

        return (size, (x, y))

    total_steps = 0
    for i, slide in enumerate(slides._slides):
        steps = slide.steps()
        for step in range(steps):
            progress = (total_steps + step) / count
            (size, (x, y)) = calculate_dim(slide, progress=progress)
            slide.box().box(show=step + 1, x=x, y=y, width=size, height=size).image(
                "images/ferris.svg")
        total_steps += steps


def print_stats(slides: SlideDeck, minutes: int):
    step_count = sum(slide.steps() for slide in slides._slides)
    slide_count = len(slides._slides)

    seconds = minutes * 60
    print(f"{slide_count} slides, {math.floor(seconds / slide_count)}s per slide")
    print(f"{step_count} steps, {math.floor(seconds / step_count)}s per step")


if PRODUCTION_BUILD:
    ferris(slides)
    print_stats(slides, minutes=16)

slides.render("slides.pdf")
