#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 859f749e-e4e0-11ec-b705-4307570280a6
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

from msglite import Message
from rich.console import Console


# ------------
# Custom Modules

from .standardemail import (
    EmailHeader,
    EmailAttachment,
    StandardEmail,
)

# -------------


def extract_msg_attachments(
        msg: Message,
        console: Console = None,
        ) -> Optional[list[EmailAttachment]]:
    """
    """

    attachments = []

    for i, part in enumerate(msg.attachments):

        if isinstance(part.data, Message):
            attachments.extend(extract_msg_attachments(part.data, console=console))
            continue

        fn = part.title
        if not fn:
            ext = mimetypes.guess_extension(part.type)

            if ext:
                fn = f"attachment_{i}{ext}"

            else:
                console.print(
                    f"[red]{part.type} - Could not guess based on mimetype! Attachment not written.[/red]"
                )
                continue

        attachments.append(
            EmailAttachment(
                filename=Path(fn),
                data=part.data,
            )
        )

    return attachments



def extract_msg(
        filename: Path,
        console: Console = None,
        ) -> StandardEmail:
    """
    Transform the string to a StandardEmail message.

    # Args

    msg
        - The path to the EML file to process

    # Return

    StandardEmail

    """

    msg = Message(filename)

    header = EmailHeader(
        date=msg.date,
        subject=msg.subject,
        email_to=msg.to,
        email_from=msg.sender,
        reply_to=msg.reply_to,
        sender=msg.sender,
        cc=msg.cc,
        bcc=msg.bcc,
        others=None,
    )

    body = msg.body

    attachments = extract_msg_attachments(msg, console=console)

    return StandardEmail(
        header=header,
        body=body,
        attachments=attachments,
    )
