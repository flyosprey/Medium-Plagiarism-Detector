from numpy import ndarray, float64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from home.models import Plagiarism


def plagiat_detector(spider_data: dict) -> dict:
    plagiarism_data = {"number_of_plagiarism": 0, "error": ""}
    if spider_data["error"]:
        plagiarism_data["error"] = spider_data["error"]
        return plagiarism_data
    s_vectors, new_vectors = _get_params(spider_data["articles"])
    plagiat_datas = _check_plagiarism(s_vectors, new_vectors)
    plagiarism_results = _sort_plagiarism(plagiat_datas)
    if plagiarism_results:
        _insert_to_database(plagiarism_results, spider_data["request_data_id"], spider_data["articles"])
        plagiarism_data["number_of_plagiarism"] = len(plagiarism_results)
    return plagiarism_data


def _get_params(articles: dict) -> (zip, list):
    article_data = {"id": [], "text": []}
    for article in articles:
        article_data["id"].append(article["id"])
        article_data["text"].append(article["text"])
    vectors = _vectorize(article_data["text"])
    s_vectors = zip(article_data["id"], vectors)
    new_vectors = list(zip(article_data["id"], vectors))
    return s_vectors, new_vectors


def _check_plagiarism(s_vectors: zip, new_vectors: list) -> set:
    plagiarism_data = set()
    for index, value_x in enumerate(s_vectors):
        id_x, text_vector_x = value_x[0], value_x[1]
        del new_vectors[0]
        for id_y, text_vector_y in new_vectors:
            sim_score, student_pair = _similarity(text_vector_x, text_vector_y)[0][1], sorted((id_x, id_y))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_data.add(score)
    return plagiarism_data


def _vectorize(articles_text: list) -> ndarray:
    return TfidfVectorizer().fit_transform(articles_text).toarray()


def _similarity(text_1: ndarray, text_2: ndarray) -> float64:
    return cosine_similarity([text_1, text_2])


def _sort_plagiarism(plagiat_datas: set) -> list:
    plagiarism_results = [item for item in plagiat_datas if item[2] >= 0.5]
    return plagiarism_results


def _insert_to_database(plagiarism_results: list, request_data_id: int, articles: dict):
    for result in plagiarism_results:
        article_id, compared_article_id, percent_of_plagiat = result[0], result[1], round(result[2] * 100)
        article_name, compared_article_name = articles[article_id]["title"], articles[compared_article_id]["title"]
        article_link, compared_article_link = articles[article_id]["url"], articles[compared_article_id]["url"]
        article_text, compared_article_text = articles[article_id]["text"], articles[compared_article_id]["text"]
        Plagiarism(request_data_id=request_data_id, article_name=article_name,
                   compared_article_name=compared_article_name, article_link=article_link,
                   compared_article_link=compared_article_link, percent_of_plagiat=percent_of_plagiat,
                   article_text=article_text, compared_article_text=compared_article_text).save()
