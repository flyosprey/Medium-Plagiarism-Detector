from home.spiders.medium.spider import run_spider_medium
from home.plagiat_detector.plagiat_detector import plagiat_detector


def site_handler(datas: dict) -> dict:
    plagiarism_data, datas["site_name"] = {}, datas["site_name"].lower()
    if "medium" in datas["site_name"]:
        spider_data = run_spider_medium(datas)
        plagiarism_data = plagiat_detector(spider_data)
    else:
        plagiarism_data["error"] = "This site name does not supported!"
    return plagiarism_data

