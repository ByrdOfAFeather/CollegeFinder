from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import act_sat_conversion
from .forms import MatcherForm
from .models import University
from .statistics.distribution import EstimatedNormal


def get_probability_for_college(college_mean, college_sat_quart_low, college_sat_quard_high, sat = None, act = None):
	if not sat:
		sat = act_sat_conversion[act]
	if not act:
		sat = sat

	normal_estimator = EstimatedNormal(college_mean, college_sat_quart_low, college_sat_quard_high)
	estimation = normal_estimator.cdf(sat)
	return estimation


def match_college(request, identi):
	requested_college = get_object_or_404(University, pk=identi)
	if request.method == "POST":
		form = MatcherForm(request.POST)
		if form.is_valid():
			sat = form.cleaned_data['sat_score']
			act = form.cleaned_data['act_score']
			ecs = form.cleaned_data['extra_circ']
			print(f"This is ecs {ecs}")
			school = requested_college

			school = University.objects.get(name=school)
			print(school.extras.all())
			if not sat: sat = act_sat_conversion[act]

			prob = get_probability_for_college(school.average_sat_score, school.sat_percentile_25,
			                                   school.sat_percentile_75, sat)
			print(f"this is prob before {prob}")

			prob += .1 if True in [e in [d_e.category for d_e in school.extras.all()] for e in ecs] else 0
			print(f"this is prob after {prob}")
			return render(request, "matcher.html", {"college": requested_college, "form": form, "prob": prob})

		else:
			form = MatcherForm()
			return render(request, "matcher.html", {"college": requested_college, "form": form})
	else:
		form = MatcherForm()
		return render(request, "matcher.html", {"college": requested_college, "form": form})


def home_page(request):
	return render(request, "index.html")


def list_results(request):
	queryKeywords = request.GET.get("q", "")
	results = University.objects.filter(name__contains = queryKeywords)
	return render(request, "list.html", {"queryResults": results, "q": queryKeywords})

