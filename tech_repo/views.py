from django.http import JsonResponse
from .models import District

def get_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)