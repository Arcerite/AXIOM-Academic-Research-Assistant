# ENGINE/search.py

from ENGINE.filters import build_filter_string
from ENGINE.normalize import normalize_work
from ENGINE.openalex import search_openalex

def search(query):
    filters = build_filter_string()
    raw= search_openalex(query, filters=filters)
    return [normalize_work(work) for work in raw]
