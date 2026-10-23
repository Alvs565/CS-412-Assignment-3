from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin # for authentication
from django.contrib.auth.forms import UserCreationForm # for new user
from django.contrib.auth.models import User # the Django User model
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Displays a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):
    '''Displays a random article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #methods:
    def get_object(self):
        '''return one instance of the Article object selected at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

# define a subclass of CreateView to handle creation of Article objects
# (1) display the HTML form to the user (GET)
# (2) process the form submission and store the new Article object (POST)
class CreateArticleView(LoginRequiredMixin, CreateView): # Cannot access this unless we are logged in
    '''A view to handle the creation of a new Article'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        '''return the URL for this app's login page'''
        return reverse('login')
    
    def form_valid(self, form):
        '''Override the default method to add some debug information'''

        # Find the logged in user, and attach that user to the form instance (Article)
        # Find User:
        user = self.request.user
        form.instance.user = user

        # Delegate some work to the superclass to do the rest
        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''A view to handle creation of a new Comment on an Article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new comment'''
        # return reverse("show_all") # This method returns a URL of our choosing (not ideal)
        pk = self.kwargs['pk']
        # call reverse to generate a URL for this article
        return reverse('article', kwargs={'pk':pk})

    def get_context_data(self):
        '''Returns the dictionary of context variables for use in template'''

        # Calling the superclass method
        context = super().get_context_data()

        # Find/Add the article to the context data, retrieve the PK from the URL Pattern
        pk = self.kwargs['pk'] 
        article = Article.objects.get(pk=pk)

        # Add this article into the context dictionary:
        context['article'] = article
        return context

    def form_valid(self, form):
        '''This method handles form submission and saves the new object to the Django database.
        We need to add the foreign key (of the article) to the comment object before saving it to the DB'''
        pk = self.kwargs['pk'] #retrieve the pk from the URL pattern (this method returns keywords within a URL)
        article = Article.objects.get(pk=pk)
        form.instance.article = article # attach this article to the comment instance (sets the FK)

        # Delegate work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateArticleView(UpdateView):
    '''View class to handle update of an article based on its PK'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    '''A view class to handle the deletion of a comment on an article'''
    
    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        '''Return the URL to redirect to after a sucessful delete'''

        # Find the PK for this comment:
        pk = self.kwargs['pk']  #kew word argument from url
        # Find the comment object:
        comment = Comment.objects.get(pk=pk) # Use object manager to retrieve comment object
        # find the PK of the article to which this comment is associated:
        article = comment.article
        #return a URL to redirect to:
        return reverse('article', kwargs={'pk':article.pk}) #URL lookup method, using key word arguments

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The URL to redirect to after sucessful registration'''
        return reverse('login')



    


