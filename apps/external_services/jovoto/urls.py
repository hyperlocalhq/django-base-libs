from django.conf.urls import url, patterns, include
from django.conf import settings

from jetson.apps.utils.context_processors import prev_next_processor

jovoto_ideas_info = {
    'paginate_by': 5,
    'allow_empty': True,
    'context_processors' : (prev_next_processor,),   
}

urlpatterns = patterns('',
    
    # urls for simulating jovoto web service locally 
    # (should be disabled when havin access to the real webservices!
    url(r'^simulate/idea_list.xml$', 'ccb.apps.external_services.jovoto.simulate_service.simulate_idea_list_service'),
    url(r'^simulate/(?P<ext_id>\d+).xml$', 'ccb.apps.external_services.jovoto.simulate_service.simulate_idea_details_service'),
    
    # urls for jovoto idea contest
    url(r'^$', 'ccb.apps.external_services.jovoto.views.get_all_ideas', dict(jovoto_ideas_info, template_name='external_services/jovoto/ideas_list.html'),),
    url(r'^page(?P<page>[0-9]+)/$', 'ccb.apps.external_services.jovoto.views.get_all_ideas', dict(jovoto_ideas_info, template_name='external_services/jovoto/ideas_list.html'),),    
    
    url(r'^idea/(?P<ext_id>\d+)/$', 'ccb.apps.external_services.jovoto.views.get_idea', dict(jovoto_ideas_info, template_name='external_services/jovoto/idea_details.html'),),
    
    # comments for jovoto ideas
    # adding comments (with and without ajax) 
    url(r'^idea/(?P<ext_id>\d+)/comments/add/$',
         'ccb.apps.external_services.jovoto.views.idea_post_comment', {'use_ajax' : False }),
    url(r'^idea/(?P<ext_id>\d+)/comments/add_ajax/$',
         'ccb.apps.external_services.jovoto.views.idea_post_comment', {'use_ajax' : True }),
    # displaying comments         
    url(r'^idea/(?P<ext_id>\d+)/comments/',
        include( 'jetson.apps.comments.urls.comments')),
    
    # refusing comments (with and without ajax)
    url(r'^idea/(?P<ext_id>\d+)/helper/comment/(?P<comment_id>\d+)/refuse/$', 
         'ccb.apps.external_services.jovoto.views.idea_refuse_comment', 
         {
              'use_popup' : True,
              'template_name' : 'external_services/jovoto/comments/popups/comment_refuse.html',
         }
    ),
    url(r'^idea/(?P<ext_id>\d+)/comment/(?P<comment_id>\d+)/refuse/$', 
     'ccb.apps.external_services.jovoto.views.idea_refuse_comment', {'use_popup' : True}),
     
    # accepting comments (with and without ajax)     
    (r'^idea/(?P<ext_id>\d+)/helper/comment/(?P<comment_id>\d+)/accept/$', 
         'ccb.apps.external_services.jovoto.views.idea_accept_comment', 
         {
              'use_popup' : True,
              'template_name' : 'external_services/jovoto/comments/popups/comment_accept.html',
         }
    ),
    url(r'^idea/(?P<ext_id>\d+)/comment/(?P<comment_id>\d+)/accept/$', 
     'ccb.apps.external_services.jovoto.views.idea_accept_comment', {'use_popup' : True}),     

    # spam marking (with and withou ajax)
    url(r'^idea/(?P<ext_id>\d+)/helper/comment/(?P<comment_id>\d+)/mark_as_spam/$', 
         'ccb.apps.external_services.jovoto.views.idea_mark_as_spam_comment', 
         {
              'use_popup' : True,
              'template_name' : 'external_services/jovoto/comments/popups/comment_markasspam.html',
         }
    ),
    url(r'^idea/(?P<ext_id>\d+)/comment/(?P<comment_id>\d+)/mark_as_spam/$', 
        'ccb.apps.external_services.jovoto.views.idea_mark_as_spam_comment', {'use_popup' : True}),
    
)
