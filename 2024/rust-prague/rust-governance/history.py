import datetime
from typing import Callable

from elsie import SlideDeck, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from config import sh, sw
from utils import COLOR_ORANGE, next_two_slides, quotation


def timeline(slides: SlideDeck):
    years = []

    def render_year_tick(timeline: Box, year: int):
        this_year = 2024
        first_year = 2006

        wrapper_width = sw(100)
        point_width = sw(25)
        point_height = sh(80)

        x_percent = (year - first_year) / (this_year - first_year)
        timeline_entry = timeline.box(
            width=wrapper_width,
            x=timeline.x(f"{round(x_percent * 100)}%").add(-wrapper_width / 2),
            y=timeline.y("50%").add(-point_height / 2)
        )
        entry_tick = timeline_entry.box(width=point_width, height=point_height)
        entry_tick.rect(bg_color="black")

        timeline_entry.box(p_top=sh(20)).text(str(year), style=T(size=44), rotation=-45)

        return entry_tick

    def render_year(year: int, render_fn: Callable[[Box], None]):
        slide = slides.new_slide(debug_boxes=False)

        timeline_box = slide.fbox(height=sh(140), p_top=sh(40))
        timeline = timeline_box.box(width="90%", height=sh(30))
        timeline.rect(bg_color="black")

        # Year ticks
        for y in years:
            render_year_tick(timeline, y)
        entry_tick = render_year_tick(timeline, year)
        entry_tick.overlay().rect(bg_color=COLOR_ORANGE)

        # Margin
        slide.sbox(height=sh(60))
        content_box = slide.box(width="100%", height="fill")

        render_fn(content_box)
        years.append(year)

    def year_2006(box: Box):
        box.box(p_bottom=sh(60)).text("Started as a personal project\nby Graydon Hoare (@Mozilla)")
        quotation(box.box(show="next+"),
                  "I think I named it after fungi…\n\t\tthat is \"over-engineered for survival\".",
                  "Graydon Hoare")

    def year_2010(box: Box):
        intro_slide = box.box(width=sw(800), show="1-2").image("images/rust-intro-slide.png")
        box.box(show="2", x=intro_slide.x("100%"), y=box.y("0%"), width=sw(400)).image(
            "images/rust-logo.png")
        team = box.overlay(show="next+")
        team = team.box().text("Patrick Walton, Niko Matsakis join Graydon")
        team.box(show="next", p_top=sh(160)).text("Communication on mailing lists, later IRC")

    def year_2012(box: Box):
        box.box().text("Graydon steps down as BDFL")
        box.box(p_top=sh(40), show="next+").text("Core team is created")

    def year_2014(box: Box):
        """
        https://rust-lang.github.io/rfcs/0002-rfc-process.html
        """
        box.box(p_right=sw(40)).text("RFC process created (inspired by PEP)")
        box.overlay(show="next").box(width=sw(1400)).image("images/rfc-1.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/rfc-2.png")

    def year_2015(box: Box):
        """
        More than a thousand RFCs in a year!
        Core team decided up until now.
        Too many RFCs, making RFCs for too small changes
        (https://rust-lang.github.io/rfcs/1058-slice-tail-redesign.html)
        Need for specific areas of focus.
        Need for moderation (separate from the core team).
        Do not require a RFC for every tiny change.
        """
        box.box(show="1").text("Rust 1.0 released")
        box.box(show="next").text("RFC #1068: introduction of (sub)teams")
        box.overlay(show="next").box(width=sw(1400)).image("images/rfc-1068.png")
        list_box = box.overlay(show="next").box()
        list_box.box().text("Initial subteams:")
        lst = unordered_list(list_box)
        lst.item().text("Language")
        lst.item().text("Library")
        lst.item().text("Compiler")
        lst.item().text("Tooling and infrastructure")
        lst.item().text("Moderation")

    def year_2020(box: Box):
        box.box(width=sw(1400), show="1").image("images/mozilla-layoffs.png")
        box.overlay(show="next").text("Core team plans to create a Rust Foundation")

    def year_2021(box: Box):
        box.box(width=sw(1400), show="1").image("images/rust-foundation-creation.png")
        foundation = box.overlay(show="next-7")
        foundation.box(p_bottom=sh(20)).text("Rust Foundation goals:", style=T(bold=True))
        lst = unordered_list(foundation.box())
        lst.item(show="3+").text("Create an official Rust entity")
        lst.item(show="4+").text("Legal, bank account, domain ownership, ...")
        lst.item(show="5+").text("Support maintainers")
        lst.item(show="6+").text("Facilitate sponsorship")
        lst.ul().item(show="7+").text("Mozilla, Google, AWS, Microsoft, Huawei")
        box.overlay(show="next+").box(width=sw(1400)).image("images/moderation-team-resignation.png")

    def year_2022(box: Box):
        box.box(width=sw(1400)).image("images/2022-governance-update.png")
        box.box(show="next+").text("Created a private \"leadership chat\" to solve the issues")

    def year_2023(box: Box):
        box.box(width=sw(1400), show="1").image("images/trademark-policy.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/crab-lang.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/rust-conf-fiasco.png")
        box.overlay(show="next").box(width=sw(1400)).image("images/rust-leadership-council.png")

    render_year(2006, year_2006)
    render_year(2010, year_2010)
    render_year(2012, year_2012)
    render_year(2014, year_2014)
    render_year(2015, year_2015)
    render_year(2020, year_2020)
    render_year(2021, year_2021)
    render_year(2022, year_2022)
    render_year(2023, year_2023)


def history(slides: SlideDeck):
    timeline(slides)
