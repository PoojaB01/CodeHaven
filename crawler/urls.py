from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    re_path(r'^get_code/$', views.code_searcher, name="code_searcher"),
    re_path(r'^analyse_profile/$', views.rating_analyser, name="rating_analyser"),
    re_path(r'^about_us/$', views.about_us, name="about_us"),
    re_path(r'^compare_contest/$', views.contest_comparator, name="contest_comparator"),
    re_path(r'^contests/$', views.contests, name="contests"),
    re_path(r'^rating_change', views.rating_change, name="rating_change"),
    re_path(r'^ladder', views.ladder, name="ladder"),
]