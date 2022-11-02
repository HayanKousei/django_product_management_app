from cgitb import html
from email import message
from turtle import title
from django.shortcuts import render
from flask import request
import markdown
from . import util
import random

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    html_content = convert_md_to_html(title) #html_content is the converted content from md
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", { #this returns the content of the file
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST": #POST is the method in which data is recievd, like you entering something into google search. That is data you are sending to recieve

        entry_search = request.POST["q"] #Q is where the data is stored, and entry_search is where the data is now stored

        html_content = convert_md_to_html(entry_search) #if the entry_search data is also converted into html then
        if html_content is not None: 
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            }) #return the entry page because it is not None. So if it exists and can be found then it will be converted and presented. 
        else:
            allEntries = util.list_entries() #this is a varible for all the entries that exist, called Allentries
            recommendation = []
            for entry in allEntries: #this is pretty self explainatory. Just read it.

                if entry_search.lower() in entry.lower(): #This converts the Q data in lowercase(entry_search), and sees if its IN entry, which is also in lowercase. Making sure at least one letter is in an entry, then recommending you those entries with that letter.
                    
                    recommendation.append(entry) #This appends, or adds the entry in the recommendation list that has at least one letters or two from the data(Q) you sent. 
            
            return render(request, "encyclopedia/search.html", { #if so then return the search.html page
                "recommendation": recommendation #name another varible called recommendation, not function, to send from views.py which will be search.html. the recommendation variable will show you the entrys related to your search
            })
        
def new_page(request):
    if request.method == "GET": #GET meaning if we just wanna get/see the page.
        return render(request, "encyclopedia/new.html") #then return the page.
    else:
        title = request.POST['title'] #get variable title from our form in new.html, input name is "title"
        content = request.POST['content'] #gets the content from the input
        titleExist = util.get_entry(title) #create a varible to check is there already is a title
        if titleExist is not None: # so if it's NOT not existing (none) then return error
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists" #because it is existing since its not NONE
            })
        else:
            util.save_entry(title, content) #here we use the funtion given to us in util.py
            html_content = convert_md_to_html(title) #converts the content
            return render(request, "encyclopedia/entry.html" ,{
                "title": title,
                "content": html_content
            })

def edit(request): #make sure to make a path for new edit function
    if request.method == 'POST':
        title = request.POST['entry_title'] #grab the entry title
        content = util.get_entry(title) #and the content of the existing entry
        return render(request, "encyclopedia/edit.html" ,{
            "title": title,
            "content": content #we pass these paramaters because have to populate edit.html with data
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title'] #get title
        content = request.POST['content'] #get content
        util.save_entry(title, content) #the function we use to save the edited page
        html_content = convert_md_to_html(title) #convert it to html, copied from 2 functios above
        return render(request, "encyclopedia/entry.html" ,{
            "title": title,
            "content": html_content
        })

def rand(request):
    allEntries = util.list_entries() #create var for all entries
    rand_entry = random.choice(allEntries) #using random.choice that we got from google we get a randome choice from the new var rand_entry
    html_content = convert_md_to_html(rand_entry) #we convert that into html
    return render(request, "encyclopedia/entry.html", { #and return it
        "title": rand_entry,
        "content": html_content
    })
