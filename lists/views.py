from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {
        'list': list_,
        'form': form,
    })


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)  # redirect 함수의 인자로 객체를 넣으면 자동으로 get_absolute_url 함수가 호출된다.
    else:
        return render(request, 'home.html', {'form': form})
