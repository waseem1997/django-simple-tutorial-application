from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # import user pre-defined form
from . import models


# Create your views here.


# determine if the slug is category or tutorials:

def single_slug(request, single_slug):  # i pass request and single_slug

    '''
     herw in my situation i don't have a
     series slug i just have a tutorial_slug and category_slug
     and my object is to get all my series that linked to the category that i clicked on

     '''

    # create a list of all the categories in my table
    categories = [c.category_slug for c in
                  models.TutorialCategory.objects.all()]  # this will give me a list in all my possible
    # chech if the slug in the categories slug (slug )
    if single_slug in categories:
        # i want to bring the matches tutorial series:
        matching_series = models.TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        # so here i filter the category slug from the tutorial_category --> category slug
        # so i bring the category slug for this series

        series_urls = {}
        for m in matching_series.all():
            part_one = models.Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest(
                "tutorial_published")
            series_urls[m] = part_one.tutorial_slug  # inject tutorial slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})

    # here if i sent a slug of tutorial
    tutorials = [t.tutorial_slug for t in models.Tutorial.objects.all()]
    # list of all possible tutorials in the table
    if single_slug in tutorials:
        # now we know that it's a tutorial
        # now we'll make a query to brig this specific tutorial
        this_tutorial = models.Tutorial.objects.get(
            tutorial_slug=single_slug)  # get our tutorial based on tutorial slug
        # (get: will bring one object
        # filter will bring a list of objects)

        # now i want to bring all the tutorials that inside my tutorial series:
        series_of_this_tutorial = models.Tutorial.objects.filter(
            tutorial_series__tutorial_series =this_tutorial.tutorial_series).order_by("tutorial_published")

        # also i need the index of specific tutorial:
        # i'll be using this to pop up the specific tutorial in my sidebar
        tutorial_index = list(series_of_this_tutorial).index(this_tutorial)

        # now i want to render the template and pass the context this_tutorial:

        return render(request,
                      "main/tutorial.html",
                      context= {"tutorial": this_tutorial, # current tutorial
                                "tutorials_in_series": series_of_this_tutorial, # send the series tutorials
                                "index_of_the_tutorial": tutorial_index}) # send the current tutorial index


    return HttpResponse(f"{single_slug} does not correspond to anything")


def homepage(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={'categories': models.TutorialCategory.objects.all})


# register view:

def request_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name = form.cleaned_data.get("username")
            messages.success(request, f'Register successful and now you are logging in as{user_name}')
            login(request, user)
            return redirect('/')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = UserCreationForm
    return render(request, template_name='main/register.html',
                  context={'form': form})


# logout view:

def request_logout(request):
    logout(request)
    messages.info(request, f"Logout successfully")
    return redirect("/")


# login view:

def request_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"successfully logged in as {username}")
                return redirect("/")
        else:
            messages.error(request, "username or password or both are invalid FIX THEM")

    form = AuthenticationForm
    return render(request, 'main/login.html', context={'form': form})
