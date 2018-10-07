from django.urls import path

from . import views

urlpatterns = [
	path('colleges/<int:identi>', views.match_college, name= "match-college"),
	path('', views.home_page, name="match-home"),
	path('colleges', views.list_results, name="match-list"),
]