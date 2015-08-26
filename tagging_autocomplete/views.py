from django.http import HttpResponse
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from tagging.models import Tag

def list_tags(request):
	max_results = getattr(settings, 'MAX_NUMBER_OF_RESULTS', 100)
	try:
		tags = Tag.objects.filter(name__istartswith=request.GET['q']).values_list('name', flat=True)[:max_results]
	except MultiValueDictKeyError:
	    tags = []
	
	return HttpResponse('\n'.join(tags), content_type='text/plain;charset=UTF-8')
