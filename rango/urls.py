# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:39:37 2019

@author: thero
"""
"Created on Mon Jan 21 16:39:37 2019"

"@author: thero"

from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^about/', views.about, name = 'about')
        ]