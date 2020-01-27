from django import forms

CHOICES= [
    ('upcoming', 'Upcoming'),
    ('ongoing', 'Ongoing'),
    ('finished', 'Finished'),
    ]

class code_search_form(forms.Form):
    user = forms.CharField()
    contest_code = forms.IntegerField()
    question_code = forms.CharField()


class analyse_profile_form(forms.Form):
    user = forms.CharField()

class rating_change_calculator(forms.Form):
    old_rating = forms.IntegerField()
    rank = forms.IntegerField()
    contest_code = forms.IntegerField()


class average_gap_form(forms.Form):
    user = forms.CharField()


class compare_contest_form(forms.Form):
    user_1 = forms.CharField()
    user_2 = forms.CharField()
    contest_code = forms.CharField()

