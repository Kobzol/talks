from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import COLOR_ORANGE, HideRest, ShowRest, StateCounter, code, code_step, error_message, \
    project, show


def use_dsls(slides: Slides, tips: StateCounter):
    @slides.slide()
    def cargo_build_vs_cargo_test(slide: Box):
        x = 640
        slide.box(x=x, p_bottom=40).text("1) Do a big refactoring")

        width = 1500
        emoji_width = 140
        slide.box(x=x, p_bottom=40, show="next+").text("2) Fix compiler errors")
        row = slide.box(horizontal=True, show="next+")
        row.box(p_right=40).text("3)")
        row.box(width=width).image("images/cargo-build-green.png")
        row.box(width=20)
        row.box(width=emoji_width).image("images/tada.svg")
        row = slide.box(horizontal=True, show="next+", p_top=20)
        row.box(p_right=40).text("4)")
        row.box(width=width).image("images/cargo-test-red.png")
        row.box(width=20)
        row.box(width=emoji_width).image("images/cry.svg")

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
#[test]
fn test_set_priority() {
  let bors = …;
  let pr = PullRequest {
    repo: "foo/bar".to_string(),
    number: 5,
    author: "bot".to_string()  
  };

  let response = bors.post_comment(pr, "@bors priority=5");

  assert_eq!(response.text(), "Priority set to 5");
}
""")

    @slides.slide()
    def use_dsls(slide: Box):
        tips.tip(slide, "Build high-level test APIs")

    @slides.slide()
    def bors_builder(slide: Box):
        project(slide, "bors")

        x = 250
        width = 1600
        code(slide.box(x=x), """
#[derive(derive_builder::Builder, Default, Clone)]
pub struct PR {
    #[builder(default = "foo/bar".to_string())]
    repo: String,
    
    #[builder(default = 1)]
    number: u32,
    …
}
""", width=width)
        code(slide.box(x=x, p_top=50, show="next+"), """
#[test]
fn test_set_priority() {
  let bors = …;
  let pr = PRBuilder::default().author("bot");
  …
}
""", width=width)

    @slides.slide()
    def bon_builder(slide: Box):
        width = 1200
        code(slide.box(), """
#[bon::builder]
fn create_pr(
    repo: Option<&str>,
    number: Option<u32>
) -> PullRequest {
    …
}
""", width=width)

    @slides.slide()
    def bors_helper_fns(slide: Box):
        project(slide, "bors")

        code(slide.box(), """
bors.post_comment("@bors delegate=try");
bors.get_pr()
    .expect_delegated(DelegatedPermission::Try);

bors.post_comment("@bors r+");
bors.get_pr()
    .expect_approved();
""")

    @slides.slide()
    def track_caller(slide: Box):
        project(slide, "bors")

        box = code(slide.box(), """
~#track{#[track_caller]}
pub fn expect_approved(&self) -> &Self {
    assert!(self.get_pr().is_approved());
    self
}
""", use_styles=True, return_codebox=True)

        y = -160
        box = box.inline_box("#track")
        slide.line([
            (box.x("50%").add(200), box.y("0").add(y)),
            (box.x("50%"), box.y("0")),
        ], stroke_width=6, color=COLOR_ORANGE, end_arrow=Arrow(20))
        slide.box(x=box.x("50%").add(220), y=box.y("0").add(y - 50)).text("Very useful!", T(color=COLOR_ORANGE))

        width = 1750
        error_message(slide.box(width=width, p_top=80, show="next+"), "thread '...' panicked at src/test_utils.rs:1066:9:")
        error_message(slide.box(width=width, p_top=20, show="last+"), "thread '...' panicked at src/bors/handlers/review.rs:560:18:")

    @slides.slide()
    def bors_post_comment(slide: Box):
        width = 1700
        code_step(slide.fbox(), """
bors.post_comment("foo/bar", 1, "@bors ping");
bors.post_comment("foo/bar", 1, "@bors try");
bors.post_comment("foo/bar", 1, "@bors r+");
bors.post_comment("foo/bar", 2, "@bors ping");

bors.post_comment("@bors ping");
bors.post_comment_custom("foo/bar", 2, "@bors ping");

bors.post_comment(Comment::new("@bors ping").pr(2));
""", [
            show(4) + [HideRest],
            show(7) + [HideRest],
            show(9) + [HideRest]
        ], width=width)

    width = 1700

    @slides.slide()
    def bors_into_trick_1(slide: Box):
        code(slide.box(), """
struct PrIdentifier { repo: Repository, number: u64 }

// The "Into trick":
fn post_comment<Id: Into<PrIdentifier>>(
    &mut self,
    id: Id,
    text: &str
) { … }
""", width=width)

    @slides.slide()
    def bors_into_trick(slide: Box):
        slide.update_style("code", T(size=40))

        code_step(slide.fbox(), """
struct PrIdentifier { repo: Repository, number: u64 }

impl From<(Repository, u64)> for PrIdentifier {
    fn from((repo, number)): (Repository, u64)) -> Self {
        Self { repo, number }
    }
}

impl From<u64> for PrIdentifier {
    fn from(number: u64) -> Self {
        Self { repo: default_repo(), number }
    }
}

impl From<()> for PrIdentifier {
    fn from(_: ()) -> Self {
        Self { repo: default_repo(), number: 1 }
    }
}
""", [
            show(1) + [HideRest],
            show(7) + [HideRest],
            show(13) + [HideRest],
            [ShowRest]
        ], width=width)


    @slides.slide()
    def bors_comment_api(slide: Box):
        """
        Succinct by default, but extensible.
        """
        width = 1600
        code_step(slide.fbox(), """
// Default repo, default PR
bors.post_comment((), "@bors ping");

// Default repo, PR 2
bors.post_comment(2, "@bors ping");

// Repo foo/bar, PR 2
bors.post_comment(("foo/bar", 2), "@bors ping");

// Custom comment author
bors.post_comment(("foo/bar", 2),
    Comment::new(User::new("user1"), "@bors ping")
);
""", [
            show(2) + [HideRest],
            show(5) + [HideRest],
            show(8) + [HideRest],
            [ShowRest],
        ], width=width)

#     @slides.slide()
#     def cargo_example(slide: Box):
#         project(slide, "Cargo")
#         code(slide.box(), """
# #[test]
# fn cargo_compile_simple() {
#   let p = project()
#     .file("Cargo.toml", &basic_bin_manifest("foo"))
#     .file("src/foo.rs", &main_file("i am foo", &[]))
#     .build();
#
#   p.cargo("build").run();
#
#   assert!(p.bin("foo").is_file());
#
#   p.process(&p.bin("foo")).with_stdout("i am foo\\n").run();
# }
# """)

    @slides.slide()
    def code_review(slide: Box):
        """
        This is exacerbated by not caring enough about test code.
        Test code is still code and we should treat it as such.
        Tests are where you should get clever! Duplication hurts.
        """
        slide.box(p_bottom=40).text("Code reviewers:", T(size=80))
        slide.box(width=800).image("images/code-review-duplicated-code.jpeg")
