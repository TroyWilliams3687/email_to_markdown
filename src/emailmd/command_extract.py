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

import mimetypes

from dataclasses import dataclass, fields
from pathlib import Path

from email import message_from_string  # processing EML
from email import policy
from email.message import EmailMessage

from typing import Optional

# ------------
# 3rd Party - From pip

import click

from rich.console import Console

console = Console()

from markdownify import (
    markdownify,
)  # https://github.com/matthewwithanm/python-markdownify

from lxml.html.clean import Cleaner
from pathvalidate import sanitize_filename

# ------------
# Custom Modules

# ------------


# Potential Email Header Keys
# Accept-Language
# ARC-Authentication-Results
# ARC-Message-Signature
# ARC-Seal
# Authentication-Results
# authentication-results
# Content-Language
# Content-Type
# Date
# Delivered-To
# DKIM-Signature
# From
# In-Reply-To
# Message-ID
# MIME-Version
# Received
# Received-SPF
# References
# Return-Path
# Subject
# Thread-Index
# Thread-Topic
# To
# x-forefront-antispam-report
# X-Google-Smtp-Source
# x-microsoft-antispam
# x-microsoft-antispam-message-info
# x-microsoft-antispam-prvs
# X-Mozilla-Keys
# X-Mozilla-Status
# X-Mozilla-Status2
# x-ms-exchange-antispam-messagedata-0
# x-ms-exchange-antispam-messagedata-chunkcount
# x-ms-exchange-antispam-relay
# X-MS-Exchange-CrossTenant-AuthAs
# X-MS-Exchange-CrossTenant-AuthSource
# X-MS-Exchange-CrossTenant-fromentityheader
# X-MS-Exchange-CrossTenant-id
# X-MS-Exchange-CrossTenant-mailboxtype
# X-MS-Exchange-CrossTenant-Network-Message-Id
# X-MS-Exchange-CrossTenant-originalarrivaltime
# X-MS-Exchange-CrossTenant-userprincipalname
# x-ms-exchange-senderadcheck
# X-MS-Exchange-Transport-CrossTenantHeadersStamped
# X-MS-Has-Attach
# x-ms-office365-filtering-correlation-id
# x-ms-publictraffictype
# X-MS-TNEF-Correlator
# x-ms-traffictypediagnostic
# X-OriginatorOrg
# X-Received


@dataclass
class EmailHeader:
    """ """

    date: str = None
    subject: str = None
    email_to: str = None
    email_from: str = None
    reply_to: str = None
    sender: str = None
    cc: str = None
    bcc: str = None
    others: dict[str, str] = None


@dataclass
class EmailAttachment:
    """ """

    filename: str = None
    data: bytes = None


@dataclass
class StandardEmail:
    """
    A way to represent a standard email message despite different input
    sources.
    """

    header: EmailHeader = None
    body: str = None
    attachments: list[EmailAttachment] = None

    def to_markdown(self, **kwargs):
        """

        # kwargs

        attachment_folder:str -> ''
            - The path to the attachment folder

        full_header:bool -> False
            - Display the full header information

        """

        attachment_folder = (
            kwargs["attachment_folder"] if "attachment_folder" in kwargs else ""
        )

        # Construct the markdown body including some of the email header information
        text = "\n".join(
            [
                f"Date: {self.header.date}",
                f"Subject: {self.header.subject}",
                f"To: {self.header.email_to}",
                f"From: {self.header.email_from}",
                f"Reply-To: {self.header.reply_to}",
                f"Sender: {self.header.sender}",
                f"CC: {self.header.cc}",
                f"BCC: {self.header.bcc}",
            ]
        )

        if "full_header" in kwargs and kwargs["full_header"]:
            text += (
                "\n".join(
                    [f"{k.strip()}: {v.strip()}" for k, v in self.header.others.items()]
                )
                if self.header.others
                else ""
            )

        text += "\n".join(["", "----", "\n"])

        text += self.body

        text += "\n".join(["", "---", "", "Attachments:", "", ""])

        text += "\n".join(
            [
                f"- {attachment_folder}/{a.filename}" if attachment_folder else f"- {a}"
                for a in self.attachments
            ]
        )

        return text


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

    [f"{hk}: {msg[hk].strip()}" for hk in header_keys if hk in msg]

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
    # body = msg.get_body(('html', 'plain'))
    body = msg.get_body(("plain", "html"))

    # console.print(f'Body Type: {body.get_content_type()}')
    # text/html
    # text/plain

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


def extract_eml_attachments(msg: EmailMessage) -> Optional[list[EmailAttachment]]:
    """ """

    attachments = []

    for i, part in enumerate(msg.get_payload()):
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


def extract_eml(msg: str) -> StandardEmail:
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
    attachments = extract_eml_attachments(email_message)

    return StandardEmail(
        header=header,
        body=body,
        attachments=attachments,
    )


def construct_non_duplicate_folder(
    root: Path, target: str, retry_count: int = 25
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


def construct_non_duplicate_file(filename: Path, retry_count: int = 25) -> Path:
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


def write_standard_email(email_message: StandardEmail, output: Path) -> None:
    """
    Given the StandardEmail, write it to the output folder, creating a
    new folder for the email and attachments.
    """

    message_name = sanitize_filename(email_message.header.subject)

    # Construct the output folder - from the subject
    message_folder = output / message_name.lower()
    message_folder.mkdir(parents=True, exist_ok=True)

    # message_folder = construct_non_duplicate_folder(output, message_name.lower())

    # construct the name of the email message
    # message_file = message_folder / Path(f"{message_name.lower()}.md")

    message_file = construct_non_duplicate_file(
        message_folder / Path(f"{message_name.lower()}.md")
    )
    message_file.write_text(email_message.to_markdown(attachment_folder="attachments"))

    console.print(f"Saved Email: [cyan]{message_file.name}[/cyan]")

    for attachment in email_message.attachments:

        attachment_folder = message_folder / Path("attachments")
        attachment_folder.mkdir(parents=True, exist_ok=True)

        attachment_file = attachment_folder / attachment.filename
        attachment_file.write_bytes(attachment.data)

        console.print(
            f"[yellow]Saved Attachment[/yellow]: [cyan]{attachment_file.name}[/cyan]"
        )


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
def extract(*args, **kwargs):
    """
    Extract the email messages (EML, MSG) to Markdown files placed in
    the OUTPUT folder.

    # Usage

    $ emailmd extract ~/email/*.msg ~/email/*.eml ~/email/output

    $ emailmd extract ~/"path to email"/*.msg ~/email/output

    $ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/email/output

    $ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/tmp/"email to markdown"/output

    """

    ctx = args[0]

    if len(kwargs["files"]) == 0:
        console.print("[red]No Files to process![/red]")
        ctx.abort()

    # console.print(f"Output: {kwargs['output']}...")
    kwargs["output"].mkdir(parents=True, exist_ok=True)

    for f in kwargs["files"]:
        console.print(f"Extracting: {f.name}...")

        if f.suffix.lower() == ".msg":
            pass

        elif f.suffix.lower() == ".eml":
            msg = extract_eml(f.read_text())
            write_standard_email(msg, kwargs["output"])
            # process_eml(f.read_text(), kwargs["output"])

        else:
            console.print(f"[red]Unknown format -> {f.name}[/red]")

        console.print("")

    console.print(f"[green]Complete[/green]")
