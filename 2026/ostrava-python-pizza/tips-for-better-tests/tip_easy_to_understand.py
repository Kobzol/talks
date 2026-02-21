from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import StateCounter, code_step, ShowRest, code


def make_tests_easy_to_understand(slides: Slides, tips: StateCounter):
    @slides.slide()
    def deque_example(slide: Box):
        slide.update_style("code", T(size=70))
        code_step(slide, """
buf = RingBuffer()

buf.append(5)
buf.append_left(3)
buf.append(4)

print(buf) # 3, 5, 4
""", [
            [ShowRest]
        ], width=1300)

    code_size = 40

    @slides.slide()
    def deque_normal_test(slide: Box):
        slide.update_style("code", T(size=code_size))
        code(slide.box(), """
def test_grow_full_middle_copy_after_t_2():
    buf = RingBuffer(maxlen=4)
    buf.append(5)
    buf.pop_left()
    buf.append(1)
    buf.append(2)
    buf.append(3)
    buf.append(4)

    assert buf.tail_index() == 1
    assert buf.head_index() == 1
    assert buf.phantom_head_index() == 5
    assert buf[0] == 4

    buf.reserve_exact(len(buf))

    assert buf.tail_index() == 1
    assert buf.head_index() == 5
    assert buf[4] == 4
""")

    @slides.slide()
    def its_all_connected(slide: Box):
        slide.box().text("Me trying to understand complex tests:")
        slide.box(width=1100, p_top=40).image("images/meme-its-all-connected.png")

    @slides.slide()
    def make_tests_data_driven(slide: Box):
        tips.tip(slide, "Make tests visual")

    @slides.slide()
    def deque_normal_test(slide: Box):
        """
        DSL
        """
        slide.update_style("code", T(size=44))
        code(slide.box(), '''
def test_grow_full_middle_copy_after_t_2():
    buf = RingBuffer(maxlen=4)
    …

    assert render(buf) == """
4,1,2,3|_,_,_,_
  ^       ^
  t       H
  h
"""

    buf.reserve_exact(vd.capacity())

    assert render(buf) == """
_,1,2,3,4,_,_,_|_,_,_,_,_,_,_,_
  ^       ^
  t       h
"""
    ''')

    # @slides.slide()
    # def imagine_you_are_building_an_ide(slide: Box):
    #     slide.box(p_bottom=40).text("Imagine you are implementing an IDE")
    #     slide.box(show="next+").text('How would you write a test for "Go to definition"?')

    # @slides.slide()
    # def intellij_rust_gotodef_test(slide: Box):
    #     """
    #     DSL, black-box test.
    #     """
    #     project(slide, "PyCharm")
    #     code(slide.box(), '''
# fun testGotoDeclarationOnInitializationWithDunderInit() {
#     myFixture.configureByText(
#         "a.py",
#         """
#         class MyClass:
#             def <target>__init__(self):
#                 pass
#         MyCla<caret>ss()
#         """
#     )
# }
# ''', language="kotlin")

#     @slides.slide()
#     def janestreet_hw_test(slide: Box):
#         """
#         Testing hardware designs.
#         Waveform of a cycle-accurate simulator.
#         """
#         project(slide, "Hardcaml test suite")
#
#         slide.update_style("code", T(size=40))
#         code(slide.box(), """
# let waves = testbench ();;
# val waves : Waveform.t = <abstr>
# Waveform.print ~display_height:12 waves;;
# ┌Signals────────┐┌Waves──────────────────────────────────────────────┐
# │clock          ││┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌──│
# │               ││    └───┘   └───┘   └───┘   └───┘   └───┘   └───┘  │
# │clear          ││                        ┌───────┐                  │
# │               ││────────────────────────┘       └───────────────   │
# │incr           ││        ┌───────────────┐                          │
# │               ││────────┘               └───────────────────────   │
# │               ││────────────────┬───────┬───────┬───────────────   │
# │dout           ││ 00             │01     │02     │00                │
# │               ││────────────────┴───────┴───────┴───────────────   │
# │               ││                                                   │
# └───────────────┘└───────────────────────────────────────────────────┘
# - : unit = ()
# """)
#         source(slide, "https://blog.janestreet.com/using-ascii-waveforms-to-test-hardware-designs")
