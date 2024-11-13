from django.shortcuts import render

# Create your views here.
# scraper/views.py
from django.shortcuts import render
from .forms import CaseForm
from .scraping_script import webscrape

def case_search(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            case_number = form.cleaned_data['case_number']
            scrape_result = webscrape(case_number)
            return render(request, "scraper/result.html", {"scrape_result": scrape_result})
    else:
        form = CaseForm()
    return render(request, "scraper/search.html", {"form": form})
