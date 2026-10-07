# blog/forms.py 
# defines the forms that we use for create/update/delete operations

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an article to the database'''

    class Meta:
        '''Associate this form with the Article model from our database'''
        model = Article  #instance of Article
        fields = ['author', 'title', 'text', 'image_file']  #Specify which fields you want to create from the form

class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment about an Article'''

    class Meta:
        '''Associate this form with a model from out database'''
        model = Comment
        fields = ['author', 'text']

