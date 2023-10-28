from elsie import Arrow, SlideDeck, TextStyle as s
from elsie.boxtree.box import Box

from utils import COLOR_BACKEND, COLOR_NOTE, bash, code, list_item, new_slide, slide_header


def cache_conflicts(slides: SlideDeck, backup: bool):
    if backup:
        slide = new_slide(slides)
        content = slide_header(slide, "Code (backup)")
        code(content.box(), """// Addresses of N integers, each `offset` bytes apart
std::vector<int*> data = ...;
for (auto ptr: data)
{
    *ptr += 1;
}
// Offsets: 4, 64, 4000, 4096, 4128""")
        slide = new_slide(slides)
        content = slide_header(slide, "Result (backup)")
        content.box(height=600).image("images/example1-time.png")

    slide = new_slide(slides)
    content = slide_header(slide, "Cache memory")
    content.box(height=600).image("images/haswell-diagram.png")
    content.box(width=230, height=40, x=816, y=530).rect(color=COLOR_BACKEND, stroke_width=3)

    slide = new_slide(slides)
    content = slide_header(slide, "How are (L1) caches implemented")
    list_wrapper = content.box()
    list_item(list_wrapper).text("N-way set associative table")
    list_item(list_wrapper, level=1, show="last+").text("Hardware hash table")
    list_item(list_wrapper, show="next+").text("Key = address (8B)")
    list_item(list_wrapper, show="next+").text("Entry = cache line (64B)")

    slide = new_slide(slides)
    content = slide_header(slide, "N-way set associative cache")
    hash_size = 8
    hash_dimension = 60

    def table(wrapper: Box, size, dimension, buckets=None, bucket_indices=True):
        htable = wrapper.box(horizontal=True)
        items = []
        for i in range(size):
            cell = htable.box(width=dimension, height=dimension, horizontal=True).rect("black",
                                                                                       stroke_width=2)
            items.append(cell)

        if buckets:
            bucket_width = int((size / buckets) * dimension)
            for i in range(buckets):
                pos = i * bucket_width
                htable.box(x=pos, y=0, width=bucket_width, height=dimension).rect("black",
                                                                                  stroke_width=6)
                if bucket_indices:
                    htable.box(x=pos, y=dimension - 5, width=bucket_width).text(str(i))

        return (htable, items)

    content.box().text("Size = {} cache lines".format(hash_size), style="notice")
    (htable, hitems) = table(content.box(p_top=20), hash_size, hash_dimension)
    arrow_wrapper = content.box()
    arrow = Arrow(20)
    arrow_wrapper.box().line([
        hitems[0].p("50%", 0).add(0, -20),
        hitems[-1].p("50%", 0).add(0, -20),
    ], start_arrow=arrow, end_arrow=arrow, stroke_width=5, color=COLOR_NOTE)

    content.box(p_top=20, show="next+").text("Associativity (N) - # of cache lines per bucket")
    content.box(p_top=10, show="next+").text("# of buckets = Size / N")

    row = content.box(horizontal=True, p_top=20)
    lcol = row.box(y=0)
    rcol = row.box(y=0, p_left=20)

    def htable_row(text, block_count):
        padding = 20
        height = 110
        lcol.box(show="next+", p_top=padding, height=height).text(text)
        return table(rcol.box(show="last+", p_top=padding, height=height), hash_size,
                     hash_dimension, block_count)

    htable_row("N = 1 (direct mapped)", hash_size)
    htable_row("N = {} (fully associative)".format(hash_size), 1)
    htable_row("N = 2", hash_size // 2)

    slide = new_slide(slides)
    content = slide_header(slide, "How are addresses hashed?")

    content.box().text("64-bit address:")
    row = content.box(horizontal=True, width=800)
    widths = ["60%", "25%", "15%"]
    address_colors = ["#B22222", "#007944", "#0018AE"]
    labels = ["Tag", "Index", "Offset"]

    for i in range(3):
        wrapper = row.box(width=widths[i]).rect(color=address_colors[i], stroke_width=4)
        wrapper.box(padding=4).text(labels[i])
    labelrow = content.box(horizontal=True, x=220)
    labelrow.box().text("63")
    labelrow.box(p_left=770).text("0")

    list_wrapper = content.box(p_top=20)
    list_item(list_wrapper, show="next+").text("Offset", "bold")
    list_item(list_wrapper, level=1, show="last+").text("Selects byte within a cache line")
    list_item(list_wrapper, level=1, show="last+").text("log2(cache line size) bits")
    list_item(list_wrapper, show="next+").text("Index", "bold")
    list_item(list_wrapper, level=1, show="last+").text("Selects bucket within the cache")
    list_item(list_wrapper, level=1, show="last+").text("log2(bucket count) bits")
    list_item(list_wrapper, show="next+").text("Tag", "bold")
    list_item(list_wrapper, level=1, show="last+").text("Used for matching")

    slide = new_slide(slides)
    content = slide_header(slide, "N-way set associative cache")

    queue = content.box(x="55%", y=40, horizontal=True)
    queue.box(p_right=40).text("Cache lines:")
    colors = ("#F0134D", "#FF6F5E", "#F0134D")
    cacheline_labels = ("A", "B", "C")
    for i in range(3):
        queue.box(width=hash_dimension, height=hash_dimension).rect(color="black",
                                                                    bg_color=colors[i],
                                                                    stroke_width=5).text(
            cacheline_labels[i], style=s(bold=True, color="white"))

    index = content.box(x="55%", y=90, horizontal=True)
    index.box(p_right=75).text("Index bits:")
    index_bits = (0, 1, 0)
    for i in range(3):
        index.box(width=hash_dimension, height=hash_dimension).text(str(index_bits[i]))

    def insert(slot, show, item):
        wrapper = slot.overlay(show=show)
        wrapper.rect(bg_color=colors[item])
        wrapper.text(cacheline_labels[item], style=s(bold=True, color="white"))

    row = content.box(horizontal=True, p_top=20)
    lcol = row.box(y=0)
    rcol = row.box(y=0, p_left=20)

    def htable_row(text, block_count):
        padding = 20
        height = 140
        lcol.box(show="next+", p_top=padding, height=height).text(text)
        return table(rcol.box(show="last+", p_top=padding, height=height), hash_size,
                     hash_dimension, block_count)

    (_, hitems) = htable_row("N = 1", hash_size)
    insert(hitems[0], "next+", 0)
    insert(hitems[1], "next+", 1)
    insert(hitems[0], "next+", 2)

    (_, hitems) = htable_row("N = {}".format(hash_size), 1)
    insert(hitems[0], "next+", 0)
    insert(hitems[1], "next+", 1)
    insert(hitems[2], "next+", 2)

    (_, hitems) = htable_row("N = 2", hash_size // 2)
    insert(hitems[0], "next+", 0)
    insert(hitems[2], "next+", 1)
    insert(hitems[1], "next+", 2)

    slide = new_slide(slides)
    slide.update_style("default", s(size=46))
    slide.update_style("bold", s(size=46))
    content = slide_header(slide, "Intel L1 cache")
    bash(content.box(), """$ getconf -a | grep LEVEL1_DCACHE
LEVEL1_DCACHE_SIZE      32768
LEVEL1_DCACHE_ASSOC     8
LEVEL1_DCACHE_LINESIZE  64""", text_style=s(align="left"))
    list_wrapper = content.box(p_top=20)
    list_item(list_wrapper, show="next+").text("~bold{Cache line size} - 64 B (6 offset bits)")
    list_item(list_wrapper, show="next+").text("~bold{Associativity} (N) - 8")
    list_item(list_wrapper, show="next+").text("~bold{Size} - 32768 B")
    list_item(list_wrapper, show="next+").text("32768 / 64 => 512 cache lines")
    list_item(list_wrapper, show="next+").text("512 / 8 => 64 buckets (6 index bits)")

    slides.set_style("tag", s(color=address_colors[0]))
    tag = slides.get_style("tag")
    slides.set_style("index", tag.compose(s(color=address_colors[1])))
    slides.set_style("offset", tag.compose(s(color=address_colors[2])))

    styles = ["tag", "index", "offset"]
    colors = ["#F0134D", "#FF6F5E", "#1F6650", "#40BFC1"]

    def address(cols, content, next=True, use_style=True, row=0):
        for i, col in enumerate(cols):
            show = "1+"
            if next:
                show = "next+" if i == 0 else "last+"

            style = "default"
            if use_style:
                if i == 0:
                    style = s(color=colors[row])
                else:
                    style = styles[i - 1]
            col.box(show=show).text(content[i], style=style)

    slide = new_slide(slides)
    content = slide_header(slide, "Offset = 4B")

    width = 700
    columns = 4
    row = content.box(horizontal=True)
    cols = [row.box(width=width // columns) for _ in range(columns)]

    address(cols, ("Number", "Tag", "Index", "Offset"), next=False, use_style=False)
    address(cols, ("A", "..100000", "000000", "000000"), next=False)
    address(cols, ("B", "..100000", "000000", "000100"), row=1)
    address(cols, ("C", "..100000", "000000", "001000"), row=2)
    address(cols, ("D", "..100000", "000000", "001100"), row=3)

    hash_dimension = 80
    (htable, hitems) = table(content.box(p_top=20), hash_size, hash_dimension, hash_size // 2)
    for i in range(4):
        hitems[0].box(show="{}+".format(i + 1), width=hash_dimension // 4,
                      height=hash_dimension).rect(bg_color=colors[i])

    list_wrapper = content.box(p_top=40)
    list_item(list_wrapper, show="next+").text("Same bucket, same cache line for each number")
    list_item(list_wrapper, show="next+").text("Most efficient, no space is wasted")

    slide = new_slide(slides)
    content = slide_header(slide, "Offset = 64B")

    row = content.box(horizontal=True)
    cols = [row.box(width=width // columns) for _ in range(columns)]

    address(cols, ("Number", "Tag", "Index", "Offset"), next=False, use_style=False)
    address(cols, ("A", "..100000", "000000", "000000"), next=False)
    address(cols, ("B", "..100000", "000001", "000000"), row=1)
    address(cols, ("C", "..100000", "000010", "000000"), row=2)
    address(cols, ("D", "..100000", "000011", "000000"), row=3)

    (htable, hitems) = table(content.box(p_top=20), hash_size, hash_dimension, hash_size // 2)
    for i in range(4):
        hitems[i * 2].box(show="{}+".format(i + 1), width=hash_dimension // 4,
                          height=hash_dimension, x=0).rect(bg_color=colors[i])

    list_wrapper = content.box(p_top=40)
    list_item(list_wrapper, show="next+").text("Different bucket for each number")
    list_item(list_wrapper, show="next+").text("Wastes 60B in each cache line")
    list_item(list_wrapper, show="next+").text("Equally distributed among buckets")

    slide = new_slide(slides)
    content = slide_header(slide, "Offset = 4096B")

    row = content.box(horizontal=True)
    cols = [row.box(width=width // columns) for _ in range(columns)]

    address(cols, ("Number", "Tag", "Index", "Offset"), next=False, use_style=False)
    address(cols, ("A", "..100000", "000000", "000000"), next=False)
    address(cols, ("B", "..100001", "000000", "000000"), row=1)
    address(cols, ("C", "..100010", "000000", "000000"), row=2)
    address(cols, ("D", "..100011", "000000", "000000"), row=3)

    (htable, hitems) = table(content.box(p_top=20), hash_size, hash_dimension, hash_size // 2)
    for i in range(4):
        hitems[i % 2].box(show="{}+".format(i + 1), width=hash_dimension // 4,
                          height=hash_dimension, x=0).rect(bg_color=colors[i])

    list_wrapper = content.box(p_top=40)
    list_item(list_wrapper, show="next+").text(
        "Same bucket, but different cache lines for each number!")
    list_item(list_wrapper, show="next+").text("Bucket full => evictions necessary")

    slide = new_slide(slides)
    content = slide_header(slide, "How to measure?")
    content.box().text("~tt{l1d.replacement}", style=s(size=48))
    content.box(p_top=20).text("How many times was a cache line loaded into L1?")

    if backup:
        bash(content.box(p_top=40, show="next+"), """$ perf stat -e l1d.replacement ./example1
4B    offset ->     149 558
4096B offset -> 426 218 383""", text_style=s(align="left"))
