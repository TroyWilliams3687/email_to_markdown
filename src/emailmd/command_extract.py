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
from email import message_from_string  # processing EML
from email import policy

# ------------
# 3rd Party - From pip

import click


from rich.console import Console
console = Console()

from markdownify import markdownify # https://github.com/matthewwithanm/python-markdownify

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
        remove_tags=('span', 'font', 'div'),
    )

    return cleaner.clean_html(dirty_html)

def process_eml(email_path:Path, output:Path) -> None:
    """
    Given the email_path, read the contents, construct a markdown file
    and write the markdown and attachments to the output path

    # Args

    email_path
        - The path to the EML file to process

    output
        - The root folder to write the Markdown and attachments too

    # Return

    None

    """

    # https://docs.python.org/3/library/email.policy.html <- a policy needs to be defined
    msg = message_from_string(email_path.read_text(), policy=policy.SMTP)

    # # all keys
    # for k,v in msg.items():
    #     console.print(f'{k} -> {v}')

    # Selected header keys
    header_keys = [
        'Date',
        'Subject',
        'To',
        'From',
        'Message-ID',
        'In-Reply-To',
        'Thread-Index',
        'Thread-Topic',
    ]

    # get the email body, preferring the first, then the second
    # body = msg.get_body(('html', 'plain'))
    body = msg.get_body(('plain', 'html'))

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
            heading_style='ATX',
            escape_asterisks=False,
            escape_underscores=False,
        )

        body_content = body_md.strip()

    # Construct the markdown body including some of the email header information
    md = '\n'.join([f'{hk}: {msg[hk].strip()}' for hk in header_keys if hk in msg] + ['','----','\n'] ) + body_content

    # Construct the output folder

    message_name = sanitize_filename(msg['Subject'])

    message_folder = output / Path(message_name.lower())
    message_folder.mkdir(parents=True, exist_ok=True)

    # -----------
    # Write Attachments

    console.print(f'Attachments: {len(msg.get_payload())}')

    attachments = []

    for i, attachment in enumerate(msg.get_payload()):
        if attachment.get_content_maintype() == 'multipart':
            continue

        if attachment.get_filename():
            fn = Path(f'{sanitize_filename(attachment.get_filename())}')

            attachments.append(fn.name)

            attachment_name = message_folder / fn.name
            attachment_name.write_bytes(attachment.get_payload(decode=True))

        else:
            console.print('[red]Unable to determine attachment name![/red]')


    # ----------
    # Write the email to file based on the subject name

    md = md + '\n'.join(['','---', '', 'Attachments:', '', '']) + '\n'.join([f'- {a}' for a in attachments])

    message_file = message_folder / Path(f'{message_name.lower()}.md')
    message_file.write_text(md)





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
    kwargs['output'].mkdir(parents=True, exist_ok=True)

    for f in kwargs["files"]:
        console.print(f"Extracting: {f.name}...")

        if f.suffix.lower() == ".msg":
            pass

        elif f.suffix.lower() == ".eml":
            process_eml(f, kwargs['output'])

        else:
            console.print(f'[red]Unknown format -> {f.name}[/red]')

        console.print('---------')
