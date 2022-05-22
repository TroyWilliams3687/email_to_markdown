#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid:   a50c7b48-d9db-11ec-bae6-b5f6a1846473
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2022-05-22
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From pip

import click

from rich.console import Console
console = Console()

# ------------
# Custom Modules

# ------------


@click.command()
@click.pass_context
@click.argument(
    "files",
    nargs=-1,  # accept an unlimited number of arguments. This makes it an iterable
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def extract(*args, **kwargs):
    """
    Extract the email messages (EML, MSG) to Markdown.

    # Usage

    $ emailmd extract ~/email/*.msg ~/email/*.eml

    """

    ctx = args[0]

    if len(kwargs["files"]) == 0:
        console.print("[red]No Files to process![/red]")
        ctx.abort()

    for f in kwargs["files"]:
        console.print(f"Extracting {f}...")


