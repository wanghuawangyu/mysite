# -*- coding: utf-8 -*-
from django import template
from database.models import Article,Category

register = template.Library()

@register.simple_tag
def get_popular_articles(num=10):
    return Article.objects.all().order_by('-comment_num')[:num]

@register.simple_tag
def get_categories(num=5):
    return Category.objects.all()[:num]


@register.simple_tag
def get_new_articles(num=10):
    return Article.objects.all()[:num]

