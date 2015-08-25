import datetime

from django.http import HttpResponse, Http404
from django.utils.encoding import smart_str
from django.template import loader

from base_libs.utils.misc import get_website_url


def simulate_idea_list_service(request):
    """
    provides xml for testing the jovoto rest services (lists)
    """
    ideas = []
    for i in range(1, 300):
        idea = {'name': "Idea Name %s" % i, 'description': "Idea Description %s" % i,
                'pubdate': datetime.datetime.now(), 'link': "%sexternal/jovoto/idea/%s" % (get_website_url(), i),
                'guid': "%sexternal/jovoto/simulate/%s.xml" % (get_website_url(), i)}

        media = []
        for m in range(1, 4):
            media_dict = {'type': "Image",
                          'thumb': "http://www.tacamo.de/weiterebilder/thumbnails/9310211111167699.jpg",
                          'medium': "http://i16.photobucket.com/albums/b38/KombatXcore/spongebob-schwammkopf-vol-3-02.jpg",
                          'big': "http://msnbcmedia4.msn.com/j/msnbc/Components/Photos/070416/070416_spongebob_vmed_1p.widec.jpg",
                          'path': "http://msnbcmedia4.msn.com/j/msnbc/Components/Photos/070416/070416_spongebob_vmed_1p.widec.jpg"}
            media.append(media_dict)

        idea['media'] = media
        ideas.append(idea)
    try:
        xml = smart_str(loader.render_to_string('simulate_idea_list.xml', {'ideas': ideas}))
        return HttpResponse(xml, content_type='application/xml')
    except:
        raise Http404, "The requested object is not available"


def simulate_idea_details_service(request, ext_id):
    """
    provides xml for testing the jovoto rest services (lists)
    """
    idea = {'name': "Idea Name %s" % ext_id, 'description': "Idea Description %s" % ext_id,
            'updated_at': datetime.datetime.now(), 'pubdate': datetime.datetime.now(),
            'link': "%sjovoto/idea/%s" % (get_website_url(), ext_id), 'author_username': "Author username %s" % ext_id,
            'author_city': "Author city %s" % ext_id, 'author_country': "Author country %s" % ext_id,
            'author_icon': "http://www.mister-wong.de/img/avatars/48/de-168709.jpg"}

    media = []
    for m in range(1, 4):
        media_dict = {'type': "Image", 'thumb': "http://www.tacamo.de/weiterebilder/thumbnails/9310211111167699.jpg",
                      'medium': "http://i16.photobucket.com/albums/b38/KombatXcore/spongebob-schwammkopf-vol-3-02.jpg",
                      'big': "http://msnbcmedia4.msn.com/j/msnbc/Components/Photos/070416/070416_spongebob_vmed_1p.widec.jpg",
                      'path': "http://msnbcmedia4.msn.com/j/msnbc/Components/Photos/070416/070416_spongebob_vmed_1p.widec.jpg"}
        media.append(media_dict)

    idea['media'] = media

    try:
        xml = smart_str(loader.render_to_string('simulate_idea_details.xml', {'idea': idea}))
        return HttpResponse(xml, content_type='application/xml')
    except:
        raise Http404, "The requested object is not available"
