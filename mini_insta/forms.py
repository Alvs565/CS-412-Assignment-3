from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database'''

    class Meta:
        '''Associate this form to the Post model'''
        model = Post
        fields = ['caption']