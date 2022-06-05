#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 41481cee-e4de-11ec-b705-4307570280a6
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-06-05
# -----------

"""
"""

# ------------
# System Modules - Included with Python

import mimetypes

from pathlib import Path
from typing import Optional

# ------------
# 3rd Party - From PyPI

from rich.console import Console

from pathvalidate import sanitize_filename

# ------------
# Custom Modules

from .standardemail import (
    StandardEmail,
)

from .util import (
    sanitize,
    construct_non_duplicate_file,
)

# -------------


def write_standard_email(
        email_message: StandardEmail,
        output: Path,
        relative_path: Path = None,
        console: Console = None,
        ) -> None:
    """
    Given the StandardEmail, write it to the output folder, creating a
    new folder for the email and attachments.

    # args

    email_message - the email message to write to a file

    output - the root path to write the data too

    # kwargs

    relative_path - the path to add to the output to write the email
    too. For example if the email is in `eml/travel/email.eml` it will
    write the corresponding files to the relative folder under `output/travel/...`

    """

    message_name = sanitize_filename(email_message.header.subject)

    # Construct the output folder - from the subject
    message_folder = output / relative_path / message_name.lower() if relative_path else output / message_name.lower()
    message_folder.mkdir(parents=True, exist_ok=True)

    # construct the name of the email message

    message_file = construct_non_duplicate_file(
        message_folder / Path(f"{message_name.lower()}.md"),
        console=console,
    )

    message_file.write_text(email_message.to_markdown(attachment_folder="attachments"))

    console.print(f"Saved Email: [cyan]{message_file.name}[/cyan]")

    for attachment in email_message.attachments:

        if attachment.data:
            attachment_folder = message_folder / Path("attachments")
            attachment_folder.mkdir(parents=True, exist_ok=True)

            attachment_file = attachment_folder / attachment.filename

            attachment_file.write_bytes(attachment.data)

            console.print(
                f"[yellow]Saved Attachment[/yellow]: [cyan]{attachment_file.name}[/cyan]"
            )
