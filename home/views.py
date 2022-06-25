from django.shortcuts import render
from django.contrib import messages
from home.forms import RequestDataForms
from home.models import Plagiarism, RequestDateTime, RequestData
from home.handler import site_handler


def home_page(request):
    form = RequestDataForms(request.POST or None)
    context, template = {'form': form}, "home/index.html"
    if request.method == "POST":
        context["form"] = _check_form_validation(form, request)
        plagiarism_results = _plagiarism_process(request)
        if plagiarism_results["error"]:
            _raise_errors(plagiarism_results["error"], request)
        context["plagiarism_results"] = plagiarism_results
    return render(request, template, context)


def _check_form_validation(form, request):
    if form.is_valid():
        messages.success(request, 'Form submission successful')
        form.save()
        _save_request_datetime()
        form = RequestDataForms()
    else:
        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
    return form


def _save_request_datetime():
    request_data_id = RequestData.objects.latest('id').id
    RequestDateTime(request_data_id=request_data_id).save()


def _plagiarism_process(request) -> dict:
    datas = {"topic": request.POST["topic"], "number_of_articles": int(request.POST["number_of_articles"]),
             "site_name": request.POST["site_name"]}
    plagiarism_results, plagiarism_data = {}, site_handler(datas)
    number_of_plagiarism = plagiarism_data.get("number_of_plagiarism", 0)
    plagiarism_results["error"] = plagiarism_data.get("error", "")
    plagiarism_results["results"] = Plagiarism.objects.all().order_by("id")[::-1][:number_of_plagiarism]
    plagiarism_results["records"] = len(plagiarism_results["results"])
    return plagiarism_results


def _raise_errors(error, request):
    messages.error(request, error)
