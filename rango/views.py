from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    #Queries the database for a list of ALL categories currently stored. Then 
    #order them by the number of likes in descending order, hiding any with 
    #less than 5 likes.
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {'categories': category_list, 'pages': page_list}
   #Render the response and send it back to the client
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {'boldmessage': "This tutorial has been put together by Daniel McQuaid"}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        #Checks if there's a category slug with the given name and returns an 
        #instance if there is and raises an exception if there isn't one.
        category = Category.objects.get(slug=category_name_slug)
        
        #Retrieve all associated pages.
        pages = Page.objects.filter(category=category)
        
        #Add the pages to the template context.
        context_dict['pages'] = pages
        #We also add the category object from the db to the context.
        context_dict['category'] = category
    except Category.DoesNotExist:
        #We get here if the specified isn't found
        #A default "no category" is displayed.
        context_dict['category'] = None
        context_dict['pages'] = None
        
    #Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

        
        
        
        
        
        
        
        
        
        
        
    

