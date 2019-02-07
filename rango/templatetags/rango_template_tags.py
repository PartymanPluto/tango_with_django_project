# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 21:46:11 2019

@author: thero
"""

from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(),
            'act_cat': cat}



