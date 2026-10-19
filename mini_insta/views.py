from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Follow 
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse
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

class ShowFollowersDetailView(DetailView):
    '''Define a view to show a profile's followers'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "followers"

class ShowFollowingDetailView(DetailView):
    '''Define a view to show a the profiles a profile is following'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "following"

class ShowFeedView(DetailView):
    '''Define a view to show a profile's feed'''
    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

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

class UpdateProfileView(UpdateView):
    '''Defines a view to handle the updating of a profile'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):
    '''Defines a view to handle deletion of a post'''

    def get_context_data(self, **kwargs): 
        '''Provides context data needed for the delete form'''
        context = super().get_context_data(**kwargs)
        
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context 

    def get_success_url(self):
        '''returns the URL to redirect to after deleting a post'''
        profile = self.object.profile

        return reverse('profile', kwargs={'pk': profile.pk})
      

    model = Post
    template_name = "mini_insta/delete_post_form.html"
            
