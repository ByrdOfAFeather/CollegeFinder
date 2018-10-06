from django.shortcuts import render


def get_match(request):
	return render(request, template_name="matcher.html")