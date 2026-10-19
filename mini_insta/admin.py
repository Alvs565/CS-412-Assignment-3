from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)

from .models import Post
admin.site.register(Post)

from .models import Photo
admin.site.register(Photo)

from .models import Follow
admin.site.register(Follow)

from .models import Comment
admin.site.register(Comment)

from .models import Like
admin.site.register(Like)
