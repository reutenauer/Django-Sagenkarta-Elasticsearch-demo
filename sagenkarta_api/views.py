from django.http import JsonResponse
import requests, json

def getDocuments(request):
	# Elasticsearch query object
	data = {
		"query": {
			"term": {
				"title": "spöken"
			}
		}
	}
	response = requests.post('http://localhost:9200/sagenkarta/legend/_search', data=json.dumps(data))
	return JsonResponse(response.json());