from elsie import Slides, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from utils import StateCounter, code


def test_in_production(slides: Slides, tips: StateCounter):
    @slides.slide()
    def test_in_production(slide: Box):
        tips.tip(slide, "Test (also) in production")

    @slides.slide()
    def mocking_prod_is_hard(slide: Box):
        """
        You will have to test in production *someday*, better embrace it.
        """
        slide.box(p_bottom=40).text("Problems with testing only in staging:")
        lst = unordered_list(slide.box())
        items = [
            "It's difficult to emulate production",
            "It's difficult to get things right on the first try"
        ]
        for (index, item) in enumerate(items, start=2):
            lst.item(show=f"{index}+").text(item, T(size=60))

    @slides.slide()
    def do_no_test_on_real_users(slide: Box):
        slide.box().text("Testing in production != testing on real users")

    @slides.slide()
    def feature_flags(slide: Box):
        """
        A/B deployments
        """
        slide.box(p_bottom=40).text("Feature flags")
        code(slide.box(), """
if is_feature_enabled("foo") {
    do_a();
} else {
    do_b();
}
""")
