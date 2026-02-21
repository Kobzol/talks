from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box

from utils import StateCounter, aka, bash, code, project


def data_driven_tests(slides: Slides, tips: StateCounter):
    @slides.slide()
    def data_driven_tests(slide: Box):
        """
        Tests no longer compile (refactoring) vs tests fail.
        """
        tips.tip(slide, "Make tests data-driven")
        width = 1000
        aka(slide, "Make tests blessable", width=width, show="last+")
        aka(slide, "Use snapshot/expect tests", width=width, show="last+")

    width = 1600
    y = 200

    @slides.slide()
    def deque_normal_test(slide: Box):
        slide.update_style("code", T(size=44))
        code(slide.box(y=y), '''
def test_grow_full_middle_copy_after_t_2():
    buf = RingBuffer(maxlen=4)

    …

    assert render(buf) == """
4,1,2,3|_,_,_,_
  ^       ^
  t       H
  h
"""
    ''', width=width)

    @slides.slide()
    def deque_snapshot_test(slide: Box):
        project(slide, "pytest-insta")
        slide.update_style("code", T(size=44))
        code(slide.box(y=y), '''
def test_grow_full_middle_copy_after_t_2(snapshot):
    buf = RingBuffer(maxlen=4)

    …

    assert snapshot() == render(buf)
    ''', width=width)

    @slides.slide()
    def deque_snapshot(slide: Box):
        project(slide, "pytest-insta")
        slide.update_style("code", T(size=60))
        bash(slide, "$ cat snapshots/test__grow_full_middle_copy_after_t_2__0.txt", width=1650,
             height=80,
             text_style=T(size=44))
        code(slide.box(p_top=100), """
4,1,2,3|_,_,_,_
^       ^
t       H
""")

    @slides.slide()
    def pytest_insta(slide: Box):
        """
        Code review to check validity.
        """
        project(slide, "pytest-insta")

        box = slide.box(y=160)
        bash(box, "$ python3 -m pytest --insta review", width=1600, height=100)
        box.box(width=1600, p_top=20).image("images/pytest-insta.png")
