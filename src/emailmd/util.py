#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = e61cf0a4-e4df-11ec-b705-4307570280a6
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-06-05
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From PyPI

from lxml.html.clean import Cleaner
from rich.console import Console

# ------------
# Custom Modules

# -------------


# https://stackoverflow.com/questions/3073881/clean-up-html-in-python
def sanitize(dirty_html):
    cleaner = Cleaner(
        scripts=True,
        javascript=True,
        comments=True,
        page_structure=True,
        style=True,
        meta=True,
        embedded=True,
        frames=True,
        forms=True,
        annoying_tags=True,
        inline_style=True,
        links=True,
        processing_instructions=True,
        remove_unknown_tags=True,
        # safe_attrs_only=True,
        # safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
        remove_tags=("span", "font", "div"),
    )

    return cleaner.clean_html(dirty_html)

def construct_non_duplicate_folder(
        root: Path,
        target: str,
        retry_count: int = 25,
        console: Console = None,
        ) -> Path:

    folder = root / Path(target)

    for i in range(retry_count):

        try:

            folder.mkdir(
                parents=True, exist_ok=False
            )  # throw an exception of the folder exists

        except FileExistsError as fe:

            console.print((f"[red]The folder {folder} exists![/red]"))

            folder = root / Path(f"{target} ({i})")

        else:
            break

    else:
        raise FileExistsError(f"The folder {folder} exists!")

    return folder


def construct_non_duplicate_file(
        filename: Path,
        retry_count: int = 100,
        console: Console = None,
        ) -> Path:
    """
    Given a file name, check if it exists and create a new incremental
    name if it does, checking each one in turn. If there are no issues,
    the new path is returned
    """

    candidate = filename.parent / filename.name

    for i in range(retry_count):

        try:
            # https://docs.python.org/3/library/pathlib.html#pathlib.Path.touch
            candidate.touch(exist_ok=False)

        except FileExistsError as fe:
            console.print((f"[red]{candidate.name} exists![/red]"))

            # construct a new file name
            candidate = filename.parent / Path(
                f"{filename.stem} ({i}){filename.suffix}"
            )

        else:
            break

    else:
        raise FileExistsError(
            f"[red]Exceeded Retry Count[/red] - The file {candidate} exists and new names exceeded the retry count! "
        )

    return candidate
