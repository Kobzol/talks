from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from shared import BOOTSTRAP_TEST_CODE_ASSERT
from utils import StateCounter, code_step, HideRest, ShowRest, show, code, project, source


def make_tests_easy_to_understand(slides: Slides, tips: StateCounter):
    @slides.slide()
    def deque_example(slide: Box):
        code_step(slide, """
let mut buf = VecDeque::new();

buf.push_back(5);
buf.push_front(3);
buf.push_back(4);

let c: Vec<&i32> = buf.iter().collect();
eprintln!("{c:?}"); // [3, 5, 4]
""", [
            [0] + [HideRest],
            show(5) + [HideRest],
            [ShowRest]
        ], width=1300)


    @slides.slide()
    def deque_issues(slide: Box):
        slide.box(p_bottom=20).text("In 2022:")

        width = 1400
        code_step(slide.fbox(height=300), """
let v = Vec::new();      // no allocation
let m = HashMap::new();  // no allocation
let d = VecDeque::new(); // allocated :(
""", [
            [0] + [HideRest],
            [0, 1] + [HideRest],
            [ShowRest],
        ], width=width)
        slide.box(x="[50%]", y="[50%]", show="next", width=1600, z_level=999).image("images/vecdeque-1.png")
        # slide.box(x="[50%]", y="[50%]", show="next", width=1600, z_level=999).image("images/vecdeque-2.png")
        # slide.box(x="[50%]", y="[50%]", show="next+", width=1600, z_level=999).image("images/vecdeque-3.png")

        # https://github.com/rust-lang/rust/compare/main...Kobzol:rust:vec-deque-tests

    code_size = 36

    @slides.slide()
    def deque_normal_test(slide: Box):
        slide.update_style("code", T(size=code_size))
        code(slide.box(y=50), """
#[test]
fn test_grow_full_middle_copy_after_t_2() {
    let mut vd = VecDeque::<u64>::with_capacity(4);
    vd.push_back(5);
    vd.pop_front();
    vd.push_back(1);
    vd.push_back(2);
    vd.push_back(3);
    vd.push_back(4);

    assert_eq!(vd.tail_index(), 1);
    assert_eq!(vd.head_index(), 1);
    assert_eq!(vd.phantom_head_index(), 5);
    assert_eq!(vd.get(0), Some(4));

    vd.reserve_exact(vd.capacity()); // shrink capacity

    assert_eq!(vd.tail_index(), 1);
    assert_eq!(vd.head_index(), 5);
    assert_eq!(vd.get(4), Some(4));
}
""")

    @slides.slide()
    def its_all_connected(slide: Box):
        slide.box().text("Me trying to understand complex tests:")
        slide.box(width=1100, p_top=40).image("images/meme-its-all-connected.png")

    @slides.slide()
    def make_tests_data_driven(slide: Box):
        tips.tip(slide, "Make tests visual")
        slide.box(show="next+").text("to make them easier to understand")

    @slides.slide()
    def deque_normal_test(slide: Box):
        """
        DSL
        """
        slide.update_style("code", T(size=44))
        code(slide.box(), """
#[test]
fn test_grow_full_middle_copy_after_t_2() {
    let mut vd = VecDeque::<u64>::with_capacity(4);
    …

    assert_eq!(render(&vd), r#"
4,1,2,3|_,_,_,_
  t       H
  h
"#);

    vd.reserve_exact(vd.capacity()); // shrink capacity

    assert_eq!(render(&vd), r#"
_,1,2,3,4,_,_,_|_,_,_,_,_,_,_,_
  t       h
"#);
}
    """)

    @slides.slide()
    def be_creative(slide: Box):
        slide.box().text("Be creative!")

    @slides.slide()
    def imagine_you_are_building_an_ide(slide: Box):
        slide.box(p_bottom=40).text("Imagine you're building an IDE for Rust")
        slide.box(show="next+").text('How would you write a test for "Go to definition"?')

    @slides.slide()
    def intellij_rust_gotodef_test(slide: Box):
        """
        DSL, black-box test.
        """
        project(slide, "IntelliJ Rust/RustRover")
        code(slide.box(), '''
fun `test type alias`() = checkByCode("""
    type Foo = usize;
         //X

    trait T { type O; }

    struct S;

    impl T for S { type O = Foo; }
                            //^
""")
''', language="kotlin")

    @slides.slide()
    def rust_analyzer_gotodef_test(slide: Box):
        slide.update_style("code", T(size=40))
        project(slide, "Rust Analyzer")
        code(slide.box(x=450), """
#[test]
fn goto_definition_resolves_correct_name() {
    check(r#"
//- /lib.rs
use a::Foo;
mod a;
mod b;

enum E { X(Foo$0) }

//- /a.rs
struct Foo;
     //^^^

//- /b.rs
struct Foo;
"#,
    );
}
""", width=1200)

    # IntelliJ
    # https://github.com/intellij-rust/intellij-rust/blob/master/src/test/kotlin/org/rust/lang/core/completion/RsAsNameCompletionTest.kt
    # https://github.com/intellij-rust/intellij-rust/blob/master/src/test/kotlin/org/rust/lang/core/resolve/RsResolveTest.kt
    # https://github.com/intellij-rust/intellij-rust/blob/master/src/test/kotlin/org/rust/lang/core/type/RsPatternMatchingTest.kt

    # Rust Analyzer
    # https://github.com/rust-lang/rust-analyzer/blob/92b9e5ef3c03d51713ff5fa32cd58bdf97701b5e/crates/ide/src/goto_definition.rs#L168-L185

#     @slides.slide()
#     def debuginfo_tests(slide: Box):
#         slide.update_style("code", T(size=40))
#         project(slide, "Rust compiler debuginfo test suite")
#         code(slide.box(), """
# let mut hash_map = HashMap::<u64, u64>::default();
# for i in 1..5 {
#     hash_map.insert(i, i * 10);
# }
# // gdb-command: print hash_map
# // gdb-check:$12 = HashMap(size=4) = {[1]=10, [2]=20, [3]=30, [4]=40}
# """)

    @slides.slide()
    def bootstrap(slide: Box):
        slide.update_style("code", T(size=40))
        project(slide, "bootstrap (Rust compiler build system)")
        code(slide.box(y=130), BOOTSTRAP_TEST_CODE_ASSERT)

    @slides.slide()
    def janestreet_hw_test(slide: Box):
        """
        Testing hardware designs.
        Waveform of a cycle-accurate simulator.
        """
        project(slide, "Hardcaml test suite")

        slide.update_style("code", T(size=40))
        code(slide.box(), """
let waves = testbench ();;
val waves : Waveform.t = <abstr>
Waveform.print ~display_height:12 waves;;
┌Signals────────┐┌Waves──────────────────────────────────────────────┐
│clock          ││┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌──│
│               ││    └───┘   └───┘   └───┘   └───┘   └───┘   └───┘  │
│clear          ││                        ┌───────┐                  │
│               ││────────────────────────┘       └───────────────   │
│incr           ││        ┌───────────────┐                          │
│               ││────────┘               └───────────────────────   │
│               ││────────────────┬───────┬───────┬───────────────   │
│dout           ││ 00             │01     │02     │00                │
│               ││────────────────┴───────┴───────┴───────────────   │
│               ││                                                   │
└───────────────┘└───────────────────────────────────────────────────┘
- : unit = ()
""")
        source(slide, "https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs")
