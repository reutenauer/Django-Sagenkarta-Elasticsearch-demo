from django.http import JsonResponse
import requests, json, sys

def getRecords(request):
	return JsonResponse({
		'response': 'success'
	});
