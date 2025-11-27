from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import StateCounter, aka, code, code_step, project, show, HideRest, ShowRest, skip, arrow_box, \
    text_box, dimmed_list_item, last


def test_the_real_thing(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_the_real_thing(slide: Box):
        """
        Maintain confidence in tests.
        """
        tips.tip(slide, "Test the ~emph{real thing}")
        aka(slide, "Don't (over)use mocks", width=None)

    @slides.slide()
    def kelvin_pr_diff(slide: Box):
        slide.box(width=800).image("images/pr-diff.png")

    @slides.slide()
    def useless_mock_tests(slide: Box):
        slide.box(width=1800).image("images/tests-with-mock.png")

    @slides.slide()
    def arthas(slide: Box):
        box = slide.box(width=1400).image("images/arthas.png")
        # slide.line([
        #     (box.x("35%"), box.y("30%")),
        #     (box.x("35%").add(180), box.y("30%")),
        # ], color="red", stroke_width=8)
        slide.line([
            (box.x("53%"), box.y("46%")),
            (box.x("53%").add(80), box.y("46%")),
        ], color="red", stroke_width=8)
        slide.box(x=box.x("45%"), y=box.y("50%")).text("TEST SUITE",
                                                       T(color="red", bold=True, size=50))
        # slide.box(x=box.x("34%"), y=box.y("12%")).text("ME", T(color="red", bold=True, size=50))

    width = 1800

    @slides.slide()
    def db_value(slide: Box):
        code_step(slide.fbox(), """
struct BorsService {
    db: sqlx::PgPool
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
        code_step(slide.box(y=100, width="100%", height=400), """
trait Database { … }

struct BorsService<DB: Database> {
    db: DB
struct BorsService {
    db: Box<dyn Database>
}
""", [
            show(1) + skip(4),
            show(4) + last(1),
            show(4) + last(1),
            show(4) + last(1),
            show(2) + show(3, start=4),
        ], width=width)

        code_step(slide.box(width="100%", p_top=80, show="3-4"), """
fn run_service<DB: Database>(service: BorsService<DB>) {}

fn start_workflow<DB: Database>(
    service: BorsService<DB>,
    id: WorkflowId
) {}
""", [
            [0] + [HideRest],
            [ShowRest]
        ], show_start=3)

    @slides.slide()
    def mocked_db(slide: Box):
        code_step(slide.fbox(), """
struct InMemoryDb {
    pull_requests: HashMap<u32, PullRequest>
}
impl Database for InMemoryDb { … }

#[test]
fn test_bors() {

    let service = BorsService {
        db: InMemoryDb::default()
    };
    …

}
""", [
            show(3) + [HideRest],
            show(4) + [HideRest],
            [ShowRest]
        ], width=width)

    @slides.slide()
    def mocked_db_shared(slide: Box):
        code(slide.box(), """
struct InMemoryDb {
    pull_requests: Mutex<HashMap<u32, PullRequest>>
}
impl Database for Arc<InMemoryDb> { … }

#[test]
fn test_bors() {
    let db = Arc::new(InMemoryDb::default());
    let service = BorsService {
        db: db.clone()
    };
    …
    assert!(db.pull_requests().lock()…);
}
""", width=width)

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
        project(slide, "bors")
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
#     def custom_db_test(slide: Box):
#         slide.update_style("code", T(size=40))
#         code_step(slide.fbox(), """
# async fn new_postgres_db() -> anyhow::Result<TestDb> {
#     let db_url = get_env("TEST_DATABASE_URL")?;
#
#     let pool = PgPool::connect(&db_url)?;
#     let db_name = format!("db{}", Uuid::new_v4());
#     pool.execute(&format!("CREATE DATABASE {db_name}"), &[])?;
#
#     let test_db_url = make_db_url(db_url, &db_name);
#     let pool = PgPool::connect(test_db_url.as_str());
#     Ok(TestDb { pool, db_url, db_name })
# }
#
# impl TestDb {
#     fn finish(self) -> anyhow::Result<()> {
#         drop(self.pool);
#         let pool = PgPool::connect(&self.db_url).unwrap();
#         pool.execute(&format!("DROP DATABASE {}", self.db_name), &[])?;
#         Ok(())
#     }
# }
# """, [
#             show(2) + skip(8) + [10] + [HideRest],
#             show(6) + skip(4) + [10] + [HideRest],
#             show(11) + [HideRest],
#             [ShowRest]
#         ], width=width)

    @slides.slide()
    def isnt_that_slow(slide: Box):
        """
        Skip slow tests locally.
        It gives me confidence in the test suite.
        """
        slide.box().text("Isn't that slow?")

        slide.box(p_top=40, show="next+").text("~250 integration tests in bors:", escape_char="#")
        lst = unordered_list(slide.box())
        lst.item().text("~15s (debug)", escape_char="#")
        lst.item().text("~8s (release)", escape_char="#")

    @slides.slide()
    def postgres_in_memory(slide: Box):
        """
        Wouldn't recommend using in-memory SQlite instead though.
        """
        width = 1050
        code_step(slide.fbox(), """
services:
  db:
    image: postgres:16.9
    # Turn off durability
    command: -c fsync=off
    # Use RAMdisk for storage
    tmpfs:
      - /var/lib/postgresql/data
""", [
            show(3) + [HideRest],
            show(5) + [HideRest],
            [ShowRest],
        ], language="python", width=width)

    @slides.slide()
    def be_pragmatic(slide: Box):
        slide.box().text("Be pragmatic!")

    @slides.slide()
    def bors_http_mock(slide: Box):
        """
        Why not test binary? We'll see later.
        Mock at outside boundaries.
        Makes the code simpler.
        """
        slide.update_style("default", T(size=60))

        row = slide.box(horizontal=True)

        desc_y = row.y("0%").add(-100)

        def col(text: str, width: int, offset: int = 0) -> Box:
            col = row.box(width=width)
            slide.box(x=col.x("0").add(offset), y=desc_y).text(text, T(size=44))
            return col

        col("(? KLoc)", 120, offset=-10).box(width=120).image("images/github-logo.png")
        arrow1 = row.box(width=300)
        arrow_box(arrow1, "Webhooks\n(HTTP)", size=50)

        box = col("(0.2 KLoc)", 120)
        text_box(box, "bors (bin)", size=40)
        arrow2 = row.box(width=100)
        arrow_box(arrow2)

        box = col("(17 KLoc)", 120)
        text_box(box, "bors (lib)", size=40)

        arrow3 = row.box(width=400)
        arrow_box(arrow3, "API requests\n(HTTP)", both_sides=True, size=50)
        col("(? KLoc)", 120, offset=-10).box(width=120).image("images/github-logo.png")

        box = slide.box(width="100%", p_top=200)
        lst = unordered_list(box.box(show="2-5"))
        items = [
            "Reimplement GitHub",
            "Deploy GitHub locally",
            "Test on real GitHub repositories",
            "Mock HTTP GitHub endpoints"
        ]
        for (index, item) in enumerate(items, start=2):
            if item == items[-1]:
                lst.item(show=index).text(item)
            else:
                dimmed_list_item(lst, item, index)

        wrapper = box.overlay(show="next+")
        wrapper.box(p_bottom=40).text("Bors tests:")
        row = wrapper.box(horizontal=True)
        text_box(row.box(), "axum", size=40)
        arrow4 = row.box(width=500)
        arrow_box(arrow4, "Mocked webhooks\n(HTTP)", size=50)
        text_box(row.box(), "bors (lib)", size=40)
        arrow5 = row.box(width=400)
        arrow_box(arrow5, "API requests\n(HTTP)", both_sides=True, size=50)
        text_box(row.box(), "wiremock", size=40)

    @slides.slide()
    def wiremock_example_1(slide: Box):
        slide.update_style("code", T(size=44))
        code(slide.box(), """
Mock::given(method("POST"))
    .and(path_regex("^/app/installations/\\d+/access_tokens$"))
    .respond_with(
        ResponseTemplate::new(200)
            .set_body_json(InstallationToken::default())
    )
    .mount(mock_server)
    .await;
""")

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
