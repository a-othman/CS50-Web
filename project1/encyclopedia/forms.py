from django import forms
from django.utils.safestring import mark_safe

class NewPage(forms.Form):
    title= forms.CharField(label= 'Article Title')
    content= forms.CharField(widget=forms.Textarea(
            attrs={'name':'body', 'height': '50vh',
             'width': '70%'}))
