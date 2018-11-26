# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option


class Command(NoArgsCommand):
    help = """Collects ad impressions and clicks"""

    def handle_noargs(self, **options):
        from django.contrib.auth.models import User
        from jetson.apps.mailing.models import EmailTemplate, EmailTemplatePlaceholder

        super_user = User.objects.filter(is_superuser=True).order_by('id')[0]

        ### Account created ###
        try:
            EmailTemplate.objects.get(slug="account_created")
        except EmailTemplate.DoesNotExist:
            account_created = EmailTemplate(slug="account_created")
            account_created.owner = super_user
            account_created.name = u"Account Created"
            account_created.subject = u"[site_name]: Welcome!"
            account_created.subject_de = u"[site_name]: Willkommen!"
            account_created.body = u"""Welcome to [site_name]!.

Your username is: [recipient_slug]
You can log in at: [website_url]login/

Enjoy the site, and do let us know if you have comments, concerns, suggestions, or other feedback!

The [site_name] team"""
            account_created.body_de = u"""Willkommen bei [asite_name]!.

Ihr Benutzername ist: [recipient_slug]
Sie können sich nun anmelden unter: [website_url]login/

Wir freuen uns über Ihren Besuch und auf ihre Kommentare, Beiträge und Vorschläge!

Das Team von [site_name]"""
            account_created.body_html = u"""<p>Welcome to [site_name]!</p>

<p>Your username is: [recipient_slug]</p>
<p>You can <a href="[website_url]login/">login here</a></p>

<p> Enjoy the site, and do let us know if you have comments, concerns, suggestions, or other feedback!</p>

<p> The [site_name] team</p>"""
            account_created.body_html_de = u"""<p>Willkommen bei [site_name]!</p>

<p>Ihr Benutzername ist: [recipient_slug]</p>
<p>Sie können <a href="[website_url]login/">hier sich nun anmelden</a></p>

<p> Wir freuen uns &uuml;ber Ihren Besuch und auf ihre Kommentare, Beiträge und Vorschläge!</p>

<p>Das Team von [site_name]</p>"""
            account_created.save()
            account_created.allowed_placeholders.add(
                *list(EmailTemplatePlaceholder.objects.all())
            )

        ### Account created ###
        try:
            EmailTemplate.objects.get(slug="account_verification")
        except EmailTemplate.DoesNotExist:
            account_verification = EmailTemplate(slug="account_verification")
            account_verification.owner = super_user
            account_verification.name = u"Account Verification"
            account_verification.subject = u"[site_name]: Account Verification Required"
            account_verification.subject_de = u"[site_name]: Benutzerkonto Anmeldung erforderlich"
            account_verification.body = u"""You're receiving this e-mail because you (or someone using your email address) is attempting to create an account at [site_name].

To verify your e-mail address and continue the registration process, please click the link below:

[website_url]signup/[encrypted_email]/

If you have no idea what this e-mail is referring to, simply ignore it and no account will be created with your e-mail address.

Thanks,
The [site_name] team"""
            account_verification.body_de = u"""Sie erhalten diese Mail, weil Sie für folgende Website ein neues Konto erstellt haben (oder jemand hat Ihre E-Mail Adresse benutzt): [site_name].

Um Ihre E-Mail Adresse zu bestätigen und Ihre Registrierung abschliessen zu können, klicken Sie bitte auf den folgenden Link:

[website_url]signup/[encrypted_email]/

Wenn Sie nicht wissen, worauf sich diese E-mail bezieht, ignorieren Sie sie einfach und es wird kein Benutzerkonto mit Ihrer E-Mail Adresse erstellt.

Danke,
Das [site_name] Team"""
            account_verification.body_html = u"""<p>You're receiving this e-mail because you (or someone using your email address) is attempting to create an account at [site_name].</p>

<p>Please <a href="[website_url]signup/[encrypted_email]/">verify your registration process</a>.</p>

<p>If you have no idea what this e-mail is referring to, simply ignore it and no account will be created with your e-mail address.</p>

<p>Thanks,<br />
The [site_name] team</p>"""
            account_verification.body_html_de = u"""<p>Sie erhalten diese Mail, weil Sie für folgende Website ein neues Konto erstellt haben (oder jemand hat Ihre E-Mail Adresse benutzt): [site_name].</p>

<p>Um Ihre E-Mail Adresse zu bestätigen und Ihre Registrierung abschliessen zu können, klicken Sie bitte auf den folgenden Link:</p>

<p><a href="[website_url]signup/[encrypted_email]/">[website_url]signup/[encrypted_email]/</a></p>

<p>Wenn Sie nicht wissen, worauf sich diese E-mail bezieht, ignorieren Sie sie einfach und es wird kein Benutzerkonto mit Ihrer E-Mail Adresse erstellt.</p>

<p>Danke,<br />
Das [site_name] Team</p>"""
            account_verification.save()
            account_verification.allowed_placeholders.add(
                *list(EmailTemplatePlaceholder.objects.all())
            )
