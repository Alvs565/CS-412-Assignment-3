from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
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
class CreateArticleView(CreateView):
    '''A view to handle the creation of a new Article'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''Override the default method to add some debug information'''

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

    


