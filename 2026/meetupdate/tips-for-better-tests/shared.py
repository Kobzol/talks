BOOTSTRAP_TEST_CODE = """
#[test]
fn cross_compile_test_library_stage_2() {
    let ctx = TestCtx::new();
    insta::assert_snapshot!(
        ctx.config("test")
            .path("library")
            .stage(2)
            .targets(&["target1"])
            .render_steps(), @r#"
    [build] llvm <host>
    [build] rustc 0 <host> -> rustc 1 <host>
    [build] rustc 1 <host> -> std 1 <host>
    [build] rustc 1 <host> -> rustc 2 <host>
    [build] rustc 2 <host> -> std 2 <host>
    [build] rustc 1 <host> -> std 1 <target1>
    [build] rustc 2 <host> -> std 2 <target1>
    [test]  std 2 <target1>
"#);
}
"""

BOOTSTRAP_TEST_CODE_ASSERT = BOOTSTRAP_TEST_CODE.replace("insta::assert_snapshot!", "assert_eq!").replace("@", "")
