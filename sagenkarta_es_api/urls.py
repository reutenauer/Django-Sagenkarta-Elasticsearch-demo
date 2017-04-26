from django.conf.urls import url

from . import views

urlpatterns = [
	#	kategorier: agg
	#	socken: agg
	#	topics: agg
	#	kön: agg
	#	insamlingsår: agg
	#	födelseår: agg
	#	personer: agg

	#	documents: list
	url(r'^documents/', views.getDocuments, name='getDocuments'),

	# aggregate topics
	url(r'^topics/', views.getTopics, name='getTopics'),

	# aggregate title topics
	url(r'^title_topics/', views.getTitleTopics, name='getTitleTopics'),

	# aggregate topics
	url(r'^topics/', views.getTopics, name='getTopics'),

	# aggregate upptäckningsår
	url(r'^collection_years/', views.getCollectionYears, name='getCollectionYears'),

	# aggregate födelseår
	url(r'^collectors_birth_years/', views.getCollectorsBirthYears, name='getCollectorsBirthYears'),

	# aggregate födelseår
	url(r'^informants_birth_years/', views.getInformantsBirthYears, name='getInformantsBirthYears'),

	# aggregate kategorier
	url(r'^categories/', views.getCategories, name='getCategories'),

	# aggregate kategorier
	url(r'^types/', views.getTypes, name='getTypes'),

	# aggregate socken
	url(r'^socken/', views.getSocken, name='getSocken'),

	# aggregate harad
	url(r'^harad/', views.getHarad, name='getHarad'),

	# aggregate landskap
	url(r'^landskap/', views.getLandskap, name='getLandskap'),

	# aggregate personer
	url(r'^persons/', views.getPersons, name='getPersons'),

	# aggregate informants
	url(r'^informants/', views.getInformants, name='getInformants'),

	# aggregate upptäcknare
	url(r'^collectors/', views.getCollectors, name='getCollectors'),

	url(r'^document/(?P<documentId>[^/]+)/$', views.getDocument, name='getDocument'),
]