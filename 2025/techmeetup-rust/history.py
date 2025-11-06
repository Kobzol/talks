import datetime
import io
from typing import Callable

import pandas as pd
from elsie import SlideDeck, TextStyle as T
from elsie.boxtree.box import Box
from elsie.ext import unordered_list

from config import sh, sw
from utils import COLOR_ORANGE, next_two_slides, quotation


def timeline(slides: SlideDeck):
    years = []

    def render_year_tick(timeline: Box, year: int):
        this_year = datetime.datetime.utcnow().year
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

    def year_2010(box: Box):
        box.box(width=800).image("images/rust-intro-slide.png")

    def year_2012(box: Box):
        box.box().text("First \"core team\" formed (~5 people from Mozilla)", escape_char="#")

    def year_2013(box: Box):
        box.box().text("Graydon steps down as BDFL")

    def year_2014(box: Box):
        box.box().text("Rust RFC process created (inspired by PEP)")
        box.box(x=1430, y=500).image("images/python-logo.svg")
        box.overlay(show="next").box(width=1400).image("images/rfc-1.png")
        box.overlay(show="next").box(width=1400).image("images/rfc-2.png")

    def year_2015(box: Box):
        box.box(width=1400).image("images/rfc-1068.png")
        wrapper = box.box(x=1200, y=0, z_level=1, show="next+")
        teams = ["Language", "Library", "Compiler", "Infrastructure", "Moderation"]
        lst = unordered_list(wrapper.box())
        for team in teams:
            lst.item().text(team)

    def year_2020(box: Box):
        box.box(p_bottom=50).text("Mozila lays off most employees paid to work on Rust")
        box.box(width=1200).image("images/mozila-layoffs.png")

    def year_2021(box: Box):
        row = box.box(horizontal=True, show="1")
        row.box().text("Rust Foundation was established")
        row.box(p_left=50).image("images/rust-foundation-logo.png")
        box.box(width=1400, show="1").image("images/aws-rust-foundation.png")

        box.box(width=1400, x="[50%]", y="[50%]", show="next+").image("images/mod-team-resignation.png")

    def year_2023(box: Box):
        images = [
            "trademark-policy",
            "crab-lang",
            # "rust-conf-fiasco",
            "rfc-3392"
        ]
        for (step, image) in enumerate(images):
            box.box(width=1400, x="[50%]", y="[50%]", show=str(step + 1)).image(f"images/{image}.png")

    render_year(2006, year_2006)
    render_year(2010, year_2010)
    render_year(2012, year_2012)
    render_year(2013, year_2013)
    render_year(2014, year_2014)
    render_year(2015, year_2015)
    render_year(2020, year_2020)
    render_year(2021, year_2021)
    render_year(2023, year_2023)


def history(slides: SlideDeck):
    timeline(slides)
