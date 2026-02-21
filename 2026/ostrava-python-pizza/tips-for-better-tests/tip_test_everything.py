from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import StateCounter, dimmed_list_item


def test_everything(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_everything(slide: Box):
        tips.tip(slide, "You can test (almost) anything")

    @slides.slide()
    def things_that_can_be_tests(slide: Box):
        slide.box(p_bottom=40).text('Things that can be tests:')
        lst = unordered_list(slide.box())
        items = [
            "Can my migrations be applied to a non-empty (production?) database?",
            "Is all code properly formatted?",
            "Do all dependencies use compatible licenses?",
            "Do we have a merge/unsigned commit in git history?",
            "Can the example config file in the repo root be parsed?"
        ]
        for (index, item) in enumerate(items, start=1):
            if item == items[-1]:
                lst.item(show=index).text(item, T(size=54))
            else:
                dimmed_list_item(lst, item, index, size=54)
