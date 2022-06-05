#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 2022-06-05
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 59adf4be-e4e0-11ec-b705-4307570280a6
# -----------

"""
This is a template python script for use in creating other classes and applying
a standard to them
"""

# ------------
# System Modules - Included with Python

import mimetypes

from pathlib import Path

from email import message_from_string  # processing EML
from email import policy
from email.message import EmailMessage

from typing import Optional

# ------------
# 3rd Party - From PyPI

from rich.console import Console

from markdownify import (
    markdownify,
)  # https://github.com/matthewwithanm/python-markdownify


# ------------
# Custom Modules

from .standardemail import (
    EmailHeader,
    EmailAttachment,
    StandardEmail,
)

from .util import (
    sanitize,
)

# -------------

def extract_eml_header(msg: EmailMessage) -> EmailHeader:
    """ """

    # # all keys
    # for k,v in msg.items():
    #     console.print(f'{k} -> {v}')

    # Selected header keys
    header_keys = [
        "Date",
        "Subject",
        "To",
        "From",
        "Reply-To",
        "Sender",
        "Cc",
        "Bcc",
    ]

    # [f"{hk}: {msg[hk].strip()}" for hk in header_keys if hk in msg]

    return EmailHeader(
        date=msg["Date"],
        subject=msg["Subject"],
        email_to=msg["To"],
        email_from=msg["From"],
        reply_to=msg['Reply-To'],
        sender=msg['Sender'],
        cc=msg['Cc'],
        bcc=msg['Bcc'],
        others={k: v for k, v in msg.items() if k not in header_keys},
    )

def extract_eml_body(msg: EmailMessage) -> str:
    """ """

    # get the email body, preferring the first, then the second
    body = msg.get_body(("plain", "html"))

    if body is None:
        return ''

    body_content = body.get_content().strip()

    if body.get_content_type() == "text/html":

        # Clean the html
        good_html = sanitize(body_content)

        # convert to Markdown
        body_md = markdownify(
            good_html,
            heading_style="ATX",
            escape_asterisks=False,
            escape_underscores=False,
        )

        body_content = body_md.strip()

    return body_content


def extract_eml_attachments(
        msg: EmailMessage,
        console: Console = None,
        ) -> Optional[list[EmailAttachment]]:
    """ """

    attachments = []

    for i, part in enumerate(msg.get_payload()):

        if isinstance(part, str):
            continue

        # need to put a check in for EML as attachments and handle those appropriately?
        # if they are already encoded as binary, it should be fine.

        if part.get_content_maintype() == "multipart":
            continue

        fn = part.get_filename()
        if not fn:
            ext = mimetypes.guess_extension(part.get_content_type())

            if ext:
                fn = Path(f"attachment_{i}{ext}")

            else:
                console.print(
                    f"[red]{part.get_content_type()} - Could not guess based on mimetype! Attachment not written.[/red]"
                )
                continue

        attachments.append(
            EmailAttachment(
                filename=fn,
                data=part.get_payload(decode=True),
            )
        )

    return attachments


def extract_eml(
        msg: str,
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

    # https://docs.python.org/3/library/email.policy.html <- a policy needs to be defined
    email_message = message_from_string(msg, policy=policy.SMTP)

    header = extract_eml_header(email_message)
    body = extract_eml_body(email_message)
    attachments = extract_eml_attachments(email_message, console=console)

    return StandardEmail(
        header=header,
        body=body,
        attachments=attachments,
    )
