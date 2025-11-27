import json
import math
import subprocess
from typing import List, Tuple

import elsie
from elsie import SlideDeck, TextStyle
from elsie.boxtree.box import Box
from elsie.ext import unordered_list
from elsie.render.backends import InkscapeBackend
from elsie.render.inkscape import InkscapeShell
from elsie.text.textboxitem import TextBoxItem
from elsie.text.textstyle import TextStyle as T

from config import HEIGHT, REFERENCE_HEIGHT, REFERENCE_WIDTH, WIDTH, sh, sw
from tip_async import async_tests
from tip_compile_time_tests import compile_time_tests
from tip_data_driven_tests import data_driven_tests
from tip_dsl import use_dsls
from tip_easy_to_understand import make_tests_easy_to_understand
from tip_test_behavior import test_behavior
from tip_test_everything import test_everything
from tip_test_in_production import test_in_production
from tip_test_metrics import do_not_stress_metrics
from tip_test_the_real_thing import test_the_real_thing
from tip_things_will_fail import things_will_fail
from tip_use_bors import use_bors
from utils import COLOR_ORANGE, LOWER_OPACITY, StateCounter, bash, code, dimmed_list_item, generate_qr_code, \
    iterate_grid, project

PRODUCTION_BUILD = True

backend = InkscapeBackend(InkscapeShell("/usr/bin/inkscape", text_to_path=True))
slides = elsie.SlideDeck(name_policy="ignore", width=WIDTH, height=HEIGHT, backend=backend)
# slides = elsie.SlideDeck(name_policy="ignore", backend=CairoBackend())

slides.update_style("default",
                    TextStyle(font="Raleway", variant_numeric="lining-nums", size=70))
slides.update_style("code", T(size=50))
slides.set_style("bold", TextStyle(bold=True), base="default")
slides.set_style("bb", TextStyle(bold=True), base="default")
slides.set_style("link", TextStyle(bold=True), base="tt")
slides.set_style("code_muted", T(opacity=LOWER_OPACITY), base="code")
slides.set_style("small", TextStyle(size=50), base="default")
slides.set_style("red", TextStyle(color="red"), base="default")
slides.set_style("r", TextStyle(color="red"), base="default")
slides.set_style("green", TextStyle(color="green"), base="default")

state = StateCounter()


@slides.slide()
def intro(slide: Box):
    slide.box(p_bottom=sh(60), width=sw(300)).image("images/rust-logo.png")
    slide.box(p_bottom=sh(40)).text("Tips for writing better (Rust) tests",
                                    style=T(size=70, bold=True))


@slides.slide()
def whoami(slide: Box):
    slide.update_style("default", T(size=60))

    content = slide.box()

    content.box(p_bottom=200).text("Kuba Beránek", T(align="left", bold=True))
    lst = unordered_list(content.box())
    lst.item().text("Teaching @ VSB-TUO")
    lst.item().text("Research @ IT4Innovations")
    lst.item().text("Co-organizer of Rust meetups :-)")
    lst.item().text("Open-source contributor @ Rust Project")

    gh = content.box(horizontal=True, p_top=200)
    gh.box(width=100).image("images/github-logo.png")
    gh.box(p_left=40).text("github.com/kobzol", style=T(bold=True))


@slides.slide()
def teams(slide: Box):
    content = slide.box()
    height = 1000

    # Link: https://www.rust-lang.org/governance/teams/infra
    # Link: https://www.rust-lang.org/governance/teams/compiler#Compiler%20performance%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Binary%20size%20working%20group
    # Link: https://www.rust-lang.org/governance/teams/compiler#Parallel%20rustc%20working%20group
    for (index, image) in enumerate((
            "team-membership",
            # "wg-perf",
            # "team-infra",
            "leadership-council"
    )):
        content.box(
            show=str(index + 1),
            x="[50%]",
            y="[50%]",
            height=sh(height - (30 * (index - 1)))
        ).image(f"images/{image}.png")


@slides.slide()
def tests(slide: Box):
    slide.box(width=1000).image("images/ballmer-tests.jpeg")


def test_slide(slide: Box, show_data: List[Tuple[int, str]], fail_indices: List[int]):
    green = "#01D220"
    slide.set_style("dot", T(color=green, font="Ubuntu Mono", size=80))
    slide.set_style("red", T(color="red"))
    slide.set_style("green", T(color=green))

    width = 1400
    height = 900
    bash(slide.box(), "$ ./run-tests.sh", width=width, height=height)

    row_start = 150
    col_start = 275
    show_index = 0
    show_rem = show_data[show_index][0]
    rows = 8
    cols = 40
    for (index, (row, col)) in enumerate(iterate_grid(rows=rows, cols=cols, width=30, height=65)):
        show = show_data[show_index][1]
        show_rem -= 1
        if show_rem == 0:
            show_index += 1
            if show_index < len(show_data):
                show_rem = show_data[show_index][0]

        r = row + row_start
        c = col + col_start
        box = slide.box(x=c, y=r, show=show)
        if index in fail_indices:
            box.text("F", slide.get_style("dot").compose(T(color="red")))
        else:
            box.text(".", "dot")

    failed = len(fail_indices)
    passed = rows * cols - failed
    result = "FAILED" if failed > 0 else "ok"
    style = "red" if failed > 0 else "green"
    slide.box(x=col_start, y=720, show="last+").text(
        f"test result: ~{style}{{{result}}}. {passed} passed; {failed} failed;",
        T(color="white", font="Ubuntu Mono", size=50))


@slides.slide()
def test_joke_flaky(slide: Box):
    """
    Do you love tests? I love tests.
    The satisfaction of seeing green tests… Oops. This happens sometimes.
    """
    show_data = [
        (10, "2+"),
        (30, "3+"),
        (26, "4+"),
        (34, "5+"),
        (999, "6+"),
    ]
    test_slide(slide, show_data, [58, 228])


@slides.slide()
def test_joke_ok(slide: Box):
    """
    Let's see… yeah, all fine now!
    """
    show_data = [
        (5, "2+"),
        (38, "3+"),
        (12, "4+"),
        (120, "5+"),
        (999, "6+"),
    ]
    test_slide(slide, show_data, [])


@slides.slide()
def why_tests(slide: Box):
    slide.box(p_bottom=100).text("Why do we bother with tests?", T(size=80))
    lst = unordered_list(slide.box())

    items = [
        'Find regressions sooner ("shift left")',
        "Be more confident when refactoring",
        "Help us develop new functionality",
        "Examples how to use API of our code"
    ]
    for (index, item) in enumerate(items, start=2):
        dimmed_list_item(lst, item, index)

    slide.box(show="6+", p_top=40).text("Code without (useful) tests => legacy code", escape_char="#")


@slides.slide()
def why_tests_suck(slide: Box):
    slide.box(p_bottom=100).text("Tests kinda suck :-/", T(size=80))
    lst = unordered_list(slide.box())
    items = [
        "Difficult to maintain",
        "Difficult to understand",
        "Difficult to reproduce failures",
        "Cause stress"
    ]
    for (index, item) in enumerate(items, start=2):
        if item == items[-1]:
            lst.item(show=index).text(item)
        else:
            dimmed_list_item(lst, item, index)


@slides.slide()
def bors(slide: Box):
    row = slide.box(horizontal=True)
    row.box(width=100).image("images/github-logo.png")
    row.box(p_left=40).text("~link{rust-lang/bors}")
    slide.box(p_top=60).text("Merge queue bot")


@slides.slide()
def disclaimer(slide: Box):
    slide.box(p_bottom=80).text("Disclaimer", T(bold=True, size=80))
    lst = unordered_list(slide.box())
    items = [
        "Highly opinionated",
        "Might not apply to your use-cases!"
    ]
    for (index, item) in enumerate(items, start=1):
        dimmed_list_item(lst, item, index)

    lst.item(show="last+").text("Some tips might be obvious")
    lst2 = lst.ul(show="4+")
    lst2.item(label="").text("…others might seem crazy")


def annoyance(slides: SlideDeck, text: str) -> TextBoxItem:
    slide = slides.new_slide()
    return state.annoyance(slide, text)


annoyance(slides, "Tests break during ~emph{refactoring}")
use_dsls(slides, state)
test_behavior(slides, state)

annoyance(slides, "Tests are hard to understand")
make_tests_easy_to_understand(slides, state)

annoyance(slides, "It is hard to adapt tests to new behavior")
data_driven_tests(slides, state)

annoyance(slides, "~green{Green} tests, ~red{red} production")
test_the_real_thing(slides, state)

@slides.slide()
def use_asserts(slide: Box):
    state.tip(slide, "Use asserts liberally")

@slides.slide()
def assert_example(slide: Box):
    project(slide, "bors")
    code(slide.box(), """
pub async fn cancel_build(
    client: &GitHubClient,
    db: &PgDbClient,
    build: &BuildModel,
) {
    assert_eq!(
        build.status,
        BuildStatus::Pending,
        "Passed a non-pending build to `cancel_build`"
    );
    …
}
""")

compile_time_tests(slides, state)
test_everything(slides, state)
test_in_production(slides, state)

box = annoyance(slides, "Async ~#box{Rust} tests")
box = box.inline_box("#box")
box.line([
    (box.x("0").add(-15), box.y("55%")),
    (box.x("100%").add(10), box.y("55%")),
], color="black", stroke_width=5)
async_tests(slides, state)

@slides.slide()
def final_bors_test(slide: Box):
    slide.update_style("code", T(size=40))
    code(slide.box(), """
#[sqlx::test]
async fn unapprove_lacking_permissions(pool: sqlx::PgPool) {
    run_test(pool, async |bors| {
        bors.approve(()).await?;
        bors.post_comment(Comment::from("@bors r-")
            .with_author(User::unprivileged())
        ).await?;
        insta::assert_snapshot!(
            bors.get_next_comment_text(()).await?,
            @"@unprivileged-user: :key:
            Insufficient privileges: not in review users"
        );

        bors
            .get_pr_copy(())
            .await
            .expect_approved_by(&User::default_pr_author().name);
        Ok(())
    })
    .await;
}
""")

annoyance(slides, "Test metrics")
do_not_stress_metrics(slides, state)

annoyance(slides, "CI is ~green{green} in PR, but ~red{red} after merge")
use_bors(slides, state)


@slides.slide()
def tip_invest_in_test_infra(slide: Box):
    box = state.tip(slide, "Invest in test infrastructure")
    row = slide.box(horizontal=True, show="next+", y=box.y("100%").add(40))
    row.box(p_right=20).text("It is")
    row.box(width=100).image("images/100.svg")
    row.box(p_left=20).text("worth it")


things_will_fail(slides, state)


@slides.slide()
def tldr(slide: Box):
    slide.update_style("default", T(size=60))

    slide.box().text("TLDR:", T(bold=True))

    lst = unordered_list(slide.box(p_top=40))
    items = [
        "Build high-level test APIs",
        "Use data-driven integration tests that are blessable",
        "Make tests visual to ease understanding",
        "Test everything and anything",
        "Don't test nor mock (too many) implementation details"
    ]
    for (index, item) in enumerate(items, start=1):
        if item == items[-1]:
            lst.item(show=str(index)).text(item)
        else:
            dimmed_list_item(lst, item, index)

@slides.slide()
def matklad(slide: Box):
    slide.box().text("Matklad's blog:")
    url = "https://matklad.github.io/2021/05/31/how-to-test.html"
    slide.box(p_top=40).text(url, slide.get_style("link").compose(T(size=44)))

    qr = generate_qr_code(url, scale=18)
    slide.box().image(qr, image_type="png")


@slides.slide()
def rustlangcz(slide: Box):
    slide.box().text("~link{rustlang.cz}")
    qr = generate_qr_code(
        "https://rustlang.cz",
        scale=18
    )
    slide.box().image(qr, image_type="png")

@slides.slide()
def outro(slide: Box):
    slide.box(p_bottom=sh(40)).text("Thank you for your attention!", style=T(size=70, bold=True))

    slide.box().text("Slides are available here:")
    qr = generate_qr_code(
        "https://github.com/kobzol/talks/blob/main/2025/rust-prague/tips-for-better-tests",
        scale=14)
    slide.box().image(qr, image_type="png")

    slide.box().text("Slides were programmed using ~tt{github.com/spirali/elsie}",
                     style=T(size=40))
    if PRODUCTION_BUILD:
        output = subprocess.check_output(["tokei", "--output=json", "."])
        output = json.loads(output)
        lines = int(output["Python"]["code"])
        slide.box().text(f"({lines} lines of Python)",
                     style=T(size=40))
    slide.box(p_top=40).text("Several emojis were used from the Noto Emoji pack", style=T(size=36))


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

    seconds = minutes * 60
    print(f"{slide_count} slides, {math.floor(seconds / slide_count)}s per slide")
    print(f"{step_count} steps, {math.floor(seconds / step_count)}s per step")


def page_numbering(slides: List[Box]):
    slide_count = len(slides)

    numbering_start = 2
    numbering_end = slide_count - 1

    width = 135
    height = 60
    margin = 20

    for i, slide in enumerate(slides):
        if numbering_start <= (i + 1) <= numbering_end:
            box = slide.box(x=sw(REFERENCE_WIDTH - width - margin),
                            y=sh(REFERENCE_HEIGHT - height - margin),
                            width=sw(width),
                            height=sh(height)).rect(
                bg_color=COLOR_ORANGE, rx=5, ry=5
            )
            box.fbox(padding=5).text(f"{i + 1}/{slide_count}",
                                     style=TextStyle(color="white", size=sw(40), align="right"))


if PRODUCTION_BUILD:
    ferris(slides)
    print_stats(slides, minutes=45)

# if PRODUCTION_BUILD:
#     slides.render("slides.pdf", slide_postprocessing=page_numbering)
# else:
slides.render("slides.pdf")
