#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 8697adf6-e4dd-11ec-b705-4307570280a6
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-06-05
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from dataclasses import dataclass
from pathlib import Path

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

# -------------

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

    filename: Path = None
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
