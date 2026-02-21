from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import COLOR_ORANGE, HideRest, ShowRest, StateCounter, bash, code, code_step, \
    error_message, \
    project, show


def use_dsls(slides: Slides, tips: StateCounter):
    @slides.slide()
    def cargo_build_vs_cargo_test(slide: Box):
        """
        Ideally, tests should change when behavior (not implementation!) changes.
        """
        slide.box(p_bottom=40).text("  1. Perform a refactoring")
        slide.box(p_bottom=40, show="next+").text("( 2. Fix compiler/typing errors )")
        row = slide.box(horizontal=True, show="next+")
        row.box(p_right=40).text("3.")
        row.box(width=1700).image("images/pytest-failures.png")

    @slides.slide()
    def bors_test_api_directly(slide: Box):
        """
        Imagine that you have hundreds of these tests.
        Be forward-looking => if you add a field, will it break your tests?
        Partially automatable with IDE actions.
        No default or named arguments in Rust.
        Insidious => as a project gets larger, tests take more time to maintain.
        Reduce friction to add new tests.
        """
        code(slide.box(), """
def test_set_priority():
    repo = Repository(...)
    pr = PullRequest(
        repo="foo/bar",
        number=5,
        author="kobzol"
    )

    repo.record_pr(pr)
    repo.set_pr_priority(5, 10)

    assert repo.get_pr(5).get_priority() == 10
""")
