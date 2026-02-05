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
        aka(slide, "Test behavior, not implementation")
        aka(slide, "Prefer black-box (rather than white-box) tests")

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

#     @slides.slide()
#     def axum_oneshot(slide: Box):
#         slide.update_style("code", T(size=40))
#
#         width = 1800
#         code_step(slide.fbox(), """
# #[tokio::test]
# async fn http_blackbox_test() -> anyhow::Result<()> {
#     let app = create_axum_app();
#     let response = app
#         .oneshot(
#             Request::builder()
#                 .uri("/subscriber")
#                 .method(Method::POST)
#                 .header(CONTENT_TYPE, mime::APPLICATION_JSON.as_ref())
#                 .body(Body::from(
#                     r#"
# {"name": "Jakub Beránek", "email": "foo@bar.cz"}
# "#,
#                 ))?,
#         )
#         .await?;
#     assert_eq!(response.status(), StatusCode::Ok);
#     Ok(())
# }
# """, [
#             show(5) + skip(9) + last(5),
#             [ShowRest]
#         ], width=width)

    @slides.slide()
    def bors_integration_test(slide: Box):
        """
        This won't break when the code is refactored.
        """
        slide.update_style("code", T(size=44))

        project(slide, "bors")

        width = 1700
        code_step(slide.fbox(), """
#[test]
fn test_try_build() {
    let ctx = // create test context
    ctx.post_comment("@bors r=karel");
    let comment = ctx.get_comment();
    assert_eq!(comment, "Pull request was approved by karel");

    let ci_workflow = Workflow::from(ctx.try_branch());
    ctx.workflow_start(&ci_workflow);
    ctx.workflow_success(&ci_workflow);

    let comment = ctx.get_comment();
    assert_eq!(comment, "Try build successful");
}
""", [
            show(6) + skip(7) + last(1),
            show(10) + skip(3) + last(1),
            [ShowRest]
        ], width=width)

    @slides.slide()
    def bors_unit_test(slide: Box):
        project(slide, "bors")
        code(slide.box(), """
#[test]
fn parse_default_approve() {
    let cmds = parse_commands("@bors r+");
    assert_eq!(cmds, vec![
        Ok(BorsCommand::Approve {
            approver: Approver::Myself,
            priority: None,
        })
    ]);
}
""")

    @slides.slide()
    def test_layers(slide: Box):
        row = slide.box(horizontal=True)
        service = row.box().rect(color="black", stroke_width=4).box(padding=20).text("Command handler")
        space = row.box(width=400)
        parser = row.box().rect(color="black", stroke_width=4).box(padding=20).text(
            "Command parser")

        arrow_box(space, "Depends on", size=50)

        def marker(parent: Box, center: Box, width: int, height: int, color: str, x_offset: int = 0):
            parent.box(
                x=center.x("50%").add(-width / 2 + x_offset), y=center.y("50%").add(-height / 2),
                width=width, height=height
            ).rect(color=color, stroke_width=10, stroke_dasharray="10")

        unit_test_1 = slide.box(show="next")
        marker(unit_test_1, parser, width=700, height=250, color="green")
        col = unit_test_1.box(x=parser.x("50%").add(-150), y=parser.y("100%"))
        col.box(height=200)
        col.box().text("Parser tests", T(color="green"))

        unit_test_2 = slide.box(show="next")
        marker(unit_test_2, service, width=700, height=250, color="red")
        col = unit_test_2.box(x=service.x("50%").add(-200), y=service.y("100%"))
        col.box(height=200)
        col.box().text("Handler tests", T(color="red"))

        unit_test_3 = slide.box(show="next+")
        marker(unit_test_3, space, width=1720, height=400, color="green", x_offset=-10)
        col = unit_test_3.box(x=service.x("50%").add(-200), y=service.y("100%"))
        col.box(height=200)
        col.box().text("Handler tests", T(color="green"))

    # @slides.slide()
    # def impl_is_behavior(slide: Box):
    #     slide.box().text("Sometimes, implementation ~emph{is} behavior")
    #
    #     lst = unordered_list(slide.box())
    #     lst.item(show="next+").text("Test that performance is good enough")
    #     lst.item(show="next+").text("Coverage marks")

    # how to test a private method? why would you?!
