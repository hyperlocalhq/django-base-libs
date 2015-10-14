# -*- coding: UTF-8 -*-

from hashlib import sha1

from django.utils.encoding import smart_str
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext
from django.db import models
from django.conf import settings

from base_libs.utils.client import Connection


def export_job_offer_to_creativeset(job_offer, test=False):
    Service = models.get_model("external_services", "Service")
    ObjectMapper = models.get_model("external_services", "ObjectMapper")
    ServiceActionLog = models.get_model("external_services", "ServiceActionLog")

    s, created = Service.objects.get_or_create(
        sysname="creativeset",
        defaults={
            'url': "http://www.creativeset.net/feeds/rss_extended/de/jobs.xml",
            'title': "Creativeset.net",
        },
    )

    creativeset = Connection("www.creativeset.net/jobapi/create")

    company_description = ""
    if job_offer.offering_institution:
        company_description = job_offer.offering_institution.description_de
    company_description = company_description or "&nbsp;"

    company_name = job_offer.offering_institution_title
    if job_offer.offering_institution:
        company_name = job_offer.offering_institution.get_title()

    key = sha1(settings.CREATIVESET_KEY_COMPONENT + smart_str(job_offer.position)).hexdigest()

    how_to_apply = [company_name]
    if job_offer.postal_address:
        address = job_offer.postal_address
        if address.street_address:
            how_to_apply.append(address.street_address)
        if address.street_address2:
            how_to_apply.append(address.street_address2)
        if address.street_address3:
            how_to_apply.append(address.street_address3)
        if address.postal_code and address.city:
            how_to_apply.append(address.postal_code + " " + address.city)
    how_to_apply.append("")
    if job_offer.contact_person:
        how_to_apply.append("Kontaktperson: %s" % job_offer.contact_person.get_title())
    else:
        how_to_apply.append("Kontaktperson: %s" % job_offer.contact_person_name)
    for phone in job_offer.get_phones():
        how_to_apply.append(
            "%s: +%s-%s-%s" % (phone['type'].title_de, phone['country'], phone['area'], phone['number']))
    for email in job_offer.get_emails():
        how_to_apply.append("%s: %s" % (ugettext("E-mail"), email['address']))
    how_to_apply.append("")
    for url in job_offer.get_urls():
        how_to_apply.append(url['link'])

    values = {
        'key': key,
        'company_id': settings.CREATIVESET_COMPANY_ID,

        'company_name': company_name,
        'title': job_offer.position,
        'job_description': job_offer.description,
        'company_description': company_description,
        'how_to_apply': "\n".join(how_to_apply),
        'city': job_offer.postal_address.city,
    }
    if test:
        values['test'] = "True"

    experiences = []
    # add job type
    mappers = s.objectmapper_set.filter(
        content_type__app_label="marketplace",
        content_type__model="jobtype",
        object_id=job_offer.job_type.pk,
    )
    if mappers:
        experiences.append(mappers[0].external_id)
    # add job qualifications
    for qualification in job_offer.qualifications.all():
        mappers = s.objectmapper_set.filter(
            content_type__app_label="marketplace",
            content_type__model="jobqualification",
            object_id=qualification.pk,
        )
        if mappers:
            experiences.append(mappers[0].external_id)

    if experiences:
        values['experiences'] = experiences

    branches = []
    # add job sectors
    for job_sector in job_offer.job_sectors.all():
        mappers = s.objectmapper_set.filter(
            content_type__app_label="marketplace",
            content_type__model="jobsector",
            object_id=job_sector.pk,
        )
        if mappers:
            branches.append(mappers[0].external_id)

    if branches:
        values['branches'] = branches

    if settings.DEBUG:
        values['test'] = "true"

    response = creativeset.send_request(
        headers={'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"},
        values=values,
    )

    response_text = "<undefined>"
    if int(response.code) == 201:  # resource created successfully
        response_text = response.read()

        external_id = response_text

        if external_id != "OK":
            # set object mapper so that the same job wouldn't be created again during the import
            mapper = ObjectMapper(
                service=s,
                external_id=external_id,
            )
            mapper.content_object = job_offer
            mapper.save()
    ServiceActionLog.objects.create(
        service=s,
        request=force_unicode(values),
        response=response_text,
        response_code=response.code,
    )
