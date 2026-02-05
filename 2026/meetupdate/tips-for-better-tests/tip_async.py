from elsie import Arrow, Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import HideRest, ShowRest, StateCounter, aka, code, code_step, error_message, last, project, show, skip


def async_tests(slides: Slides, tips: StateCounter):
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
    def be_in_control(slide: Box):
        tips.tip(slide, "Be in control of your async code")
        width = 1700
        aka(slide, "Use structured concurrency", width=width)
        aka(slide, "Synchronize tests to avoid flaky race conditions", width=width)

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

async fn program(tx: Sender<()>) {
    let mut interval = interval(Duration::from_secs(30));
    loop {
        interval.tick().await;
        tx.send(()).await;
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
            show(1) + [None] + show(5, start=2) + [None] * 8,
            show(7) + [None] * 8,
            show(14) + [None],
            show(7) + show(8, start=15)
            ], width=width, return_codebox=True)

        l1 = box.line_box(12)
        l2 = box.line_box(13)

        x_offset = 50
        x_start = -300
        arrow = Arrow(20)
        slide.fbox(x=0, y=0, show="5+").line([
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
        slide.box().text("How to ensure that something ~emph{happens} reliably?")

        lst = unordered_list(slide.box(p_top=80))
        row = lst.item(show="next+")
        row = row.box(horizontal=True)
        row.box(p_right=40).text('Arbitrarily add sleeps throughout tests until it "works"', "small")
        row.box(width=64).image("images/cross.svg")
        lst.item(show="next+").text("Synchronize through some external state", "small")
        lst2 = lst.ul()
        lst2.item().text("Database, HTTP endpoint, file on disk, …", "small")
        lst.item(show="7+").text("Use coverage marks", "small")

        width = 1700
        code_step(slide.fbox(show="4-6", y=200), """
async fn unapprove() {
    …
    ctx.post_comment("@bors r-").await?;

    // Bot comment acts as a synchronization point
    insta::assert_snapshot!(
        ctx.get_next_comment().await?,
        @"Commit pr-1-sha has been unapproved."
    );

    ctx.get_pr().await.expect_unapproved();
}
""", [
            show(3) + skip(8) + last(1),
            show(9) + skip(2) + last(1),
            [ShowRest]
        ], show_start=4, width=width)
        project(slide, "bors", show="4-6")

    @slides.slide()
    def coverage_marks(slide: Box):
        """
        Inspects implementation.
        https://ferrous-systems.com/blog/coverage-marks
        Dangers of global/thread-local variables - better use context.
        """
        project(slide, "bors")
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

    @slides.slide()
    def collect_all_errors(slide: Box):
        tips.tip(slide, "Collect all errors during tests")


    @slides.slide()
    def missing_error(slide: Box):
        code(slide.box(), """
async fn test_approve() -> anyhow::Result<()> {
    let ctx = start_bors().await;
    ctx.post_comment("@bors r+").await?;
    …

    Ok(())
}
""")
        width = 1750
        error_message(slide.box(width=width, p_top=40, show="next+"), "Error: Connection reset by peer (os error 104)")
        error_message(slide.box(width=width, p_top=20, show="next+", z_level=999), """thread '<unnamed>' (269367) panicked at src/lib.rs:229:25:
Cannot approve PR 1 because of …""")

    @slides.slide()
    def test_wrapper(slide: Box):
        """
        This used to be painful without async closures - had to pass context by value and return it.
        """
        slide.update_style("code", T(size=44))
        code_step(slide.fbox(), """
async fn run_test<F>(test_fn: F) -> anyhow::Result<()>
where
    F: AsyncFnOnce(&mut TestCtx) -> anyhow::Result<()>
{
    let mut ctx = create_ctx().await;

    // or test_fn(&mut ctx).catch_unwind()
    let res1 = test_fn(&mut ctx).await;
    let res2 = ctx.finish().await;
    combine_results(res1, res2)
}

#[tokio::test]
async fn test() {
    run_test(async |ctx| {
        ctx.post_comment("@bors r+").await?;
        Ok(())
    }).await;
}
""", [
            show(4) + skip(6) + show(1, start=10) + [HideRest],
            show(11) + [HideRest],
            [ShowRest]
        ])

    @slides.slide()
    def inspiration(slide: Box):
        slide.box(p_bottom=40).text("Deterministic Simulation Testing")
        lst = unordered_list(slide.box())
        lst = lst.ul()
        lst.item().text("TigerBeetle")
        lst.item().text("antithesis")
