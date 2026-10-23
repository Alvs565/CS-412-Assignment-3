from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin # for authentication
from django.contrib.auth.models import User # the Django User model
from django.contrib.auth.forms import UserCreationForm # for a new user

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

class ShowMyProfileView(ProfileDetailView):
    '''Show a logged in user their own profile'''

    def get_object(self):
        '''returns the object, rather than it pk'''
        return Profile.objects.get(user=self.request.user)

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

class ShowFeedView(LoginRequiredMixin, DetailView):
    '''Define a view to show a profile's feed'''
    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''returns the object, rather than it pk'''
        return Profile.objects.get(user=self.request.user)

class CreatePostView(LoginRequiredMixin, CreateView):
    '''Defines a view to handle form submission of a new post'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        '''Returns the dictionary of context variables in use in template'''
        context = super().get_context_data()
        profile = Profile.objects.get(user=self.request.user)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles form submission and saves the new object to the Django database'''
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile

        response = super().form_valid(form)

        files = self.request.FILES.getlist('files')
        for file in files:
            photo = Photo(post=self.object, image_file=file)
            photo.save()

        return response

class CreateProfileView(CreateView):
    '''A view to handle the creation of a profile'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''returns the dictionary of context variables in use in template'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()

        return context

    def form_valid(self, form):
        '''This method handles form submission and saves the new object to the Django database'''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user

        return super().form_valid(form)
        

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Defines a view to handle the updating of a profile'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_login_url(self):
            '''return the URL for this app's login page'''
            return reverse('login')

    def get_object(self):
        '''returns the object, rather than it pk'''
        return Profile.objects.get(user=self.request.user)

class DeletePostView(LoginRequiredMixin, DeleteView):
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

    def get_login_url(self):
        '''return the URL for this app's login page'''
        return reverse('login')
    
    template_name = "mini_insta/delete_post_form.html"
    model = Post

class SearchView(LoginRequiredMixin, ListView):
    '''A view that allows you to search for profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    model = Post

    def dispatch(self, request, *args, **kwargs):
        '''Handles requests from search.html'''
        if 'query' in self.request.GET:
            return super().dispatch(request, *args, **kwargs)
        else:
            profile = Profile.objects.get(user=self.request.user)
            return render(request, 'mini_insta/search.html')

    def get_queryset(self):
        '''Controls which objects are returned by a search request'''
        query = self.request.GET.get('query')
        return Post.objects.filter(caption__contains=query)

    def get_context_data(self, **kwargs):
        '''Returns the dictionary of context data that can be acessed from the template'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        context['profile'] = Profile.objects.get(user=self.request.user) # the profile doing the search
        context['query'] = query # the text the user typed
        context['posts'] = self.get_queryset() # matching posts

        context['profiles'] = (  # matching profiles: query found in username, display name, or bio text
            Profile.objects.filter(username__contains=query) |
            Profile.objects.filter(display_name__contains=query) |
            Profile.objects.filter(bio_text__contains=query)
            )

        return context

class FollowView(LoginRequiredMixin, TemplateView):
    '''A view that handles an authenticated user following another profile'''

    def get_login_url(self):
        '''In case the user is logged out, redirect them to login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        '''Handles requests to follow a profile'''
        if not request.user.is_authenticated:
            return redirect(self.get_login_url())

        me = Profile.objects.get(user=request.user)
        other = Profile.objects.get(pk=self.kwargs['pk'])

        if me != other: 
            Follow.objects.get_or_create(profile=other, follower_profile=me)

        return redirect('profile', pk=other.pk)

class DeleteFollowView(FollowView):
    '''Subview that handles an authenticated user unfollowing another profile'''

    def dispatch(self, request, *args, **kwargs):
        '''Handles requests to unfollow profile'''
        if not request.user.is_authenticated:
            return redirect(self.get_login_url())

        me = Profile.objects.get(user=request.user)
        other = Profile.objects.get(pk=self.kwargs['pk'])
        Follow.objects.filter(profile=other, follower_profile=me).delete()
        return redirect('profile', pk=other.pk)

class LikeView(FollowView):
        '''Subview that handles an authenticated user liking another post'''
    
        def dispatch(self, request, *args, **kwargs):
            '''Handles requests to like a post'''
            if not request.user.is_authenticated:
                return redirect(self.get_login_url())
    
            me = Profile.objects.get(user=request.user)
            post = Post.objects.get(pk=self.kwargs['pk'])

            if post.profile != me:
                Like.objects.get_or_create(post=post, profile=me)

            return redirect('post', pk=post.pk)

class DeleteLikeView(FollowView):
        '''Subview that handles an authenticated user unliking a post'''
    
        def dispatch(self, request, *args, **kwargs):
            '''Handles requests to unlike a post'''
            if not request.user.is_authenticated:
                return redirect(self.get_login_url())
    
            me = Profile.objects.get(user=request.user)
            post = Post.objects.get(pk=self.kwargs['pk'])
            Like.objects.filter(post=post, profile=me).delete()

            return redirect('post', pk=post.pk)
    
    


     

       
          


   
            
