# -*- coding: UTF-8 -*-
import smtplib
import rfc822
import random
import time
import re

from email.header import Header
from email import Charset

from django.conf import settings
from django.contrib.sites.models import Site

from base_libs.utils.misc import html_to_plain_text

# based on http://www.askthepony.com/blog/2011/06/how-to-send-a-proper-unicode-encoded-email-using-python-2-7/


class BadHeaderError(ValueError):
    pass


def check_if_valid(val):
    if '\n' in val or '\r' in val:
        raise BadHeaderError(
            "Header values can't contain newlines (got %r for header value)" %
            val
        )
    return val


def prepare_email_address(email):
    def encode_name(match):
        return '"%s" <%s>' % (
            str(Header(match.group(1), settings.DEFAULT_CHARSET.lower())),
            match.group(2)
        )

    return re.sub(r'^([^<]+)<([^>]+)>$', encode_name, email)


def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=settings.EMAIL_HOST_USER,
    auth_password=settings.EMAIL_HOST_PASSWORD,
    plain_message=""
):
    DNS_NAME = Site.objects.get_current().domain
    from_email = prepare_email_address(from_email)
    recipient_list = map(prepare_email_address, recipient_list)
    random_bits = ''.join([random.choice('1234567890') for i in range(19)])

    msg = createhtmlmail(
        subject=str(
            Header(check_if_valid(subject), settings.DEFAULT_CHARSET.lower())
        ),
        html=message,
        text=plain_message,
        headers=(
            ("From", from_email),
            ("To", check_if_valid(", ".join(recipient_list))),
            ("Date", rfc822.formatdate()),
            ("Message-ID", "<%d.%s@%s>" % (time.time(), random_bits, DNS_NAME)),
        ),
    )

    num_sent = 0
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        if settings.EMAIL_USE_TLS:
            server.starttls()
        if auth_user and auth_password:
            server.login(auth_user, auth_password)
    except:
        if fail_silently:
            return
        raise
    try:
        server.sendmail(from_email, recipient_list, msg)
        num_sent += 1
    except:
        if not fail_silently:
            raise
    try:
        server.quit()
    except:
        if fail_silently:
            return
        raise
    return num_sent


def send_mass_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=settings.EMAIL_HOST_USER,
    auth_password=settings.EMAIL_HOST_PASSWORD,
    plain_message=""
):
    DNS_NAME = Site.objects.get_current().domain
    from_email = prepare_email_address(from_email)
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        if settings.EMAIL_USE_TLS:
            server.starttls()
        if auth_user and auth_password:
            server.login(auth_user, auth_password)
    except:
        if fail_silently:
            return
        raise

    num_sent = 0
    for recipient in recipient_list:
        recipient = prepare_email_address(recipient)
        random_bits = ''.join([random.choice('1234567890') for i in range(19)])
        msg = createhtmlmail(
            subject=str(
                Header(
                    check_if_valid(subject), settings.DEFAULT_CHARSET.lower()
                )
            ),
            html=message,
            text=plain_message,
            headers=(
                ("From", from_email),
                ("To", check_if_valid(recipient)),
                ("Date", rfc822.formatdate()),
                (
                    "Message-ID",
                    "<%d.%s@%s>" % (time.time(), random_bits, DNS_NAME)
                ),
            ),
        )
        try:
            server.sendmail(from_email, recipient, msg)
            num_sent += 1
        except:
            if not fail_silently:
                raise

    try:
        server.quit()
    except:
        if fail_silently:
            return
        raise
    return num_sent


def createhtmlmail(subject, html, text="", headers=()):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    Charset.add_charset(
        settings.DEFAULT_CHARSET, Charset.QP, Charset.QP,
        settings.DEFAULT_CHARSET
    )

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    for header, value in headers:
        msg[header] = value

    # Create the body of the message (a plain-text and an HTML version).
    if not text:
        text = html_to_plain_text(html)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain', settings.DEFAULT_CHARSET)
    part2 = MIMEText(html, 'html', settings.DEFAULT_CHARSET)

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    return msg.as_string()
