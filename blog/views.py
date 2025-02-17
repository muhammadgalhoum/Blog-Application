import smtplib
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseServerError
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .models import Post
from.forms import SharePostForm, CommentForm, SearchForm

# Create your views here.

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        page_posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver the last page of the results
        page_posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        page_posts = paginator.page(1)
    return render(request, 'blog/post/list.html', {'page_posts': page_posts, 'tag': tag})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=slug)
    
    # The following Solution is similar to the previous solution which is more simple
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No post found.')
    
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    # Retrieve objects by shared tags using similar_objects() manager method
    similar_objects = post.tags.similar_objects()
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    return render(request, 'blog/post/detail.html', 
                    {'post': post, 'comments': comments, 'form': form,
                     'similar_posts': similar_posts, 'similar_objects': similar_objects})


@require_POST
def post_comment(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=slug)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})
         
         
def post_share(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=slug)
    sent = False
    if request.method == 'POST':
        form = SharePostForm(request.POST or None)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = f"{cd['name']} recommends you read {post.title}"
                message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
                send_mail(subject, message, from_email=None, recipient_list=[cd['to_email']], fail_silently=False)
                sent = True
            except (smtplib.SMTPException, OSError):
                return HttpResponseServerError('An error occurred while sending the email.')
    else:
        form = SharePostForm()
        
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent':sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        # results = (
        #     Post.published.annotate(
        #         similarity=TrigramSimilarity('title', query),
        #     )
        #     .filter(similarity__gt=0.1)
        #     .order_by('-similarity')
        # )
        results = (
            Post.published.annotate(
                title_similarity=TrigramSimilarity('title', query),
                body_similarity=TrigramSimilarity('body', query),
            )
            .annotate(similarity=F('title_similarity') + F('body_similarity'))
            .filter(similarity__gt=0.1)
            .order_by('-similarity')
        )
        # search_vector = SearchVector('title', weight='A', config='english') + \
        #                 SearchVector('body', weight='B', config='english')
        # search_query = SearchQuery(query, config='english')
        # results = Post.published.annotate(search=search_vector,
        #                                 rank=SearchRank(search_vector, search_query)
        #                                 ).filter(rank__gte=0.3).order_by('-rank')
    
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})