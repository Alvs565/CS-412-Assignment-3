from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # for authentication


# Create your models here.
class Profile(models.Model):
    '''Encapsulates the data of a mini_insta profile'''

    #Define the fields under profile:
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Returns a string representation of the a certain row/model instance'''
        return f'{self.username} A.K.A {self.display_name}'

    def get_all_posts(self):
        '''Returns all posts for a given profile'''
        posts = Post.objects.filter(profile=self)
        return posts

    def get_absolute_url(self):
        '''Returns the URL corresponding to the Profile's PK'''
        return reverse('profile', kwargs={'pk': self.pk})

    def get_followers(self):
        '''Returns the list of followers who follow this profile'''
        follows = Follow.objects.filter(profile=self)
        followers = [f.follower_profile for f in follows]
        return followers

    def get_num_followers(self):
        '''Returns the amount of followers who follow this profile'''
        return len(self.get_followers())

    def get_following(self):
        '''Returns a list of profiles followed by this user'''
        followed = Follow.objects.filter(follower_profile=self)
        followers = [f.profile for f in followed]
        return followers

    def get_num_following(self):
        '''Returns the amount of people this user follows'''
        return len(self.get_following())

    def get_post_feed(self):
        '''Returns a feed of a profiles posts ordered by time'''
        following = self.get_following()
        posts = Post.objects.filter(profile__in=following).order_by('-timestamp')
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

    def get_all_comments(self):
        '''Returns all comments on a post'''
        comments = Comment.objects.filter(post=self)
        return comments

    def get_likes(self):
        '''Returns all likes on this post'''
        likes = Like.objects.filter(post=self)
        return likes

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

class Follow(models.Model):
    '''Encapsulates an directed edge between two profiles (where one follows the other)'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile") #BEING FOLLOWED
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile") #FOLLOWER
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of a follow-follower relationship instance'''
        return f'{self.profile.display_name} is followed by {self.follower_profile.display_name}'

class Comment(models.Model):
    '''Encapsulates the idea of one profile leaving a comment on a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''Returns a string representation of a comment'''
        return f'By {self.profile}: {self.text}'

class Like(models.Model):
    '''Encapsulates the idea of a profile liking a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
            '''Returns a string representation of a like'''
            return f'{self.profile} liked {self.post}'
    



