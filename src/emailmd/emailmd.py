#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid:   2101e248-d9db-11ec-bae6-b5f6a1846473
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2022-05-22
# -----------

"""
"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From pip

import click


from rich.console import Console
console = Console()

from rich.traceback import install
install(show_locals=False, suppress=[click])

# ------------
# Custom Modules

from .command_extract import extract

# -------------

@click.group()
@click.version_option()
@click.pass_context
def main(*args, **kwargs):
    """
    Extract emails to markdown format and save the attachments.

    """

    # ctx = args[0]
    # ctx.ensure_object(dict)

    pass


# Add the child menu options
main.add_command(extract)

