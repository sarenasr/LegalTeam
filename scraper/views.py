from django.shortcuts import render
from .forms import CaseForm
from .scraping_script import webscrape
# Create your views here.


def case_search(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            case_number = str(form.cleaned_data['case_number'])
            scrape_result = webscrape(case_number)
            return render(request, "result.html", {"scrape_result": scrape_result})
    else:
        form = CaseForm()
    return render(request, "search.html", {"form": form})