from elsie import Arrow, Slides
from elsie.boxtree.box import Box
from elsie.ext import ordered_list, unordered_list
from elsie.text.textstyle import TextStyle as T

from utils import GITHUB_BG_COLOR, HideRest, LOWER_OPACITY, ShowRest, arrow_box, chapter, \
    code, \
    code_step, dimmed_list_item, error_message, last, quotation, show, skip, text_box


def bors(slides: Slides):
    @slides.slide()
    def next_steps(slide: Box):
        chapter(slide, "The weekend project")

    @slides.slide()
    def bors_rewrite_meme(slide: Box):
        slide.box(width=1200).image("images/bors-rewrite-meme.jpg")

    @slides.slide()
    def bors_features(slide: Box):
        slide.update_style("default", T(size=70))
        slide.box(p_bottom=40).text("Bors features", T(size=80))

        lst = ordered_list(slide.box())
        lst.item(show="next+").text("Receiving webhooks")
        lst.item(show="next+").text("Authenticating as a GitHub App")
        lst.item(show="next+").text("Reading Rust team permissions")
        lst.item(show="next+").text("Parsing comments")
        lst.item(show="next+").text("Try builds")
        lst.item(show="next+").text("Refreshing PR status")
        lst.item(show="next+").text("Setting PR priority")
        lst.item(show="next+").text("Delegating approval rights")
        lst.item(show="next+").text("(Un)approving PRs")

        slide.box(show="next+", x=1300, y=475).text(
            "10. Tree closing/opening",
            rotation=90
        )
        slide.box(show="next+", x=0, y=500).text(
            "11. Rollups",
            rotation=-90
        )
        slide.box(show="next+", x=1000, y=575).text("12. Checking PR")
        slide.box(show="last+", x=1360, y=750).text("mergeability", rotation=90)
        slide.box(show="next+", x=100, y=100).text("13. Merge queue…")

    @slides.slide()
    def sqlx(slide: Box):
        slide.update_style("code", T(size=44))
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
        slide.box(x="[50%]", y="[50%]", width=1600, z_level=999, show="next+").image(
            "images/sqlx-error.png")

    @slides.slide()
    def strong_typing_lock(slide: Box):
        """
        Double merge bug, parallel deployment
        """
        slide.update_style("code", T(size=50))
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
""".strip(), use_styles=True, escape_char=("~", "#", "#"))

    @slides.slide()
    def bors_summary_2(slide: Box):
        slide.box(p_bottom=60).text("How to implement bors", T(size=80))

        width = 1400
        slide.box(width=width, p_bottom=20).text("First 95%: implement a correct merge queue",
                                                 T(align="left"))
        slide.box(width=width, show="next+").text("Remaining 95%: deal with GitHub's quirks",
                                                  T(align="left"))

    @slides.slide()
    def github_adversarial(slide: Box):
        quotation(slide.box(), """GitHub is an adversarial, eventually inconsistent chaotic system
masquerading as a git forge.""", "(author unknown)")

    @slides.slide()
    def favourite_things(slide: Box):
        """
        https://rust-lang.zulipchat.com/#narrow/channel/496228-t-infra.2Fbors/topic/Bors.20approved.20outdated.20commit.20while.20it.20shouldn.27t.20have.3F/with/576808943
        https://rust-lang.zulipchat.com/#narrow/channel/242791-t-infra/topic/Bors.20posting.20success.20message.20a.20dozen.20times/with/593574999
        """
        row = slide.box(horizontal=True, y=120)
        row.box(width=200, p_right=50).image("images/github-logo.png")
        row.box(y=-80, width=980).image("images/chat-bubble.svg").text(
            "These are a few of my favourite things…", T(size=50)
        )
        lst = unordered_list(slide.box(y=400))
        dimmed_list_item(lst, "Not delivering a webhook", show=2)
        dimmed_list_item(lst, "Delivering a webhook 15 minutes late", show=3)
        dimmed_list_item(lst, "Delivering a webhook ~emph{12 hours} late", show=4)
        dimmed_list_item(lst,
                         " ̶S̶p̶r̶e̶a̶d̶i̶n̶g̶ ̶l̶i̶e̶s̶  Returning inconsistent data from the API",
                         show=5)
        dimmed_list_item(lst, "Non-idempotent retries", show=9, highlight_steps=5, last=True)

        # slide.box(x="[50%]", y="[50%]", width=1700, show="5").image("images/bors-late-webhook.png")
        slide.box(x="[50%]", y="[50%]", width=1700, show="6-8").image("images/bors-github-bug.png")

        bg = "#222222"
        slide.box(x=130, y=640, width=1650, height=100, show="6").rect(bg_color=bg)
        slide.box(x=130, y=725, width=1650, height=100, show="6-7").rect(bg_color=bg)

        overlay = slide.box(x="[50%]", y="[50%]", width=1000, show="10-13").rect(bg_color="white",
                                                                                 color="black",
                                                                                 stroke_width=8)
        box = overlay.box(width="100%", p_x=50, p_y=100)
        box.box(width="100%", show="10+").text("~bold{bors}:      post comment", T(align="left"))
        box.box(width="100%", show="11+").text("~bold{GitHub}: 500 Internal Server Error", T(align="left"))
        box.box(width="100%", show="12+").text("~bold{bors}:      post comment (retry)", T(align="left"))
        box.box(width="100%", show="13+").text("~bold{GitHub}: 200 OK", T(align="left"))
        slide.box(x="[50%]", y="[50%]", width=1400, show="14+").image(
            "images/bors-duplicated-comment.png")
        slide.box(x=1200, y=700, width=400, show="last+").image("images/huh-meme.png")

    @slides.slide()
    def cost_of_missed_webhooks(slide: Box):
        slide.box(p_bottom=60).text("Cost of missed webhooks", T(size=80))

        lst = ordered_list(slide.box())
        lst.item(show="next+").text("Prepare a merge commit")
        lst.item(show="next+").text("Start CI jobs")
        lst.item(show="next+").text("Wait 3 hours for CI to succeed")
        lst.item(show="next+").text("Miss CI completion webhook", T(color="red"))
        lst.item(show="next+").text("Wait 3 more hours until timeout kicks in")
        lst.item(show="next+").text("GOTO 1.")

    @slides.slide()
    def polling(slide: Box):
        slide.box(p_bottom=40).text("Checking GitHub state", T(size=80))
        slide.box().text("Edge-triggered (webhooks) +")
        slide.box(show="next+").text("Level-triggered (periodic polling)")

    width = 1800

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def bors_kindergarten(slide: Box):
        slide.box(width=1700).image("images/bors-kindergarten.png")

    def integration_tests(slides: Slides, index: int):
        @slides.slide()
        def tests_db(slide: Box):
            slide.update_style("default", T(size=70))
            slide.box(p_bottom=60).text("Bors integration tests", T(size=80))

            lst = unordered_list(slide.box())
            items = ["Database", "GitHub", "Async"]
            for (i, item) in enumerate(items):
                style = "default"
                label = None
                if i < index:
                    style = T(opacity=LOWER_OPACITY)
                elif i > index:
                    style = T(color="white")
                    label = ""
                lst.item(label=label).text(item, style)

    integration_tests(slides, index=0)

    @slides.slide()
    def db_value(slide: Box):
        code_step(slide.fbox(), """
struct BorsService {
    db: Postgres
}

#[test]
fn bors_service() {
    let service = BorsService {
        db: ???
    };
    …
}
""", [
            show(3) + [HideRest],
            [ShowRest]
        ], width=width)

    @slides.slide()
    def db_trait(slide: Box):
        """
        Architectural aspect (are you gonna need to switch DBs?) vs introducing a trait *just* for
        tests.
        Maybe it's Box<dyn Database>, but that's not much better.
        """
        code_step(slide.fbox(), """
trait Database { … }

struct InMemoryDb {
    pull_requests: HashMap<u32, PullRequest>
}

impl Database for InMemoryDb { … }
""", [
            show(1) + [HideRest],
            show(7) + [HideRest],
        ], width=width)

    @slides.slide()
    def postgres_production_error(slide: Box):
        row = slide.box(p_bottom=40, horizontal=True)
        for _ in range(3):
            row.box().image("images/tada.svg")
        slide.box(width=1700).image("images/postgres-int-datatype-error.png")

    @slides.slide()
    def sqlx_test(slide: Box):
        """
        Don't use SQLite vs Postgres.
        """
        code(slide, """
#[sqlx::test]
async fn bors_service(db: PgPool) {
    let bors = BorsService {
        db
    };
    …
}
""", width=width)

    #     @slides.slide()
    #     def isnt_that_slow(slide: Box):
    #         """
    #         Skip slow tests locally.
    #         It gives me confidence in the test suite.
    #         """
    #         slide.box().text("Isn't that slow?")
    #
    #         slide.box(p_top=40, show="next+").text("~400 integration tests in bors:", escape_char="#")
    #         lst = unordered_list(slide.box())
    #         lst.item().text("~20s (debug)", escape_char="#")
    #         lst.item().text("~8s (release)", escape_char="#")
    #
    #     @slides.slide()
    #     def postgres_in_memory(slide: Box):
    #         """
    #         Wouldn't recommend using in-memory SQlite instead though.
    #         """
    #         width = 1050
    #         code_step(slide.fbox(), """
    # services:
    #   db:
    #     image: postgres:16.9
    #     # Turn off durability
    #     command: -c fsync=off
    #     # Use RAMdisk for storage
    #     tmpfs:
    #       - /var/lib/postgresql/data
    # """, [
    #             show(3) + [HideRest],
    #             show(5) + [HideRest],
    #             [ShowRest],
    #         ], language="python", width=width)
    #
    #     @slides.slide()
    #     def be_pragmatic(slide: Box):
    #         slide.box().text("Be pragmatic!")

    # @slides.slide()
    # def bors_lgtm(slide: Box):
    #     slide.box(width=1400).image("images/lgtm.png")

    @slides.slide()
    def bors_db_error(slide: Box):
        slide.box(p_bottom=40).text("Production migration error:")
        slide.box(width=1800).image("images/postgres-not-null-error.png")

    @slides.slide()
    def bors_wrong_migration(slide: Box):
        slide.box(p_bottom=40).text("Oops")
        slide.box(width=1600).image("images/bors-wrong-migration.png")

    # Reduce stress of future people working on the codebase
    @slides.slide()
    def caution(slide: Box):
        slide.box(p_bottom=40).text("Add a warning for next time:")
        slide.box().image("images/no-default-caution.png")
        # slide.box(p_top=40, show="next+").text("…is that all we can do?")

    @slides.slide()
    def cargo_sqlparser(slide: Box):
        slide.box(width=1600).image("images/cargo-add-sqlparser.png")

    #     @slides.slide()
    #     def migration_test(slide: Box):
    #         slide.update_style("code", T(size=32))
    #
    #         width = 1700
    #         code_step(slide.fbox(), """
    # #[test]
    # fn check_non_null_column_without_default() {
    #     let root = env!("CARGO_MANIFEST_DIR");
    #     let migrations = PathBuf::from(root).join("migrations");
    #     for file in std::fs::read_dir(migrations).unwrap() {
    #         let file = file.unwrap();
    #         if file.path().extension() == Some(OsStr::new("sql")) {
    #             let contents =
    #                 std::fs::read_to_string(&file.path()).unwrap();
    #
    #             let ast = Parser::parse_sql(&PostgreSqlDialect {}, &contents).unwrap();
    #             let mut visitor = CheckNotNullWithoutDefault::new();
    #             ast.visit(&mut visitor);
    #
    #             if let Some(error) = visitor.compute_error() {
    #                 panic!(
    #                     "Migration {} contains error: {error}",
    #                     file.path().display()
    #                 );
    #             }
    #         }
    #     }
    # }
    # """, [
    #             show(4) + skip(18) + last(1),
    #             show(9) + skip(11) + last(3),
    #             [ShowRest]
    #         ], width=width)

    @slides.slide()
    def visitor_code(slide: Box):
        slide.update_style("code", T(size=32))

        width = 1700
        code_step(slide.fbox(), """
impl Visitor for CheckNotNullWithoutDefault {
    fn pre_visit_statement(&mut self, statement: &Statement)
        -> ControlFlow<Self::Break> {
        let Statement::AlterTable {
            operations, name, ..
        } = statement else {
            return ControlFlow::Continue(());
        };
        for op in operations {
            match op {
                AlterTableOperation::AlterColumn { column_name, op } => match op {
                    AlterColumnOperation::SetNotNull => {
                        self.columns_set_to_not_null
                            .insert((name.clone(), column_name.clone()));
                    }
                    AlterColumnOperation::SetDefault { .. } => {
                        self.columns_set_default_value
                            .insert((name.clone(), column_name.clone()));
                    }
                    _ => {}
                },
                _ => {}
            }
        }
        ControlFlow::Continue(())
    }
}
""", [
            # show(8) + skip(16) + last(3),
            [ShowRest]
        ], width=width)

    # @slides.slide()
    # def end_to_end_tests(slide: Box):
    #     slide.box(width=1600).image("images/bors-migration-data.png")

    #     @slides.slide()
    #     def migration_data_apply(slide: Box):
    #         slide.update_style("code", T(size=32))
    #         code_step(slide.fbox(), """
    # #[sqlx::test(migrations = false)]
    # async fn apply_migrations_with_test_data(pool: PgPool) -> anyhow::Result<()> {
    #     let migrations = get_sorted_up_migrations();
    #
    #     for migration_path in migrations {
    #         let migration_sql = std::fs::read_to_string(&migration_path)?;
    #
    #         pool.execute(&*migration_sql).await?;
    #
    #         let test_data_path = get_test_data_path(&migration_path);
    #         let test_data = std::fs::read_to_string(&test_data_path)?;
    #
    #         pool.execute(&*test_data).await.unwrap_or_else(|e| {
    #             panic!(
    #                 "Failed to apply migration test data {:?}: {}",
    #                 test_data_path, e
    #             )
    #         });
    #     }
    #     Ok(())
    # }""", [
    #             show(5) + skip(13) + last(3),
    #             [ShowRest]
    #         ])

#     @slides.slide()
#     def migration_data_test(slide: Box):
#         slide.update_style("code", T(size=40))
#         code(slide.box(), """
# #[test]
# fn check_migrations_have_sample_data() {
#     let migrations = get_sorted_up_migrations();
#     assert!(!migrations.is_empty());
#     for migration_path in migrations {
#         let test_data_path = get_test_data_path(&migration_path);
#
#         assert!(
#             test_data_path.exists(),
#             "Migration {:?} does not have a test data file at {:?}.
#             Add a test data file there that fills some test data
#             into the database after that migration is applied.",
#             migration_path,
#             test_data_path
#         );
#     }
# }
# """)

    integration_tests(slides, index=1)

    @slides.slide()
    def bors_http_mock(slide: Box):
        """
        Why not test binary? We'll see later.
        Mock at outside boundaries.
        Makes the code simpler.
        """
        slide.update_style("default", T(size=60))
        slide.update_style("code", T(size=70))

        row = slide.box(horizontal=True)

        desc_y = row.y("0%").add(-100)

        def col(text: str, width: int, offset: int = 0) -> Box:
            col = row.box(width=width)
            slide.box(x=col.x("0").add(offset), y=desc_y).text(text, T(size=44))
            return col

        col("(? KLoc)", 120, offset=-10).box(width=120).image("images/github-logo.png")
        arrow1 = row.box(width=400)
        arrow_box(arrow1, "Webhooks\n(HTTP)", size=50)

        row.box(width=20)
        box = col("(28 KLoc)", 180)
        text_box(box, "bors", size=40)
        row.box(width=50)

        arrow3 = row.box(width=400)
        arrow_box(arrow3, "API requests\n(HTTP)", both_sides=True, size=50)
        col("(? KLoc)", 120, offset=-10).box(width=120).image("images/github-logo.png")

        box = slide.box(width="100%", p_top=200)
        lst = unordered_list(box.box(show="2-6"))
        dimmed_list_item(lst, "Reimplement GitHub", 2, highlight_steps=1)
        code_box = slide.box(x="[50%]", y="[50%]", show="3")
        code_box.rect(color="black", stroke_width=8)
        code(code_box, """
def github(request):
    sleep(randint(2, 5))
    return 500
""", language="python")

        dimmed_list_item(lst, "Deploy GitHub locally", 4)
        dimmed_list_item(lst, "Test on real GitHub repositories", 5)
        lst.item(show="6").text("Mock HTTP GitHub endpoints")

        wrapper = box.overlay(show="next+")
        wrapper.box(p_bottom=40).text("Bors tests:")
        row = wrapper.box(horizontal=True)
        text_box(row.box(), "axum", size=40)
        arrow4 = row.box(width=500)
        arrow_box(arrow4, "Webhooks\n(HTTP)", size=50)
        text_box(row.box(width=180), "bors", size=40)
        row.box(width=50)
        arrow5 = row.box(width=400)
        arrow_box(arrow5, "API requests\n(HTTP)", both_sides=True, size=50)
        text_box(row.box(), "wiremock", size=40)

#     @slides.slide()
#     def wiremock_example_1(slide: Box):
#         slide.update_style("code", T(size=44))
#         code(slide.box(), """
# Mock::given(method("POST"))
#     .and(path_regex("^/app/installations/\\d+/access_tokens$"))
#     .respond_with(
#         ResponseTemplate::new(200)
#             .set_body_json(InstallationToken::default())
#     )
#     .mount(mock_server)
#     .await;
# """)

    @slides.slide()
    def wiremock_example_2(slide: Box):
        slide.update_style("code", T(size=40))

        width = 1800
        code_step(slide.fbox(), """
Mock::given(method("GET"))
    .and(path_regex(format!("^/repos/{repo_name}/pulls/([0-9]+)$")))
    .respond_with(move |req: &Request| {
        let num = req.url.path_segments().unwrap().next_back().unwrap();
        let pr_number: u64 = num.parse().unwrap();
        let pull_request_error = repo.lock().error;
        if pull_request_error {
            ResponseTemplate::new(500)
        } else if let Some(pr) = repo.lock().prs.get(&pr_number) {
            ResponseTemplate::new(200).set_body_json(
                GitHubPullRequest::from(pr)
            )
        } else {
            ResponseTemplate::new(404)
        }
    })
    .mount(mock_server)
    .await;
""", [
            show(3) + skip(12) + last(3),
            show(5) + skip(10) + last(3),
            [ShowRest]
        ], width=width)

    integration_tests(slides, index=2)

    @slides.slide()
    def spawn(slide: Box):
        """
        Async usage and control in binaries vs libraries.
        """
        code(slide.box(), """
async fn yolo() {
    // Good luck testing this! xoxo
    tokio::task::spawn(async move {
        …
    });
}
""")

    @slides.slide()
    def bg_job_1(slide: Box):
        width = 1700
        code_step(slide.fbox(), """
use tokio::time::interval;

async fn background_job() {
    // Duration might have to be adjusted for tests 
    let mut interval = interval(Duration::from_secs(30));
    loop { // The process runs forever
    loop {
        interval.tick().await;
        do_work().await;
        do_work().await; // Not synchronized
    }
}
""", [
            show(3) + skip(1) + show(1, start=4) + show(3, start=6) + last(2),
            show(5) + show(3, start=6) + last(2),
            show(6) + show(2, start=7) + last(2),
            show(6) + show(1, start=7) + show(3, start=9),
        ], width=width)

    @slides.slide()
    def bg_job_2(slide: Box):
        slide.update_style("code", T(size=40))
        width = 1700
        box = code_step(slide.fbox(), """
async fn background_job(mut rx: Receiver<()>) {
    // Explicit control + proper cleanup
    while let Some(msg) = rx.recv().await {
        do_work().await;
    }
}

async fn test() {
    let (tx, rx) = mpsc::channel(10);
    task::spawn(background_job(rx));

    do_something().await;
    tx.send(()).await;
    ensure_work_was_done().await;
}
""", [
            show(1) + [None] + show(5, start=2) + [HideRest],
            show(6) + [HideRest],
            [ShowRest]
        ], width=width, return_box=True)

        l1 = box.line_box(12)
        l2 = box.line_box(13)

        x_offset = 50
        x_start = -300
        arrow = Arrow(20)
        slide.fbox(x=0, y=0, show="4").line([
            (l1.x("100%").add(x_start), l1.y("50%")),
            (l1.x("100%").add(x_start + x_offset), l1.y("50%")),
            (l1.x("100%").add(x_start + x_offset), l2.y("50%")),
            (l1.x("100%").add(x_start), l2.y("50%")),
        ], stroke_width=6, color="red", start_arrow=arrow, end_arrow=arrow)
        slide.box(
            x=l1.x("100%").add(x_start + x_offset + 50),
            y=l1.y("0"),
            show="last+"
        ).text("Possible race!", T(color="red"))

    @slides.slide()
    def finish_something(slide: Box):
        slide.box().text("How to ensure that something ~emph{completes} reliably?")

        lst = unordered_list(slide.box(p_top=80))
        row = lst.item(show="next+")
        row = row.box(horizontal=True)
        row.box(p_right=40).text('Arbitrarily add sleeps throughout tests until it "works"',
                                 "small")
        row.box(width=64).image("images/cross.svg")
        lst.item(show="next+").text("Synchronize through some external state", "small")
        lst2 = lst.ul()
        lst2.item().text("Database, HTTP endpoint, file on disk, …", "small")
        row = lst.item(show="next+", p_top=40)
        row = row.box(horizontal=True)
        row.box(y=0).text("Use coverage marks", "small")
        row.box(width=25)
        row.box(y=-20, width=120).image("images/matklad.png")

#         width = 1700
#         code_step(slide.fbox(show="4-6", y=200), """
# async fn unapprove() {
#     …
#     ctx.post_comment("@bors r-").await?;
#
#     // Bot comment acts as a synchronization point
#     assert_eq!(
#         ctx.get_next_comment_text().await?,
#         "Commit pr-1-sha has been unapproved."
#     );
#
#     ctx.get_pr().await.expect_unapproved();
# }
# """, [
#             show(3) + skip(8) + last(1),
#             show(9) + skip(2) + last(1),
#             [ShowRest]
#         ], show_start=4, width=width)

    @slides.slide()
    def coverage_marks(slide: Box):
        """
        Inspects implementation.
        https://ferrous-systems.com/blog/coverage-marks
        Dangers of global/thread-local variables - better use context.
        """
        slide.update_style("code", T(size=40))
        code_step(slide.fbox(y=120), """
#[cfg(test)]
pub static WAIT_FOR_WORKFLOW_STARTED = TestSyncMarker::new();

fn insides_of_bors() {
    …
    BorsRepositoryEvent::WorkflowStarted(payload) => {
        handle_workflow_started(repo, db, payload).await?;

        #[cfg(test)]
        WAIT_FOR_WORKFLOW_STARTED.mark();
    }
    …
}

async fn test(ctx: TestCtx) {
    ctx.start_workflow().await;
    WAIT_FOR_WORKFLOW_STARTED.sync().await;
    ctx.assert_workflow_started().await;
}
""", [
            show(2) + [HideRest],
            show(13) + [HideRest],
            [ShowRest]
        ])

#     @slides.slide()
#     def missing_error(slide: Box):
#         code(slide.box(), """
# async fn test_approve() -> anyhow::Result<()> {
#     let ctx = start_bors().await;
#     ctx.post_comment("@bors r+").await?;
#     …
#
#     Ok(())
# }
# """)
#         width = 1750
#         error_message(slide.box(width=width, p_top=40, show="next+"),
#                       "Error: Connection reset by peer (os error 104)")
#         error_message(slide.box(width=width, p_top=20, show="next+", z_level=999), """thread '<unnamed>' (269367) panicked at src/lib.rs:229:25:
# Cannot approve PR 1 because of …""")
#
#     @slides.slide()
#     def test_wrapper(slide: Box):
#         """
#         This used to be painful without async closures - had to pass context by value and return it.
#         """
#         slide.update_style("code", T(size=44))
#         code_step(slide.fbox(), """
# async fn run_test<F>(test_fn: F) -> anyhow::Result<()>
# where
#     F: AsyncFnOnce(&mut TestCtx) -> anyhow::Result<()>
# {
#     let mut ctx = create_ctx().await;
#
#     // or test_fn(&mut ctx).catch_unwind()
#     let res1 = test_fn(&mut ctx).await;
#     let res2 = ctx.finish().await;
#     combine_results(res1, res2)
# }
#
# #[tokio::test]
# async fn test() {
#     run_test(async |ctx| {
#         ctx.post_comment("@bors r+").await?;
#         Ok(())
#     }).await;
# }
# """, [
#             show(4) + skip(6) + show(1, start=10) + [HideRest],
#             show(11) + [HideRest],
#             [ShowRest]
#         ])

    @slides.slide()
    def octocrab_bug(slide: Box):
        """
        https://kobzol.github.io/rust/2025/12/30/investigating-and-fixing-a-nasty-clone-bug.html
        """
        slide.update_style("code", T(size=50))

        # The code snippet ends with `x` to avoid stripping the blank lines at the end
        code_step(slide.fbox(), """
PATCH /repos/a/b/git/refs/heads/main HTTP/1.1
x-github-api-version: 2022-11-28
content-type: application/json
authorization: Bearer foo

{"sha": "foo", "force": true}

HTTP/1.1 500 Internal Server Error

PATCH /repos/a/b/git/refs/heads/main HTTP/1.1
x-github-api-version: 2022-11-28
content-type: application/json
authorization: Bearer foo


x""", [
            show(6) + [HideRest],
            show(8) + [HideRest],
            show(14) + [HideRest],
        ], language="c")
        slide.box(x=275, y=875, show="next+").text("???", T(color="red", bold=True, size=80))

    @slides.slide()
    def octocrab_bug_code(slide: Box):
        slide.update_style("code", T(size=30))
        box = code(slide.box(), """
fn clone_request(&mut self, req: &Request<OctoBody>) -> Option<Request<OctoBody>> {
    match self {
        RetryConfig::None => None,
        _ => {
            // `Request` can't be cloned
            let mut new_req = Request::builder()
                .uri(req.uri())
                .method(req.method())
                .version(req.version());

            for (name, value) in req.headers() {
                new_req = new_req.header(name, value);
            }

            let body = req.body().clone();

            let new_req = new_req.body(body).expect(
                "This should never panic, as we are cloning a components from existing request",
            );
            Some(new_req)
        }
    }
}
""", return_box=True)
        linebox = box.line_box(14)
        slide.box(
            x=linebox.x("45%"),
            y=linebox.y("0%").add(-15),
            show="next+"
        ).text("Can't be cloned, huh? Watch me!", T(color="red", size=50))

    @slides.slide(bg_color=GITHUB_BG_COLOR)
    def octocrab_fix_pr(slide: Box):
        """
        https://github.com/XAMPPRocky/octocrab/pull/842
        Fixed a two year old retry bug in octocrab.
        """
        slide.box().image("images/octocrab-fix-pr.png")

    # @slides.slide()
    # def inspiration(slide: Box):
    #     slide.box(p_bottom=40).text("Deterministic Simulation Testing")
    #     lst = unordered_list(slide.box())
    #     lst = lst.ul()
    #     lst.item().text("TigerBeetle")
    #     lst.item().text("antithesis")

    @slides.slide()
    def final_bors_test(slide: Box):
        slide.update_style("code", T(size=38))
        code(slide.box(), """
#[sqlx::test]
async fn unapprove_lacking_permissions(pool: sqlx::PgPool) {
    run_test(pool, async |ctx| {
        ctx.approve(()).await?;
        ctx.post_comment(Comment::from("@bors r-")
            .with_author(User::unprivileged())
        ).await?;
        insta::assert_snapshot!(
            ctx.get_next_comment_text(()).await?,
            @"@unprivileged-user: :key:
            Insufficient privileges: not in review users"
        );

        ctx
            .get_pr(())
            .await
            .expect_approved_by(&User::default_pr_author().name);
        Ok(())
    })
    .await;
}
""")

    @slides.slide()
    def test_stats(slide: Box):
        slide.box(p_bottom=40).text("Bors has a lot of these!", T(size=80))
        slide.box(p_bottom=40).text("~420 tests", escape_char="#")
        slide.box(show="next+").text("~15k lines of tests & test helpers (half of the codebase)", escape_char="#")

    @slides.slide()
    def test_compile_time(slide: Box):
        slide.box(p_bottom=60).text("Bors test compile times", T(size=80))

        row = slide.box(p_bottom=40, horizontal=True)
        row.box(p_right=20).text("Lot of async + lot of generics = ")
        row.box().image("images/cry.svg")
        slide.box(p_bottom=40, show="next+").text("Incremental test rebuild = ~10s",
                                                  escape_char="#")

        row = slide.box(horizontal=True, show="next+")
        row.box().text("(")
        row.box().image("images/nerd.svg")
        row.box().image("images/water-pistol.svg")
        row.box().text(")")
