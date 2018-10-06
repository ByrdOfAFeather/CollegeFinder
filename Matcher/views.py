from django.shortcuts import render

from .forms import MatcherForm


def get_match(request):
	if request.method == "POST":
		data = MatcherForm(request.POST)
		if data.is_valid():
			gpa = data.cleaned_data['unweighted_gpa']
			sat = data.cleaned_data['sat_score']
			act = data.cleaned_data['act_score']
			print(gpa, sat, act)
			# if not sat and not act:
			# 	raise ValidationError("SAT or ACT must be used")

			return render(request, "results.html", {"data": data})
		else:
			return render(request, "matcher.html", {"data": data})



	else:
		data = MatcherForm()
		return render(request, "matcher.html", {"data": data})
