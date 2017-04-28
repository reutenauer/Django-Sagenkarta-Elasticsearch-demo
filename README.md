# Django-Sagenkarta-Elasticsearch-demo

Enkelt Django application som visar hur man kan göra enkel API som hämtar data från Elasticserach utan att definera models.
Django samt requests modulen måste vara installerad för att köra applicationen.
Applicationen startas via `python manage.py runserver`.

Koden för API:et finns i `sagenkarta_api/urls.py` och `sagenkarta_api/views.py`

## Hämta documenter
`[HOST]/sagenkarta/documents/`. Enkel sökning kan utföras med `[HOST]/sagenkarta/documents/**?search=häst**`

## Hämta enda dokument
`[HOST]/sagenkarta/document/[DOC_ID]`

## sagenkarta_es_api

`def createQuery(request)`
Tar inn request object från Django. Bygger upp Elasticsearch query.
Giltiga params:
- collection_years=[från,till]
-
