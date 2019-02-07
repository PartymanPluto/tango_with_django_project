# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 14:53:57 2019

@author: thero
"""

from django import forms 
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    #An inline class to provide additional info on the form.
    #Provides an association between the ModelForm and a model.
    class Meta:
        model = Category
        fields = ('name',)
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                            help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    #Method that appends 'http://' to the front of a url if it isn't there.
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            
            return cleaned_data
    
    
    #Basically the same as the Meta class in CategoryForm
    class Meta:
        model = Page
        exclude = ("category",) 
        #Note that fields = ("title", "url", "views") also works as they are
        #the fields we need here.
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    