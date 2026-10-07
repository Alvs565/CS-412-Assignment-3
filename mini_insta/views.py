from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
import random

# Create your views here.
class ProfileListView(ListView):
    '''Define a view to show all the profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Define a view to show one instance of profiles'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" #note the singular!

class PostDetailView(DetailView):
    '''Define a view to show one instance of a Post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''Defines a view to handle form submission of a new post'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        '''Returns the dictionary of context variables in use in template'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles form submission and saves the new object to the Django database'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        response = super().form_valid(form)

        files = self.request.FILES.getlist('files')
        for file in files:
            photo = Photo(post=self.object, image_file=file)
            photo.save()

        return response
            
