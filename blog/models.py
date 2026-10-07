from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''Encapsulates the data of a blog Article by an author'''

    #define the data attributes (fields) of the Article object:
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True) URL as a string
    image_file = models.ImageField(blank=True) # an actual image (we replaced image_url)

    def __str__(self):
        '''Return a String Representation of this model instance (row)'''
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('article', kwargs={'pk':self.pk}) # Notice it generates a URL

    def get_all_comments(self):
        '''Return a QuerySet of Comments on thiS Article'''
        comments = Comment.objects.filter(article=self) #Looks for comments whose foreign key is the article instance
        return comments

class Comment(models.Model):
    '''Encapsulates the idea of a comment about an Article'''

    # Data attributes for a comment:
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment'''
        return f'{self.text}'

 

    

