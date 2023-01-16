from django.shortcuts import render
import requests
import re
from .models import Analytics

# Create your views here.
def index(request):
    return render(request, "index.html")


def demand(request):
    data = Analytics.objects.filter(name='web-разработчик')[0]
    return render(request, "demand.html", context={"graph": data.demand_graph.url, "table": str(data.demand_table)})


def geography(request):
    data = Analytics.objects.filter(name='web-разработчик')[0]
    return render(request, "geography.html", context={"graph": data.geography_graph.url, "table": str(data.geography_table)})


def skills(request):
    data = Analytics.objects.filter(name='web-разработчик')[0]
    return render(request, "skills.html", context={"graph": data.skills_graph.url, "table": str(data.skills_table)})


def last_vacancies(request):
    date_from = f"2022-12-24T00:00:00"
    date_to = f"2022-12-24T23:59:00"
    vacancies_list = []
    link = f"https://api.hh.ru/vacancies/?specialization=1&page=1&per_page=10&date_from={date_from}&date_to={date_to}"
    vacancies = requests.get(link).json()["items"]
    for item in vacancies:
        vacancy_dict = {}
        id = item["id"]
        if item["salary"] != None:
            salary_from = 0 if item["salary"]["from"] == None else int(item["salary"]["from"])
            salary_to = 0 if item["salary"]["to"] == None else int(item["salary"]["to"])
            salary = max(salary_to, salary_from) if salary_from == 0 or salary_to == 0 else ( salary_from + salary_to) / 2
            salary_currency = item["salary"]["currency"]
        else:
            salary = 0
        link = f"https://api.hh.ru/vacancies/{id}"
        vacancy_data = requests.get(link).json()
        vacancy_dict["name"] = item["name"]
        vacancy_dict["description"] = re.sub(r'<[^>]*>', '', vacancy_data["description"])
        vacancy_dict["key_skills"] = ", ".join([i["name"] for i in vacancy_data["key_skills"]])
        vacancy_dict["area_name"] = item["area"]["name"]
        vacancy_dict["salary"] = f"{salary} {salary_currency}" if salary != 0 else "null"
        vacancy_dict["published_at"] = item["published_at"]
        vacancy_dict["employer"] = item["employer"]["name"]

        vacancies_list.append(vacancy_dict)

    vacancies_list = sorted(vacancies_list, key=lambda x: x["published_at"])

    return render(request, "last-vacancies.html", context={"vacancies_list": vacancies_list})
