from django import forms  
from django.forms import ModelForm 
from .models import Category, Items, ItemRequest


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude =['country', 'code', 'status']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'
        exclude =['country', 'code', 'status' ,'description']



class RequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = '__all__'
        exclude =['country',  'stage', 'requester', ]
