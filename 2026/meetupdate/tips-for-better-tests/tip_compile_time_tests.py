from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import StateCounter, code, project, render_rustc_error


def compile_time_tests(slides: Slides, tips: StateCounter):
    @slides.slide()
    def compile_time_tests(slide: Box):
        tips.tip(slide, "Leverage compile-time tests")

    @slides.slide()
    def compile_time_tests_types(slide: Box):
        codebox = code(slide.box(), """
fn merge_branch(repo: ~#test1{GitHubRepo}, name: ~#test2{String})
    -> anyhow::~#test3{Result}<MergedBranch> {
    …
}
""", use_styles=True, return_codebox=True)

        positions = [
            (700, 200),
            (1200, 200),
            (1200, 700),
        ]

        for (i, (x, y)) in zip(range(1, 4), positions):
            box = codebox.inline_box(f"#test{i}")
            top = y < 500
            target_y = box.y("0%") if top else box.y("100%")
            x_offset = -150 if top else 20
            slide.fbox(show="2", x=0, y=0).line((
                (x, y + 50),
                (box.x("50%"), target_y)
            ), stroke_width=6, end_arrow=Arrow(20))
            slide.box(x=x + x_offset, y=y, show="2").text("Test")

    @slides.slide()
    def strong_typing_pr_number(slide: Box):
        code(slide.box(), """
fn send_comment(
    repo: GithubRepo,
    number: PullRequestNumber,
    comment: Comment
) {
   …
}
""")

    @slides.slide()
    def strong_typing_lock(slide: Box):
        code(slide.fbox(show="1", x="[50%]", y="[50%]"), """
fn attempt_merge(
    branch_name: &str,
    head_sha: &CommitSha,
    base_sha: &CommitSha,
    merge_message: &str,
    _merge_lock_is_held: &ExclusiveLockProof,
) -> anyhow::Result<MergeResult> {
    …
}
""")
        code(slide.fbox(show="2", x="[50%]", y="[50%]"), """
~code_muted#fn attempt_merge(
    branch_name: &str,
    head_sha: &CommitSha,
    base_sha: &CommitSha,
    merge_message: &str,#
    _merge_lock_is_held: &ExclusiveLockProof,
~code_muted#) -> anyhow::Result<MergeResult> {
    …
}#
""", use_styles=True, escape_char=("~", "#", "#"))

    @slides.slide()
    def sqlx(slide: Box):
        slide.update_style("code", T(size=44))
        project(slide, "bors")
        code(slide.box(), """
let build_id = sqlx::query_scalar!(
    r#"
INSERT INTO build (repository, branch, commit_sha, parent, state)
VALUES ($1, $2, $3, $4, $5)
"#,
    repo as &GithubRepoName,
    branch,
    commit_sha.0,
    parent.0,
    BuildStatus::Pending as BuildStatus
)
.fetch_one(executor)
.await?;
""")
        slide.box(x="[50%]", y="[50%]", width=1600, z_level=999, show="next+").image("images/sqlx-error.png")

    @slides.slide()
    def static_size_assert(slide: Box):
        """
        static_assertions crate.
        """
        slide.update_style("code", T(size=40))

        project(slide, "Rust compiler")
        rust_code = """
pub struct Attribute {
    pub kind: AttrKind,
    pub id: AttrId,
    pub style: AttrStyle,
    pub span: Span,
}

const AssertAttributeSize: [(); 32] = 
    [(); std::mem::size_of::<Attribute>()];
"""
        code(slide.box(), rust_code)

        extended_code = """
struct AttrKind([u8; 16]);
struct AttrId([u8; 24]);
struct AttrStyle([u8; 4]);
struct Span([u8; 4]);
""" + rust_code
        render_rustc_error(slide.box(show="next+", p_top=60), extended_code, style=T(size=26))
