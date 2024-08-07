# encyclopedia/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdown_content = util.get_entry(title)
    if markdown_content:
        html_content = markdown2.markdown(markdown_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page was not found."
        })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
    else:
        filtered_entries = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": filtered_entries
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is None:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists."
            })
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': random_entry}))
