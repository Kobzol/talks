from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import ShowRest, StateCounter, aka, arrow_box, code, code_step, last, project, quotation, \
    show, skip, source


def test_behavior(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_behavior(slide: Box):
        """
        Public API doesn't change that often.
        Public API of libraries, CLI of binaries.
        """
        tips.tip(slide, "Test public (rather than private) interfaces")
        aka(slide, "Test behavior, not implementation", show="last+")
        aka(slide, "Prefer black-box (rather than white-box) tests", show="last+")

    @slides.slide()
    def testing_pyramids(slide: Box):
        """
        Why split tests based on categories?
        How often a test breaks, how flaky it is, how fast it is.
        """

        row = slide.box(horizontal=True)
        row.box(width=800).image("images/testing-pyramid-1.jpg")
        row.box(show="next+", width=800).image("images/testing-pyramid-2.png")
        source(slide, "semaphore.io, Kent C. Dodds")

    @slides.slide()
    def neural_network_test(slide: Box):
        """
        When your tests are high-level, they won't break when you refactor your code.
        """
        slide.box(p_bottom=40).text("Neural Network Test")
        quotation(slide.box(),
                  """Can you re-use the test suite if your entire software is
replaced with an opaque neural network?""",
                  "Aleksey Kladov (matklad)")

    @slides.slide()
    def bors_integration_test(slide: Box):
        """
        This won't break when the code is refactored.
        """
        slide.update_style("code", T(size=44))

        width = 1700
        code(slide.fbox(), """
def test_ci_try_build(ctx: TestCtx):
    ctx.post_comment("@bors r=karel")
    comment = ctx.get_comment()
    assert comment == "Pull request was approved by karel"

    ci_workflow = Workflow.from_branch(ctx.try_branch())
    ctx.workflow_start(ci_workflow)
    ctx.workflow_success(ci_workflow)

    comment = ctx.get_comment()
    assert comment == "Try build successful"
""", width=width)
