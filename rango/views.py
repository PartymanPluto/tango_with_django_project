from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
    form = CategoryForm()
    
    #A HTTP POST?
    if request.method == "POST":
        form = CategoryForm(request.POST)
        
        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the databace.
            form.save(commit=True)
            #We could give a confirmation message here 
            #but the new category will be on the index page anyway,
            #so we can just send the user there.
            return index(request)
        else:
            #If the form contained errors then just print them to the terminal.
            print(form.errors)
            
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
            
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
    
      
        
        
        
        
        
        
        
        
        
        
    

