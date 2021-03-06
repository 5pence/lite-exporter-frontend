from conf.client import get, post
from conf.constants import GOODS_URL


def get_goods(request):
    data = get(request, GOODS_URL)
    return data.json(), data.status_code


def get_good(request, pk):
    data = get(request, GOODS_URL + pk)
    return data.json(), data.status_code


def post_goods(request, json):
    data = post(request, GOODS_URL, json)
    return data.json(), data.status_code
