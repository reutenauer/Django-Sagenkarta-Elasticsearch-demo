from django.http import JsonResponse
import requests, json, sys

def createQuery(request):
	# Parameters:

	#	söksträng (title, text, acc. number) X
	#	kategori X
	#	typ X
	#	institut ?
	#	topic X
	#	title_topic X

	#	insamlingsår (från och till) X
	#	insamlingsort (sockennamn, socken-id, harad, landskap, bounding box, ...)

	#	person relation
	#	födelseår
	#	namn
	#	kön
	#	födelseort

	if (len(request.GET) > 0):
		query = {
			'bool': {
				'must': []
			}
		}
	else:
		query = {}

	if ('collection_years' in request.GET):
		collectionYears = request.GET['collection_years'].split(',')

		query['bool']['must'].append({
			'range': {
				'year': {
					'gte': collectionYears[0],
					'lt': collectionYears[1]
				}
			}
		})

	if ('search' in request.GET):
		searchTerms = request.GET['search'].split(',')

		for term in searchTerms:
			query['bool']['must'].append({
				'bool': {
					'should': [
						{
							'match': {
								'title': term
							}
						},
						{
							'match': {
								'text': term
							}
						}
					]
				}
			})


	if ('category' in request.GET):
		categoryShouldBool = {
			'bool': {
				'should': []
			}
		}

		categoryStrings = request.GET['category'].split(',')

		for category in categoryStrings:
			categoryShouldBool['bool']['should'].append({
				'match': {
					'taxonomy.category': category
				}
			})
		query['bool']['must'].append(categoryShouldBool)


	if ('type' in request.GET):
		typeShouldBool = {
			'bool': {
				'should': []
			}
		}

		typeStrings = request.GET['type'].split(',')

		for type in typeStrings:
			typeShouldBool['bool']['should'].append({
				'match': {
					'type': type
				}
			})
		query['bool']['must'].append(typeShouldBool)


	if ('socken_id' in request.GET):
		sockenShouldBool = {
			'nested': {
				'path': 'places',
				'query': {
					'bool': {
						'should': []
					}
				}
			}
		}

		sockenIds = request.GET['socken_id'].split(',')

		for socken in sockenIds:
			sockenShouldBool['nested']['query']['bool']['should'].append({
					'match': {
						'places.id': socken
					}
			})

		query['bool']['must'].append(sockenShouldBool)



	if ('socken' in request.GET):
		sockenShouldBool = {
			'nested': {
				'path': 'places',
				'query': {
					'bool': {
						'should': []
					}
				}
			}
		}

		sockenNames = request.GET['socken'].split(',')

		for socken in sockenNames:
			sockenShouldBool['nested']['query']['bool']['should'].append({
					'match': {
						'places.name': socken
					}
			})

		query['bool']['must'].append(sockenShouldBool)


	if ('person' in request.GET):
		personShouldBool = {
			'nested': {
				'path': 'persons',
				'query': {
					'bool': {
						'must': [
							{
								'match': {
									'persons.name_analyzed': request.GET['person']
								}
							}
						]
					}
				}
			}
		}

		if ('person_relation' in request.GET):
			personShouldBool['nested']['query']['bool']['must'].append({
				'match': {
					'persons.relation': request.GET['person_relation']
				}
			})

		query['bool']['must'].append(personShouldBool)


	if ('person_exact' in request.GET):
		personShouldBool = {
			'nested': {
				'path': 'persons',
				'query': {
					'bool': {
						'must': [
							{
								'match': {
									'persons.name': request.GET['person_exact']
								}
							}
						]
					}
				}
			}
		}

		if ('person_relation' in request.GET):
			personShouldBool['nested']['query']['bool']['must'].append({
				'match': {
					'persons.relation': request.GET['person_relation']
				}
			})

		query['bool']['must'].append(personShouldBool)


	if ('topics' in request.GET):
		topicsShouldBool = {
			'nested': {
				'path': 'topics',
				'query': {
					'bool': {
						'must': []
					}
				}
			}
		}

		topicStrings = request.GET['topics'].split(',')

		for topic in topicStrings:
			topicsShouldBool['nested']['query']['bool']['must'].append({
				'nested': {
					'path': 'topics.terms',
					'query': {
						'bool': {
							'should': [
								{
									'function_score': {
										'query': {
											'match': {
												'topics.terms.term': topic
											}
										},
										'functions': [
											{
												'field_value_factor': {
													'field': 'topics.terms.probability'
												}
											}
										]
									}
								}
							]
						}
					}
				}
			})

		query['bool']['must'].append(topicsShouldBool)

	if ('title_topics' in request.GET):
		titleTopicsShouldBool = {
			'nested': {
				'path': 'title_topics',
				'query': {
					'bool': {
						'must': []
					}
				}
			}
		}

		titleTopicStrings = request.GET['title_topics'].split(',')

		for topic in titleTopicStrings:
			titleTopicsShouldBool['nested']['query']['bool']['must'].append({
				'nested': {
					'path': 'title_topics.terms',
					'query': {
						'bool': {
							'should': [
								{
									'function_score': {
										'query': {
											'match': {
												'title_topics.terms.term': topic
											}
										},
										'functions': [
											{
												'field_value_factor': {
													'field': 'title_topics.terms.probability'
												}
											}
										]
									}
								}
							]
						}
					}
				}
			})

		query['bool']['must'].append(titleTopicsShouldBool)

	return query

def esQuery(request, query):
	esResponse = requests.get('http://localhost:9200/sagenkarta_v2/legend/_search', data=json.dumps(query))
	
	responseData = esResponse.json()

	if ('showQuery' in request.GET) and request.GET['showQuery']:
		responseData['query'] = query

	jsonResponse = JsonResponse(responseData)
	jsonResponse['Access-Control-Allow-Origin'] = '*'

	return jsonResponse

def getDocument(request, documentId):
	esResponse = requests.get('http://localhost:9200/sagenkarta_v2/legend/'+documentId)

	jsonResponse = JsonResponse(esResponse.json())
	jsonResponse['Access-Control-Allow-Origin'] = '*'

	return jsonResponse

def getTopics(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'topics'
				},
				'aggs': {
					'data': {
						'nested': {
							'path': 'topics.terms'
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'topics.terms.term',
									'size': 100
								},
								'aggs': {
									'parent_doc_count': {
										'reverse_nested': {}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getTitleTopics(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'title_topics'
				},
				'aggs': {
					'data': {
						'nested': {
							'path': 'title_topics.terms'
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'title_topics.terms.term',
									'size': 100
								},
								'aggs': {
									'parent_doc_count': {
										'reverse_nested': {}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getCollectionYears(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'terms': {
					'field': 'year',
					'size': 10000,
					'order': {
						'_term': 'asc'
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getBirthYears(request, relation):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'persons'
				},
				'aggs': {
					'data': {
						'filter': {
							'term': {
								'persons.relation': relation
							}
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'persons.birth_year',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getCollectorsBirthYears(request):
	return getBirthYears(request, 'collector')

def getInformantsBirthYears(request):
	return getBirthYears(request, 'informant')

def getCategories(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'terms': {
					'field': 'taxonomy.category',
					'size': 10000,
					'order': {
						'_term': 'asc'
					}
				},
				'aggs': {
					'data': {
						'terms': {
							'field': 'taxonomy.name',
							'size': 10000,
							'order': {
								'_term': 'asc'
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getTypes(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'terms': {
					'field': 'type',
					'size': 10000,
					'order': {
						'_term': 'asc'
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getSocken(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'places'
				},
				'aggs': {
					'data': {
						'terms': {
							'field': 'places.id',
							'size': 10000
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'places.name',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'harad': {
								'terms': {
									'field': 'places.harad',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'landskap': {
								'terms': {
									'field': 'places.landskap',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'lan': {
								'terms': {
									'field': 'places.county',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getHarad(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'places'
				},
				'aggs': {
					'data': {
						'terms': {
							'field': 'places.harad_id',
							'size': 10000
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'places.harad',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'parent_doc_count': {
								'reverse_nested': {}
							},
							'landskap': {
								'terms': {
									'field': 'places.landskap',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'lan': {
								'terms': {
									'field': 'places.county',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getLandskap(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'places'
				},
				'aggs': {
					'data': {
						'terms': {
							'field': 'places.landskap',
							'size': 10000
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'places.county',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'parent_doc_count': {
								'reverse_nested': {}
							},
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse

def getPersons(request):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'persons'
				},
				'aggs': {
					'data': {
						'terms': {
							'field': 'persons.id',
							'size': 10000
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'persons.name',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'relation': {
								'terms': {
									'field': 'persons.relation',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								}
							},
							'home': {
								'terms': {
									'field': 'persons.home.id',
									'size': 10000,
									'order': {
										'_term': 'asc'
									}
								},
								'aggs': {
									'data': {
										'terms': {
											'field': 'persons.home.name',
											'size': 10000,
											'order': {
												'_term': 'asc'
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse


def getRelatedPersons(request, relation):
	query = {
		'query': createQuery(request),
		'size': 0,
		'aggs': {
			'data': {
				'nested': {
					'path': 'persons'
				},
				'aggs': {
					'data': {
						'filter': {
							'term': {
								'persons.relation': relation
							}
						},
						'aggs': {
							'data': {
								'terms': {
									'field': 'persons.id',
									'size': 10000
								},
								'aggs': {
									'data': {
										'terms': {
											'field': 'persons.name',
											'size': 10000,
											'order': {
												'_term': 'asc'
											}
										}
									},
									'relation': {
										'terms': {
											'field': 'persons.relation',
											'size': 10000,
											'order': {
												'_term': 'asc'
											}
										}
									},
									'home': {
										'terms': {
											'field': 'persons.home.id',
											'size': 10000,
											'order': {
												'_term': 'asc'
											}
										},
										'aggs': {
											'data': {
												'terms': {
													'field': 'persons.home.name',
													'size': 10000,
													'order': {
														'_term': 'asc'
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse


def getInformants(request):
	return getRelatedPersons(request, 'informant')


def getCollectors(request):
	return getRelatedPersons(request, 'collector')


def getDocuments(request):
	query = {
		'query': createQuery(request),
		'highlight' : {
			'fields' : {
				'text' : {}
			}
		}
	}

	esQueryResponse = esQuery(request, query)
	return esQueryResponse
