# -*- coding: UTF-8 -*-
import smtplib, rfc822, random, time, re
from email.Header import Header

from django.conf import settings
from django.contrib.sites.models import Site

from base_libs.utils.misc import html_to_plain_text
from base_libs.utils.emails import is_valid_email, get_email_and_name

class BadHeaderError(ValueError):
    pass

def check_if_valid(val):
    if '\n' in val or '\r' in val:
        raise BadHeaderError, "Header values can't contain newlines (got %r for header value)" % val
    return val

def prepare_email_address(email):
    def encode_name(match):
        return "%s <%s>" % (Header(match.group(1), "utf-8"), match.group(2))
    return re.sub(r'^([^<]+)<([^>]+)>$', encode_name, email)

def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD, plain_message=""):
    DNS_NAME = Site.objects.get_current().domain
    from_email = prepare_email_address(from_email)
    recipient_list = map(prepare_email_address, recipient_list)
    random_bits = ''.join([random.choice('1234567890') for i in range(19)])
    message = createhtmlmail(
        subject=str(Header(check_if_valid(subject), "utf-8")),
        html=message,
        text=plain_message,
        headers=(
            ("From", check_if_valid(from_email)),
            ("To", check_if_valid(", ".join(recipient_list))),
            ("Date", rfc822.formatdate()),
            ("Message-ID", "<%d.%s@%s>" % (time.time(), random_bits, DNS_NAME)),
        ),)
    num_sent = 0
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        if auth_user and auth_password:
            server.login(auth_user, auth_password)
    except:
        if fail_silently:
            return
        raise
    try:
        server.sendmail(from_email, recipient_list, message)
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

def send_mass_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD, plain_message=""):
    DNS_NAME = Site.objects.get_current().domain
    from_email = prepare_email_address(from_email)
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
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
        message = createhtmlmail(
            subject=str(Header(check_if_valid(subject), "utf-8")),
            html=message,
            text=plain_message,
            headers=(
                ("From", check_if_valid(from_email)),
                ("To", check_if_valid(recipient)),
                ("Date", rfc822.formatdate()),
                ("Message-ID", "<%d.%s@%s>" % (time.time(), random_bits, DNS_NAME)),
            ),)
        try:
            server.sendmail(from_email, recipient, message)
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

def createhtmlmail(subject, html, text="", headers=[]):
    """Create a mime-message that will render HTML in popular
       MUAs, text in better ones"""
    import MimeWriter
    import mimetools
    import cStringIO
    
    out = cStringIO.StringIO() # output buffer for our message 
    htmlin = cStringIO.StringIO(html)
    
    if not text:
        text = html_to_plain_text(html)
    txtin = cStringIO.StringIO(text)
    
    writer = MimeWriter.MimeWriter(out)
    #
    # set up some basic headers... we put subject here
    # because smtplib.sendmail expects it to be in the
    # message body
    #
    for header,value in headers:
        writer.addheader(header, value)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    #
    # start the multipart section of the message
    # multipart/alternative seems to work better
    # on some MUAs than multipart/mixed
    #
    writer.startmultipartbody("alternative")
    writer.flushheaders()
    #
    # the plain text section
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'utf-8')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    #
    # start the html subpart of the message
    #
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    #
    # returns us a file-ish object we can write to
    #
    pout = subpart.startbody("text/html", [("charset", 'utf-8')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    #
    # Now that we're done, close our writer and
    # return the message body
    #
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg

