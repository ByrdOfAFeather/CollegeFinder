from django.shortcuts import render

from . import act_sat_conversion
from .forms import MatcherForm
from .models import University
from .statistics.distribution import EstimatedNormal


def get_probablity_for_college(college_mean, college_sat_quart_low, college_sat_quard_high, sat=None, act=None):
	if not sat:
		sat = act_sat_conversion[act]
	if not act:
		sat = sat

	normal_estimator = EstimatedNormal(college_mean, college_sat_quart_low, college_sat_quard_high)
	estimation = normal_estimator.calculate_z_score(sat)
	estimation = normal_estimator.cdf(estimation)
	return estimation


def get_match(request):
	if request.method == "POST":
		data = MatcherForm(request.POST)
		if data.is_valid():
			gpa = data.cleaned_data['unweighted_gpa']
			sat = data.cleaned_data['sat_score']
			act = data.cleaned_data['act_score']
			school = data.cleaned_data['college']

			school = University.objects.get(name=school)
			if not sat: sat = act_sat_conversion[act]
			print(get_probablity_for_college(school.average_sat_score, school.sat_percentile_25,
			                                 school.sat_percentile_75, sat))

			prob = get_probablity_for_college(school.average_sat_score, school.sat_percentile_25,
			                                  school.sat_percentile_75, sat)

			return render(request, "results.html", {"data": prob})
		else:
			return render(request, "matcher.html", {"data": data})

	else:
		data = MatcherForm()
		return render(request, "matcher.html", {"data": data})
