from django.http import JsonResponse
import requests, json, sys

def getDocument(request, documentId):
	response = requests.get('http://localhost:9200/sagenkarta/legend/'+documentId)
	return JsonResponse(response.json());

def getDocuments(request):
	# Elasticsearch query object
	if ('search' in request.GET) :
		data = {
			"query": {
				"bool": {
					"should": [
						{
							"match": {
								"type": "tryckt"
							}
						},
						{
							"match": {
								"type": "arkiv"
							}
						}
					],
					"must": [
						{
							"bool": {
								"should": [
									{
										"match": {
											"text": request.GET['search']
										}
									},
									{
										"match": {
											"text": request.GET['search']
										}
									}
								]
							}
						}
					]
				}
			}
		}
	else :
		data = {};

	response = requests.get('http://localhost:9200/sagenkarta/legend/_search', data=json.dumps(data))
	
	return JsonResponse(response.json());
