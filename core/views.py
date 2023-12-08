from django.shortcuts import render
from django.db.models import Case, When, Value, CharField
from core.models import PersonSalary
import plotly.express as px

# Create your views here.


def plot(request):
    person_salaries = PersonSalary.objects.all()
    # person_salaries = PersonSalary.objects.filter(
    #     education__in=['1. < HS Grad', '5. Advanced Degree'])

    ages = person_salaries.values_list('age', flat=True)
    salaries = person_salaries.values_list('salary', flat=True)
    color = person_salaries.values_list('education', flat=True)

    fig = px.scatter(
        x=ages,
        y=salaries,
        title='Salary by age',
        height=500,
        color=color,
        trendline='ols'
    )
    html = fig.to_html()

    # 15-19, 20-24, 25-29, ...
    YEARS_PER_AGG = 5

    age_bins = [(i, i+YEARS_PER_AGG-1,) for i in range(15, 85, YEARS_PER_AGG)]
    conditionals = [
        When(age__range=bin, then=Value(f'{bin}')) for bin in age_bins]

    case = Case(*conditionals, output_field=CharField())

    age_groupings = person_salaries.annotate(
        age_group=case).values('age_group').order_by('age_group')
    # print(age_groupings)

    age_groups = age_groupings.values_list('age_group', flat=True)
    salaries_groups = age_groupings.values_list('salary', flat=True)

    fig_box = px.box(
        x=age_groups,
        y=salaries_groups,
        title='Salary by age',
        height=500,
    )
    html_box = fig_box.to_html()

    context = {
        'chart': html,
        'box': html_box,
    }
    return render(request, 'scatter.html', context)


# def boxplot(request):
#     person_salaries = PersonSalary.objects.all()

    # 15-19, 20-24, 25-29, ...
    # YEARS_PER_AGG = 5

    # age_bins = [(i, i + YEARS_PER_AGG - 1)
    #             for i in range(15, 85, YEARS_PER_AGG)]
    # conditionals = [
    #     When(age_range=bin, then=Value(f'{bin}')) for bin in age_bins]

    # case = Case(*conditionals, output_field=CharField())

    # age_groupings = person_salaries.annotate(age_groupings=case).values

    # ages = person_salaries.values_list('age', flat=True)
    # salaries = person_salaries.values_list('salary', flat=True)
    # color = person_salaries.values_list('education', flat=True)

    # fig = px.box(
    #     x=ages,
    #     y=salaries,
    #     title='Salary by age',
    #     height=1000,
    # )
    # html = fig.to_html()

    # context = {
    #     'chart': html,
    # }
    # return render(request, 'scatter.html', context)
