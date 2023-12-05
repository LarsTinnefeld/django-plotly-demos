from django.shortcuts import render
from core.models import PersonSalary
import plotly.express as px

# Create your views here.


def plot(request):
    # person_salary = PersonSalary.objects.all()
    person_salary = PersonSalary.objects.filter(
        education__in=['1. < HS Grad', '5. Advanced Degree'])
    ages = person_salary.values_list('age', flat=True)
    salaries = person_salary.values_list('salary', flat=True)
    color = person_salary.values_list('education', flat=True)

    fig = px.scatter(
        x=ages,
        y=salaries,
        title='Salary by age',
        height=500,
        color=color,
        trendline='ols'
    )
    html = fig.to_html()

    fig_box = px.box(
        x=ages,
        y=salaries,
        title='Salary by age',
        height=500,
    )
    html_box = fig_box.to_html()

    context = {
        'chart': html,
        'box': html_box,
    }
    return render(request, 'scatter.html', context)


def boxplot(request):
    person_salary = PersonSalary.objects.all()
    ages = person_salary.values_list('age', flat=True)
    salaries = person_salary.values_list('salary', flat=True)
    color = person_salary.values_list('education', flat=True)

    fig = px.box(
        x=ages,
        y=salaries,
        title='Salary by age',
        height=1000,
    )
    html = fig.to_html()

    context = {
        'chart': html,
    }
    return render(request, 'scatter.html', context)
