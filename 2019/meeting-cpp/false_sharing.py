from elsie import SlideDeck, TextStyle as s

from utils import new_slide, slide_header, code, COLOR_BACKEND, bash


def false_sharing(slides: SlideDeck, backup: bool):
    if backup:
        slide = new_slide(slides)
        content = slide_header(slide, "Code (backup)")
        code(content.box(), """// tid - [0, NO_OF_THREADS)
void thread_fn(int tid, double* data)
{
    size_t repetitions = 1024 * 1024 * 1024UL;
    for (size_t i = 0; i < repetitions; i++)
    {
        data[tid] *= i;
    }
}""")
        slide = new_slide(slides)
        content = slide_header(slide, "Result (backup)")
        content.box(height=600).image("images/example3-time.png")

    slide = new_slide(slides)
    content = slide_header(slide, "Cache system")
    content.box(height=600).image("images/haswell-diagram.png")
    content.box(width=230, height=40, x=816, y=530).rect(color=COLOR_BACKEND, stroke_width=3)
    content.box(width=226, height=40, x=240, y=570).rect(color=COLOR_BACKEND, stroke_width=3)

    slide = new_slide(slides)
    content = slide_header(slide, "Cache coherency")
    content.box(height=600).image("images/false-sharing.svg")

    slide = new_slide(slides)
    content = slide_header(slide, "False sharing")
    content.box(width="90%").image("images/false-sharing-array.svg")

    slide = new_slide(slides)
    content = slide_header(slide, "How to measure?")
    content.box().text("~tt{l2_rqsts.all_rfo}", s(size=48))
    content.box(p_top=20).text("How many times some core invalidated data in other cores?")

    if backup:
        bash(content.box(p_top=40, show="next+"), """$ perf stat -e l2_rqsts.all_rfo ./example3
1 thread   ->        59 711
2 threads  -> 1 112 258 710""", text_style=s(align="left"))
