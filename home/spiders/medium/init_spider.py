import json
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def _get_medium_params() -> (str, dict, dict):
    url = "https://medium.com/_/graphql"
    user_agent = get_user_agent()
    query = _get_query()
    payload = _get_payload(query)
    headers = _get_headers(user_agent)
    return url, payload, headers


def get_user_agent() -> str:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                   hardware_type="computer", limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent


def _get_query() -> dict:
    with open('home/spiders/medium/graphql_query.json', 'r') as json_file:
        query = json.load(json_file)
    return query


def _get_payload(query: dict):
    payload = [
        {
            "operationName": "SearchQuery",
            "variables": {
                "query": "",
                "pagingOptions": {
                    "limit": 100,
                    "page": 0
                },
                "withUsers": False,
                "withTags": False,
                "withPosts": True,
                "withCollections": False,
                "searchInCollection": False,
                "collectionDomainOrSlug": "medium.com",
            },
            "query": query["query"]
        }
    ]
    return payload


def _get_headers(user_agent: str) -> dict:
    headers = {
        'authority': 'medium.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'graphql-operation': 'SearchQuery',
        'origin': 'https://medium.com',
        'user-agent': user_agent
    }
    return headers
