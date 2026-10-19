from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database'''

    class Meta:
        '''Associate this form to the Post model'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']