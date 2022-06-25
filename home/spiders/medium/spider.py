import json
import requests
from home.models import RequestData
from home.spiders.medium.init_spider import _get_medium_params


def run_spider_medium(datas: dict) -> dict:
    article_id, spider_data, articles = 0, {}, []
    pages = datas["number_of_articles"] // 100 if datas["number_of_articles"] > 100 else 1
    for page in range(0, pages):
        limit = 100 if datas["number_of_articles"] > 100 else datas["number_of_articles"]
        datas["number_of_articles"] -= limit
        response = _send_request(datas, page, limit)
        json_data = _check_json_data(response)
        spider_data["request_data_id"] = RequestData.objects.latest('id').id
        spider_data["error"], spider_data["articles"] = json_data.get("error", ""), []
        if spider_data["error"]:
            return spider_data
        articles, article_id = _parse_articles(json_data, article_id, articles)
    spider_data["articles"] = articles
    return spider_data


def _send_request(datas: dict, page: int, limit: int) -> requests.request:
    url, payload, headers = _get_medium_params()
    payload = _update_payload(payload, datas, page, limit)
    response = requests.request(method="POST", url=url, headers=headers, data=json.dumps(payload))
    return response


def _check_json_data(response: requests.request) -> dict:
    json_data = {}
    if response.status_code == 200:
        if response.text:
            json_data = json.loads(response.text)[0]
            if json_data["data"]["search"]["posts"]["pagingInfo"]["next"] is not None:
                return json_data
            else:
                json_data["error"] = "Error! You selected number of articles out of range! Try again!"
        else:
            json_data["error"] = "Error on Medium.com!"
    elif response.status_code == 408:
        json_data["error"] = "Error! You selected number of articles out of range! Try again!"
    else:
        json_data["error"] = f"Crawler error! Try again!"
    return json_data


def _parse_articles(json_data: dict, article_id: int, articles: list) -> (list, int):
    items = json_data["data"]["search"]["posts"]["items"]
    for item in items:
        text = ""
        for paragraph in item["extendedPreviewContent"]["bodyModel"]["paragraphs"]:
            text = f"{text} {paragraph['text']}" if paragraph["type"] == "P" else text
        articles.append({
            "id": article_id, "title": item["title"], "url": item["mediumUrl"], "text": text.strip()
        })
        article_id += 1
    return articles, article_id


def _update_payload(payload: dict, datas: dict, page: int, limit: int) -> dict:
    payload[0]["variables"]["query"] = datas["topic"]
    payload[0]["variables"]["pagingOptions"]["limit"] = limit
    payload[0]["variables"]["pagingOptions"]["page"] = page
    return payload
