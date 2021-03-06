from django.shortcuts import render , redirect ,get_object_or_404, get_list_or_404 
from datetime import datetime
from django.views.generic.edit import CreateView
# Create your views here.
from django.http import HttpResponse
from .models import Stores, Dishes , Review
from .forms import StoresForm, DishesForm ,CustomTime ,UserRegisterForm,ReviewForm
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
import pdb

def info(request):
    stores = Stores.objects.all()
    context={'stores':stores,"form":CustomTime()}
    return render(request,'info/index.html',context)

def add_store(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StoresForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            messages.success(request, f'Store added!')
            return redirect ("info")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StoresForm()

    return render(request, 'info/add_store.html', {'form': form})

def add_dish(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DishesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            messages.success(request, f'Dish added!')
            return redirect ("info")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DishesForm()

    return render(request, 'info/add_dish.html', {'form': form})

def current_store(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    stores=Stores.objects.filter(start_hour__lte=current_time, end_hour__gte=current_time)
    context={'stores':stores,"form":CustomTime()}
    return render(request,'info/current.html',context)

def custom_store(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomTime(request.POST)
    if form.is_valid():
        time=form['time'].value()
        current_time = time
        request.session['current_time'] = current_time
        stores= Stores.objects.filter(start_hour__lte=current_time, end_hour__gte=current_time)
        context={'stores':stores}
        return render(request,'info/custom.html',context)
    else:
        messages.error(request, f'Please enter time in HH:MM:SS format',extra_tags="danger")
        return redirect('info')

def render_items(request, store_name):
    store = Stores.objects.get(name=store_name)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        form.instance.store = store
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, f'Review added!')
            return redirect ("info")
    else:
        form = ReviewForm()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        item = Dishes.objects.filter(start_hour__lte=current_time, end_hour__gte=current_time,store=store)
        review = Review.objects.filter(store=store)
        return render(request, 'info/dish.html', {'item': item ,'store':store,'review':review,'form':form})


def render_items_custom(request, store_name):
    store = Stores.objects.get(name=store_name)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        form.instance.store = store
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, f'Review added!')
            return redirect ("info")
    else:
        form = ReviewForm()
        current_time = request.session['current_time']
        item = Dishes.objects.filter(start_hour__lte=current_time, end_hour__gte=current_time,store=store)
        review = Review.objects.filter(store=store)
        ##item = get_list_or_404(Dishes.objects.filter(start_hour__lte=current_time, end_hour__gte=current_time), store=store)
        return render(request, 'info/dish.html', {'item': item ,'store':store,'review':review,'form':form})

# class IndexView(generic.ListView):
#     template_name = 'info/dish2.html'
#     context_object_name = 'item'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Dishes.objects.order_by('price')[:5]

def register(request):
    if request.method== "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

