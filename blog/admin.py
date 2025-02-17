from django.contrib import admin
from django.utils.text import slugify
from django.contrib import messages
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'updated', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish'] 
    show_facets = admin.ShowFacets.ALWAYS

    # it's also cautious as it ensures that even if the save() method in the model is by passed
    # or not called, the logic for updating the slug based on the title is still applied in the admin.
    def save_model(self, request, obj, form, change):
        # Check if the title is unique
        if Post.objects.filter(title=obj.title).exclude(pk=obj.pk).exists():
            self.message_user(request,
                            "This title already exists. Please choose a different title.", level=messages.ERROR)
        else:
            # Update the slug field based on the updated title
            obj.slug = slugify(obj.title)
            obj.save()
   

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']