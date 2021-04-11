from datetime import date, datetime

from .models import specifications
from django.http import HttpRequest, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.template import loader
from django.shortcuts import render
from .forms import SpecifForm, RegisterForm

def index(request):
    spec = specifications.objects.order_by('-date')
    if request.method == "POST":
        form_filter = SpecifForm(request.POST)
        if form_filter.is_valid():
            spec = filter_spec(spec, form_filter)
    return render(request, 'index.html', {'list': spec})

def filter_spec(spec, form_filter):
    if form_filter.cleaned_data['specification_name']:
        spec = spec.filter(name_specification=form_filter.cleaned_data['specification_name'])

    if form_filter.cleaned_data['renewal_date'] and form_filter.cleaned_data['renewal_date2']:
        if not (form_filter.cleaned_data['renewal_date'] > form_filter.cleaned_data['renewal_date2']):
            spec = spec.filter(date__range=[form_filter.cleaned_data['renewal_date'],
                                            form_filter.cleaned_data['renewal_date2']])
    if form_filter.cleaned_data['author_name']:
        spec = spec.filter(author=form_filter.cleaned_data['author_name'])

    if form_filter.cleaned_data['version_name']:
        spec = spec.filter(version=form_filter.cleaned_data['version_name'])

    if form_filter.cleaned_data['tag_name']:
        spec = filter_by_tags(spec, form_filter.cleaned_data['tag_name'])
    return spec

def filter_by_tags(spec, tags: str):
    tags_split = tags.replace(',', ' ').split()
    for tag in tags_split:
        spec = spec.filter(tags__name=tag)
    return spec

def by_author(request, author_name):
    specif = specifications.objects.filter(author=author_name)
    authors = User.objects.all()
    context = {'bbs': specif, 'author': authors}
    return render(request, 'author.html', context)


def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # после отправки формы
        regform = RegisterForm(request.POST)
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            # переадресация на главную страницу после регистрации

            return HttpResponseRedirect('http://127.0.0.1:8000/')
    else:
        regform = RegisterForm()  # создание объекта формы для ввода данных нового пользователя
        assert isinstance(request, HttpRequest)
    return render(request, 'registration/registration.html',
                  {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        })

def view_specification(request, pk):
    if request.method == "GET":
        specif = specifications.objects.filter(pk=pk).get()
        text = specif.text_specification
        context = {'library': specif, 'text': text}
        return render(request, 'view_specifications.html', context)
