from elsie import SlideDeck, TextStyle as s

from branch_prediction import branch_prediction
from cache_conflicts import cache_conflicts
from denormals import denormals
from false_sharing import false_sharing
from utils import COLOR_NOTE, code, finish_slides, list_item, new_slide, new_slides, slide_header

COLOR1 = "black"
COLOR2 = "#f74f00"
FONT = "Raleway"


def intro(slides: SlideDeck):
    slide = new_slide(slides)
    slide.box().text("""CPU design effects
that can degrade performance of your programs""", s(bold=True, size=40))

    slide.box(p_top=40).text("""Jakub Beránek
jakub.beranek@vsb.cz""", s(bold=False, size=30))

    slide = new_slide(slides)
    content = slide_header(slide, "~tt{whoami}")
    list_wrapper = content.box()
    list_item(list_wrapper).text("PhD student @ VSB-TUO, Ostrava, Czech Republic")
    list_item(list_wrapper).text("Research assistant @ IT4Innovations (HPC center)")
    list_item(list_wrapper).text("HPC, distributed systems, program optimization")

    slide = new_slide(slides)
    content = slide_header(slide, "How do we get maximum performance?")
    list_wrapper = content.box()
    list_item(list_wrapper).text("Select the right algorithm")
    list_item(list_wrapper, show="next+").text("Use a low-overhead language")
    list_item(list_wrapper, show="next+").text("Compile properly")
    list_item(list_wrapper, show="next+").text("~bold{Tune to the underlying hardware}")


def hw_complexity(slides: SlideDeck):
    slide = new_slide(slides)
    content = slide_header(slide, "Why should we care?")
    list_wrapper = content.box()
    list_item(list_wrapper).text("We write code for the C++ abstract machine")
    list_item(list_wrapper, show="next+").text(
        "Intel CPUs fulfill the contract of this abstract machine")
    list_item(list_wrapper, level=1, show="next+").text(
        "But inside they can do whatever they want")
    list_item(list_wrapper, show="next+").text(
        "Understanding CPU trade-offs can get us more performance")

    slide = new_slide(slides)
    slide.update_style("code", s(size=50))
    content = slide_header(slide, "C++ abstract machine example")
    code(content.box(), """void foo(int* arr, int count)
{
    for (int i = 0; i < count; i++)
    {
        arr[i]++;
    }
}""")
    content.box(p_top=20).text("How fast are the individual array increments?", s(size=40))

    slide = new_slide(slides)
    content = slide_header(slide, "Hardware effects")
    list_wrapper = content.box()
    list_item(list_wrapper).text(
        "Performance effects caused by a specific CPU/memory implementation")
    list_item(list_wrapper, show="next+").text(
        "Demonstrate some CPU/memory trade-off or assumption")
    list_item(list_wrapper, show="next+").text("Impossible to predict from (C++) code alone")

    slide = new_slide(slides)
    content = slide_header(slide, "Hardware is getting more and more complex")
    content.box(height=600).image("images/moores-law.png")
    content.box().text("Source: karlrupp.net", s(size=30))

    slide = new_slide(slides)
    content = slide_header(slide, "Microarchitecture (Haswell)")
    content.box(height=600).image("images/haswell-diagram.svg")
    # Heuristics, assumptions, fast paths/slow paths
    content.box().text("Source: Intel Architectures Optimization Reference Manual", s(size=30))

    slide = new_slide(slides)
    content = slide_header(slide, "How bad is it?")
    list_wrapper = content.box()
    cpp = list_item(list_wrapper).box(horizontal=True)
    cpp.box().text("C++ 17 final draft: ")
    cpp.box(show="next+").text(" 1622 pages")
    intel = list_item(list_wrapper, show="next+").box(horizontal=True)
    intel.box().text("Intel x86 manual: ")
    intel.box(show="next+").text(" ~bold{5764} pages!")
    content.box(y=580).text("""http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf
https://software.intel.com/sites/default/files/managed/39/c5/325462-sdm-vol-1-2abcd-3abcd.pdf
https://software.intel.com/sites/default/files/managed/9e/bc/64-ia-32-architectures-optimization-manual.pdf""",
                            s(
                                size=14,
                                align="left"
                            ))

    slide = new_slide(slides)
    content = slide_header(slide, "Plan of attack")
    list_wrapper = content.box()
    list_item(list_wrapper).text("Show example C++ programs")
    list_item(list_wrapper, level=1, show="next+").text("short, (hopefully) comprehensible")
    list_item(list_wrapper, level=1, show="next+").text("compiled with ~tt{-O3}")
    list_item(list_wrapper, show="next+").text("Demonstrate weird performance behaviour")
    list_item(list_wrapper, show="next+").text("Let you guess what might cause it")
    list_item(list_wrapper, show="next+").text("Explain (a possible) cause")
    list_item(list_wrapper, show="next+").text("Show how to measure and fix it")
    list_item(list_wrapper, show="next+", p_top=20).text(
        "Disclaimer #1: Everything will be Intel x86 specific")
    list_item(list_wrapper, show="next+").text(
        "Disclaimer #2: I'm not an expert on this and I may be wrong :-)")

    slide = new_slide(slides)
    slide.box().text("""Let's see some examples...""", s(bold=True, size=40))


def outro(slides: SlideDeck):
    slide = new_slide(slides)
    content = slide_header(slide, "There are many other effects")
    list_wrapper = content.box()
    list_item(list_wrapper).text("NUMA")
    list_item(list_wrapper).text("4k aliasing")
    list_item(list_wrapper).text("Misaligned accesses, cache line boundaries")
    list_item(list_wrapper).text("Instruction data dependencies")
    list_item(list_wrapper).text("Software prefetching")
    list_item(list_wrapper).text("Non-temporal stores & cache pollution")
    list_item(list_wrapper).text("Bandwidth saturation")
    list_item(list_wrapper).text("DRAM refresh intervals")
    list_item(list_wrapper).text("AVX/SSE transition penalty")
    list_item(list_wrapper).text("...")

    slide = new_slide(slides)
    slide.box().text("Thank you!", s(bold=True, size=60))
    slide.box(p_top=60).text("""For more examples visit:
~tt{github.com/kobzol/hardware-effects}""", s(size=44))
    slide.box(p_top=80).text("Jakub Beránek")

    slide.box(p_top=100).text("Slides built with ~tt{github.com/spirali/elsie}", s(size=30))


def make_presentation(path: str, backup: bool):
    slides = new_slides(1280, 720)

    slides.update_style("default", s(font=FONT, size=36, color=COLOR1))  # Default font
    slides.update_style("emph", s(color=COLOR2))  # Emphasis
    slides.update_style("code", s(size=32))
    slides.set_style("bold", s(bold=True))
    slides.set_style("notice", s(color=COLOR_NOTE, bold=True))

    intro(slides)
    hw_complexity(slides)
    branch_prediction(slides, backup)
    cache_conflicts(slides, backup)
    denormals(slides, backup)
    outro(slides)
    finish_slides(slides)
    false_sharing(slides, backup)

    slides.render(path)


make_presentation("slides.pdf", True)
