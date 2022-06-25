from django.forms import ModelForm
from home.models import RequestData


class RequestDataForms(ModelForm):
    class Meta:
        model = RequestData
        fields = "__all__"
