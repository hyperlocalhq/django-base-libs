from datetime import datetime
from datetime import timedelta
from mailsnake import MailSnake

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now


def sync_mc_list(ml):
    Settings = models.get_model("mailchimp", "Settings")
    Subscription = models.get_model("mailchimp", "Subscription")
    st = Settings.objects.get()
    ms = MailSnake(st.api_key)

    messages = []

    if ml.mailchimp_id:
        last_sync = ml.last_sync or datetime(2000, 1, 1)
        mc_last_sync = last_sync - timedelta(hours=2)  # GMT time

        triggered_emails = []

        # add or change subscribed members
        counter = 0
        for mc_member in ms.listMembers(
            id=ml.mailchimp_id,
            status="subscribed",
            since=mc_last_sync.strftime("%Y-%m-%d %H:%M:%S"),
            limit=3000,
        )['data']:

            mc_member_info = ms.listMemberInfo(
                id=ml.mailchimp_id,
                email_address=mc_member['email'],
            )

            sub, created = Subscription.objects.get_or_create(
                email=mc_member['email'],
                mailinglist=ml,
                defaults={
                    'first_name':
                        mc_member_info['data'][0]['merges'].get('FNAME', ""),
                    'last_name':
                        mc_member_info['data'][0]['merges'].get('LNAME', ""),
                    'ip':
                        "127.0.0.1",
                }
            )
            sub.status = "subscribed"
            sub.save()
            triggered_emails.append(mc_member['email'])
            counter += 1
        if counter:
            messages.append(
                _(
                    "%(counter)d members at %(list_title)s added from MailChimp."
                ) % {
                    'counter': counter,
                    'list_title': ml.title,
                }
            )

        # add or change updated members
        counter = 0
        for mc_member in ms.listMembers(
            id=ml.mailchimp_id,
            status="updated",
            since=mc_last_sync.strftime("%Y-%m-%d %H:%M:%S"),
            limit=3000,
        )['data']:

            mc_member_info = ms.listMemberInfo(
                id=ml.mailchimp_id,
                email_address=mc_member['email'],
            )

            sub, created = Subscription.objects.get_or_create(
                email=mc_member['email'],
                mailinglist=ml,
                defaults={
                    'first_name':
                        mc_member_info['data'][0]['merges'].get('FNAME', ""),
                    'last_name':
                        mc_member_info['data'][0]['merges'].get('LNAME', ""),
                    'ip':
                        "127.0.0.1",
                }
            )
            sub.first_name = mc_member_info['data'][0]['merges'].get(
                'FNAME', ""
            )
            sub.last_name = mc_member_info['data'][0]['merges'].get('LNAME', "")
            sub.status = "subscribed"
            sub.save()
            triggered_emails.append(mc_member['email'])
            counter += 1
        if counter:
            messages.append(
                _(
                    "%(counter)d members at %(list_title)s updated from MailChimp."
                ) % {
                    'counter': counter,
                    'list_title': ml.title,
                }
            )

        # add or change unsubscribed members
        counter = 0
        for mc_member in ms.listMembers(
            id=ml.mailchimp_id,
            status="unsubscribed",
            since=mc_last_sync.strftime("%Y-%m-%d %H:%M:%S"),
            limit=3000,
        )['data']:

            mc_member_info = ms.listMemberInfo(
                id=ml.mailchimp_id,
                email_address=mc_member['email'],
            )

            sub, created = Subscription.objects.get_or_create(
                email=mc_member['email'],
                mailinglist=ml,
                defaults={
                    'first_name':
                        mc_member_info['data'][0]['merges'].get('FNAME', ""),
                    'last_name':
                        mc_member_info['data'][0]['merges'].get('LNAME', ""),
                    'ip':
                        "127.0.0.1",
                }
            )
            sub.status = "unsubscribed"
            sub.save()
            triggered_emails.append(mc_member['email'])
            counter += 1
        if counter:
            messages.append(
                _(
                    "%(counter)d members at %(list_title)s unsubscribed from MailChimp."
                ) % {
                    'counter': counter,
                    'list_title': ml.title,
                }
            )

        # subscribe or unsubscribe on MailChimp
        subscribed_counter = 0
        unsubscribed_counter = 0
        for sub in ml.subscription_set.filter(
            models.Q(creation_date__gt=last_sync) |
            models.Q(modified_date__gt=last_sync)
        ):
            if sub.status == "subscribed" and sub.email not in triggered_emails:
                if ms.listSubscribe(
                    id=ml.mailchimp_id,
                    email_address=sub.email,
                    merge_vars={
                        'FNAME': sub.first_name,
                        'LNAME': sub.last_name,
                    },
                    double_optin=False,
                    update_existing=True,
                    send_welcome=False,
                ):
                    subscribed_counter += 1
            elif sub.status == "unsubscribed" and sub.email not in triggered_emails:
                if ms.listUnsubscribe(
                    id=ml.mailchimp_id,
                    email_address=sub.email,
                    delete_member=False,
                    send_goodbye=False,
                    send_notify=False,
                ):
                    unsubscribed_counter += 1
        if subscribed_counter:
            messages.append(
                _(
                    "%(counter)d members at %(list_title)s subscribed on MailChimp."
                ) % {
                    'counter': subscribed_counter,
                    'list_title': ml.title,
                }
            )
        if unsubscribed_counter:
            messages.append(
                _(
                    "%(counter)d members at %(list_title)s unsubscribed on MailChimp."
                ) % {
                    'counter': unsubscribed_counter,
                    'list_title': ml.title,
                }
            )

        ml.last_sync = tz_now()
        ml.save()
    return messages
