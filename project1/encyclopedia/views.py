from numpy import random
from django.shortcuts import render
from django.shortcuts import redirect
import markdown2
from django.http import HttpResponse
from . import util
from .forms import *


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    titles_lower_case= util.list_entries()
    titles_lower_case= [t.lower() for t in titles_lower_case]
    if title.lower() not in titles_lower_case:
        return render(request, "encyclopedia/error.html",
        {'error_message': "This page doesn't exist"})
    else:
        content= markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",
            {"title": title, "entry": content})

def search(request):
    query= request.GET['q']
    titles= util.list_entries()
    for title in titles:
        if query.lower()== title.lower():
            return redirect(f"../wiki/{title}")
    possible_results=[]
    for t in titles:
        if query.lower() in t.lower():
            possible_results.append(t)
    if len(possible_results)==0:
        return render(request, 'encyclopedia/error.html',
        {'error_message': "Couldn't find any matches"})
    return render(request, 'encyclopedia/search.html', 
    {'possible_results': possible_results})

def new_page(request):
    if request.method== 'POST':
        form= NewPage(request.POST)
        if form.is_valid():
            cleaned_data= form.cleaned_data
            if cleaned_data['title'] in util.list_entries():
                return render(request, "encyclopedia/error.html",
                {'error_message': 'An article already exists with the same Title'})
            else:
                title= cleaned_data['title']
                content= cleaned_data['content']
                util.save_entry(title, content)
                content= markdown2.markdown(util.get_entry(title))
                return render(request, 'encyclopedia/entry.html',
                    {'title': title, 'entry': content})
    else:
        form= NewPage()
        return render(request, 'encyclopedia/new_page.html',
                        {'form': form})

def random_page(request):
    random_title= random.choice(util.list_entries())
    return redirect(f"../wiki/{random_title}")

    
def edit_page(request, title):
    if request.method== 'POST':
        edited_content= request.POST['content']
        util.save_entry(title, edited_content)
        return redirect(f"../wiki/{title}")
    else:
        content= util.get_entry(title)
        return render(request, 'encyclopedia/edit_page.html',
                    {'title': title, 'content': content})