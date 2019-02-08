from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    request.session.set_test_cookie()
    #Queries the database for a list of ALL categories currently stored. Then 
    #order them by the number of likes in descending order, hiding any with 
    #less than 5 likes.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    
    #Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visit'] = request.session['visits']
    
    #Obtain our Response object early so we can add cookie information.
    response = render(request, 'rango/index.html', context_dict)
    
   
    
    #Return response back to the user, updating any cookies that need changed.
    return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    
    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context_dict)

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

@login_required
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

@login_required
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
    
def register(request):
    #Boolean telling the template if the registration was successful.
    registered = False
    
    if request.method == 'POST':
        #Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            #Save the user's form data to the database.
            user = user_form.save()
            
            #Now we hash the password with the set_password method.
            #Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            
            #Now we deal with the UserProfile instance.
            #Since we need to set the user attribute ourselves,
            #we set commit=False.
            profile = profile_form.save(commit=False)
            profile.user = user
            
            #Check if a profile picture was given.
            #Put it in the UserProfile model if there was.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            #Now we save the UserProfile model instance.
            profile.save()
            
            #Update out boolean to show that registration was successful.
            registered = True
        
        else:
            #Invalid form(s), print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        #Not a HTTP POST, so we render our form using two ModelForm instances.
        #These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    #Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method =='POST':
        #Gather the username and password form the login form.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #Use Django to check if the username/password combination 
        #is valid and return a User object if it is.
        
        user = authenticate(username=username, password=password)
        
        if user:
            #Is the account active?
            if user.is_active:
                #If the username/password combo is valid and the acount is
                #active. Then we log the user in and return them to the 
                #homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                #If account is inactive- then they cannot log into it.
                return HttpResponse("Your Rango account is disabled.")
        else:
            #Bad login details were provided. So we can't log the user in.
            #print("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Invalid login details supplied.")
            if username_present(username) == True:
                print("Invalid login details: {0}, {1}".format(username, \
                      password))
                return HttpResponse("Invalid username and password \
                                    combination supplied.")
                
            else:print("Invalid login details: {0}, {1}".format(username, \
                      password))
            return HttpResponse("Unregistered username supplied.")
                
        #The reques isn't a HTTP POST, so display the login form again.
    else:
        #No context variables to pass to the template system,
        #hence the blank dictionary object.
        return render(request, 'rango/login.html', {})
            
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html/', {})

@login_required
def user_logout(request):
    #Since we know the user is logged in we can just log them out and return
    #them to the homepage.
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#Method to determine whether a username is already in use or not.
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    #Get the number of visits to the site.
    #We use the COOKIES.get() function to obtain the visits cookie.
    #If it exists it returns its value as an integer.
    #If it doesn't then it returns the default value of 1.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit', 
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    #If it's been more than a day since the last visit...
    if(datetime.now() - last_visit_time).days > 0:
        visits += 1
        #Update the last visit cookie now that we have updated the count
        request.session['last_visit'] =  str(datetime.now())
    else:
        #Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie 
        
    #Update/set the visits cookie
    request.session['visits'] = visits
 
    

















     
        
        
        
        
        
        
        
        
        
        
    

