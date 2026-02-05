from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import StateCounter, code, code_step, ShowRest, show, skip, last, dimmed_list_item


def test_everything(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_everything(slide: Box):
        tips.tip(slide, "You can test (almost) anything")

    @slides.slide()
    def bors_lgtm(slide: Box):
        slide.box(width=1400).image("images/lgtm.png")

    @slides.slide()
    def bors_db_error(slide: Box):
        slide.box(p_bottom=40).text("In production:")
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
        slide.box(p_top=40, show="next+").text("…is that all we can do?")

    @slides.slide()
    def cargo_sqlparser(slide: Box):
        slide.box(width=1600).image("images/cargo-add-sqlparser.png")

    @slides.slide()
    def migration_test(slide: Box):
        slide.update_style("code", T(size=32))

        width = 1700
        code_step(slide.fbox(), """
#[test]
fn check_non_null_column_without_default() {
    let root = env!("CARGO_MANIFEST_DIR");
    let migrations = PathBuf::from(root).join("migrations");
    for file in std::fs::read_dir(migrations).unwrap() {
        let file = file.unwrap();
        if file.path().extension() == Some(OsStr::new("sql")) {
            let contents =
                std::fs::read_to_string(&file.path()).unwrap();

            let ast = Parser::parse_sql(&PostgreSqlDialect {}, &contents).unwrap();
            let mut visitor = CheckNotNullWithoutDefault::new();
            ast.visit(&mut visitor);

            if let Some(error) = visitor.compute_error() {
                panic!(
                    "Migration {} contains error: {error}",
                    file.path().display()
                );
            }
        }
    }
}
""", [
            show(4) + skip(18) + last(1),
            show(9) + skip(11) + last(3),
            [ShowRest]
        ], width=width)

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
            show(8) + skip(16) + last(3),
            [ShowRest]
    ], width=width)

    @slides.slide()
    def breaking_previous_tip(slide: Box):
        row = slide.box(horizontal=True)
        row.box(p_right=50).text("Didn't I just test implementation details?")
        row.box(width=100).image("images/thinking.svg")
        # Like testing if code is formatted
        slide.box(show="next+", p_top=40).text("Testing a ~emph{property} of an implementation")
        slide.box(show="next+", p_top=40).text("To provide a good error message")

    @slides.slide()
    def end_to_end_tests(slide: Box):
        slide.box(width=1600).image("images/bors-migration-data.png")

    @slides.slide()
    def migration_data_apply(slide: Box):
        slide.update_style("code", T(size=32))
        code_step(slide.fbox(), """
#[sqlx::test(migrations = false)]
async fn apply_migrations_with_test_data(pool: PgPool) -> anyhow::Result<()> {
    let migrations = get_sorted_up_migrations();

    for migration_path in migrations {
        let migration_sql = std::fs::read_to_string(&migration_path)?;

        pool.execute(&*migration_sql).await?;

        let test_data_path = get_test_data_path(&migration_path);
        let test_data = std::fs::read_to_string(&test_data_path)?;

        pool.execute(&*test_data).await.unwrap_or_else(|e| {
            panic!(
                "Failed to apply migration test data {:?}: {}",
                test_data_path, e
            )
        });
    }
    Ok(())
}""", [
        show(5) + skip(13) + last(3),
        [ShowRest]
    ])

    @slides.slide()
    def migration_data_test(slide: Box):
        slide.update_style("code", T(size=40))
        code(slide.box(), """
#[test]
fn check_migrations_have_sample_data() {
    let migrations = get_sorted_up_migrations();
    assert!(!migrations.is_empty());
    for migration_path in migrations {
        let test_data_path = get_test_data_path(&migration_path);

        assert!(
            test_data_path.exists(),
            "Migration {:?} does not have a test data file at {:?}.
            Add a test data file there that fills some test data
            into the database after that migration is applied.",
            migration_path,
            test_data_path
        );
    }
}
""")

#     @slides.slide()
#     def cargo_wizard_dialog(slide: Box):
#         slide.box(p_bottom=40).text("cargo-wizard", T(size=80))
#         slide.box(width=1600).image("images/cargo-wizard.png")
#
#     @slides.slide()
#     def rexpect(slide: Box):
#         slide.update_style("code", T(size=40))
#         code(slide.box(), """use rexpect::spawn;
# use rexpect::error::Error;
#
# fn main() -> Result<(), Error> {
#     let mut p = spawn("cargo wizard", Some(2000))?;
#     p.exp_regex(".*Select the profile.*")?;
#     p.send("\\x1b\\x5b\\x42")?; // Arrow down
#     p.flush()?;
#     p.send_line("")?;        // Enter
#     Ok(())
# }""")
#
#     @slides.slide()
#     def cargo_wizard_test(slide: Box):
#         slide.update_style("code", T(size=40))
#         code(slide.box(), """
# #[test]
# fn dialog_fast_compile_nightly() -> anyhow::Result<()> {
#     let project = init_cargo_project()?;
#
#     DialogBuilder::default()
#         .nightly()
#         .customize_item(
#             "Number of frontend threads",
#             CustomValue::Custom("4".to_string()),
#         )
#         .run(&project)?;
#
#     insta::assert_snapshot!(project.read_config(), @r###"
# [build]
# rustflags = ["-Clink-arg=-fuse-ld=lld", "-Zthreads=4"]
# "###);
#
#     Ok(())
# }
# """)

    @slides.slide()
    def things_that_can_be_tests(slide: Box):
        """
        Just run tests vs have specific CI config.
        """
        slide.box(p_bottom=40).text('Things that can be tests:')
        lst = unordered_list(slide.box())
        items = [
            "Is all code properly formatted?",
            "Do all dependencies use compatible licenses?",
            "Do we have a merge/unsigned commit in git history?",
            "Can the example config file in the repo root be parsed?"
        ]
        for (index, item) in enumerate(items, start=2):
            if item == items[-1]:
                lst.item(show=index).text(item, T(size=54))
            else:
                dimmed_list_item(lst, item, index, size=54)
