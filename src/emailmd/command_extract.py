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


from .standardemailtools import(
    write_standard_email,
)

from .emltools import extract_eml
from .msgtools import extract_msg

# ------------


@click.command()
@click.pass_context
@click.argument(
    "files",
    nargs=1,
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.argument(
    "output",
    nargs=1,
    type=click.Path(
        exists=False,
        dir_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "--recursive", "-r",
    is_flag=True,
    help="Search for email messages recursively in the input folder.",
)
def extract(*args, **kwargs):
    """
    Extract the email messages (EML, MSG) to Markdown files placed in
    the OUTPUT folder.

    # Usage

    $ emailmd extract ~/tmp/"email to markdown"/eml/ ~/email/output

    $ emailmd extract -r ~/tmp/'email to markdown'/eml/ ~/tmp/'email to markdown'/output


    """

    ctx = args[0]

    kwargs["output"].mkdir(parents=True, exist_ok=True)

    search = kwargs["files"].rglob if kwargs['recursive'] else kwargs["files"].glob

    for f in search("*.*"):
        console.print(f"Extracting: {f}...")

        if f.suffix.lower() == ".msg":
            msg = extract_msg(f, console=console)

        elif f.suffix.lower() == ".eml":

            msg = extract_eml(f.read_text(), console=console)

        else:
            console.print(f"[red]Unknown format -> {f.name}[/red]")
            continue

        write_standard_email(
            msg,
            kwargs["output"],
            relative_path=f.parent.relative_to(kwargs["files"]),
            console=console,
        )


        console.print("")

    console.print(f"[green]Complete[/green]")
