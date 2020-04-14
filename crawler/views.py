from django.shortcuts import render
from .forms import *
import json
import datetime
from datetime import date
from .crawlers import *


def index(request):
    return render(request, 'crawler/index.html')


def code_searcher(request):
    if request.method == 'POST':
        form = code_search_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            contest_code = form.cleaned_data['contest_code']
            question_code = form.cleaned_data['question_code']
            code_text = crawler_1(str(user), str(contest_code), str(question_code))
            #print(code_text)
            return render(request, 'crawler/code_searcher.html', {'form': form, 'code_text': code_text})
    form = code_search_form()
    return render(request, 'crawler/code_searcher.html', {'form': form})


def rating_analyser(request):
    if request.method == 'POST':
        form = analyse_profile_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            result = crawler_2(user)
            #sub = generate_heat_map(user)
            #pie = generate_pie_chart(user)
            #grid = [[0 for i in range(53)] for j in range(7)]
            #for k, v in sub.items():
            #    if k < 366:
            #        grid[k % 7][k // 7] = v
            return render(request, 'crawler/rating_analyser.html', {'form': form, 'result' : result })
    form = analyse_profile_form()
    return render(request, 'crawler/rating_analyser.html', {'form': form})
"""

def questions_and_attempts(request):
    if request.method == 'POST':
        form = questions_and_attempts_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            attempts = crawler_3(user)
            return render(request, 'crawler/questions_and_attempts.html', {'form': form, 'attempts': attempts})
    form = questions_and_attempts_form()
    return render(request, 'crawler/questions_and_attempts.html', {'form': form})
"""

def contest_comparator(request):
    if request.method == 'POST':
        form = compare_contest_form(request.POST)
        if form.is_valid():
            user_1 = form.cleaned_data['user_1']
            user_2 = form.cleaned_data['user_2']
            contest_code = form.cleaned_data['contest_code']
            problems = crawler_5(user_1, user_2, contest_code)
            return render(request, 'crawler/contest_comparator.html', {'form': form, 'problems': problems})
    form = compare_contest_form()
    return render(request, 'crawler/contest_comparator.html', {'form': form})

"""
def average_gap(request):
    if request.method == 'POST':
        form = average_gap_form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            gap = crawler_4(user)
            sub = generate_heat_map(user)
            pie = generate_pie_chart(user)
            grid = [[0 for i in range(53)] for j in range(7)]
            for k, v in sub.items():
                if k < 366:
                    grid[k % 7][k // 7] = v
            return render(request, 'crawler/average_gap.html', {'form': form, 'gap': gap , 'pie':pie , 'sub' : sub })
    form = average_gap_form()
    return render(request, 'crawler/average_gap.html', {'form': form})
"""

def contests(request):
    u, o, f = crawler_6()
    return render(request, 'crawler/contests.html', { 'upcoming' : u , 'ongoing' : o , 'finished' : f })

def about_us(request):
    return render(request, 'crawler/about_us.html')

def rating_change(request):
    form = rating_change_calculator(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['old_rating']
        contest_code = form.cleaned_data['contest_code']
        rank = form.cleaned_data['rank']
        change = virtual_rating_change(rank,contest_code,rating)
        return render(request, 'crawler/rating_change.html',{'form' : form, 'change' : change})
    form = rating_change_calculator()
    return render(request, 'crawler/rating_change.html',{'form':form})
