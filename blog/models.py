from django.db import models
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.text import slugify 
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager


# Our Custom Manager rather than the default manager => [objects]
class PublishedManager(models.Manager):
    # We have overridden this method by written 'Super().get_qyeryset()' to build a custom QuerySet that filters 
    # posts by their status and returns a successive QuerySet that only includes posts with the PUBLISHED status.
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
 
 
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, unique=True, null=False)
    slug = models.SlugField(max_length=250, null=False, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # Another way is to set the default value using current date and time of the database server
    # publish = models.DateTimeField(db_default=Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    

    # Managers
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager
    tags = TaggableManager()  # 3rd party manager
    
        
    class Meta:
        # To specify different default manager
        # default_manager_name = published
        
        # Setting a custom name for the table or it will be appname_modelname(blog_post)
        # db_table = 'posts_table'
        
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def save(self, *args, **kwargs):
        # Ensure slug is based on the title before saving
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
  
        
    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[
                            self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                        ])

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'