# -*- coding: utf-8 -*-
from django import template

# 自定义split方法过滤器
register = template.Library()

@register.filter(name='split')
def split(value,arg):
    return value.split(arg)