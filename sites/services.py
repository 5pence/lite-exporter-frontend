from conf.client import get, post
from conf.constants import SITES_URL


def get_sites(request):
    data = get(request, SITES_URL)
    return data.json(), data.status_code


def get_site(request, pk):
    data = get(request, SITES_URL + pk)
    return data.json(), data.status_code


def post_sites(request, json):
    data = post(request, SITES_URL, json)
    return data.json(), data.status_code