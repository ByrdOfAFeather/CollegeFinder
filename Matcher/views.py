from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import act_sat_conversion
from .models import University
from .statistics.distribution import EstimatedNormal


def get_probability_for_college(college_mean, college_sat_quart_low, college_sat_quard_high, sat = None, act = None):
	if not sat:
		sat = act_sat_conversion[act]
	if not act:
		sat = sat

	normal_estimator = EstimatedNormal(college_mean, college_sat_quart_low, college_sat_quard_high)
	normal_estimator.calculate_z_score(sat)
	return sat


def match_college(request, id):
	requested_college = get_object_or_404(University, pk = id)
	return render(request, "matcher.html", {"college": requested_college})


def home_page(request):
	return render(request, "index.html")


def list_results(request):
	queryKeywords = request.GET.get("q", "")
	results = University.objects.filter(name__contains = queryKeywords)
	return render(request, "list.html", {"queryResults": results, "q": queryKeywords})

