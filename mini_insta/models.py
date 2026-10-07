from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulates the data of a mini_insta profile'''

    #Define the fields under profile:
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Returns a string representation of the a certain row/model instance'''
        return f'{self.username} A.K.A {self.display_name}'

    def get_all_posts(self):
        '''Returns all posts for a given profile'''
        posts = Post.objects.filter(profile=self)
        return posts

class Post(models.Model):
    '''Encapsulates the data for a post on mini_insta'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Returns a string representation of a post instance'''
        return f'{self.caption} by {self.profile} at {self.timestamp}'

    def get_all_photos(self):
        '''Returns all photos for a given post'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Encapsulates the data for a photo within a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_image_url(self):
        '''Returns the URL to this photo's image'''
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ''

    def __str__(self):
        '''Returns a string representation of a Photo instance'''
        if self.image_url:
            return f'{self.image_url}'
        else:
            return f'{self.image_file.name}'