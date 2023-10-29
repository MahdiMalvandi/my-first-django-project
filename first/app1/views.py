from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib.postgres.search import TrigramSimilarity
import random
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def er404(request):
    return render(request, 'app/404.html')


def statistics(request):
    return render(request, 'app/statistics.html')


def home(request):
    """home page"""

    # Get A random Post
    post = Post.published.get(slug=Post.published.all()[random.randint(0, len(Post.published.all()) - 1)].slug)
    blogs = Post.published.all()[:4]

    context = {
        "random_post": post,
        "posts": blogs
    }
    return render(request, "app/home.html", context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(message=cd["message"], name=cd["name"], email=cd["email"],
                                               phone=cd["phone"], title=cd["title"])
            return redirect("app1:home page")
    else:
        form = TicketForm()
    return render(request, "app/contactus.html", {"form": form})


def blog_detail(request, slug):
    try:
        post = Post.published.get(slug=slug)
        comments_count = Post.published.annotate(count_comments=Count("comments"))
        comment = post.comments.filter(active=True)
        content = {
            "posts": post,
            "comments": comment
        }
        return render(request, "app/detail.html", content)
    except:
        return redirect('app1:er404')





@login_required
def post_comment(request, slug):
    if request.method == "POST":
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISH)
        comment = None
        form = CommentsForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Comment.objects.create(name=request.user, body=cd["body"], postFor=post)
            return redirect("app1:blog_detail_page", slug)
        context = {
            "posts": post
        }
    return redirect("app1:blog_detail_page", slug)


@login_required
def add_post(request):
    context = {}
    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.users = request.user
            post.save()
            print(cd['image'])
            # PostsImage.objects.create(imgfile=cd["image"], postFor=post)


            return redirect("app1:profile")
    else:
        form = AddBlogForm()
    context = {
        "forms": form,
    }
    return render(request, "app/addNewBlog.html", context)


def search_post(request):
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
            images_search = PostsImage.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gt=0.1)
            results2 = Post.published.annotate(similarity=TrigramSimilarity('text', query)).filter(similarity__gt=0.1)
            results3 = Post.published.filter(images__in=images_search)

            results = (results1 | results2).order_by("-similarity")

    context = {
        "query": query,
        "posts": results
    }
    return render(request, "app/search.html", context)


@login_required
def profile(request, page=1):
    user = request.user
    posts = Post.published.filter(users=user)
    paginator = Paginator(posts, 2)
    page_number = page
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    content = {
        "user": user,
        "posts": posts
    }
    return render(request, "app/profile.html", content)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('app1:profile')


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            cd = form.cleaned_data
            post = form.save(commit=False)
            post.users = request.user
            post.save()
            PostsImage.objects.create(imgfile=cd["image1"], postFor=post)
            PostsImage.objects.create(imgfile=cd["image2"], postFor=post)
            return redirect("app1:profile")
    else:
        form = AddBlogForm(instance=post)
    content = {
        'form': form,
        'post': post
    }
    return render(request, "app/edit.html", content)


@login_required
def delete_img(request, img_id):
    img = get_object_or_404(PostsImage, id=img_id)
    img.delete()
    return redirect("app1:profile")


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return redirect('app1:home page')
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {'form': form})


@login_required()
def ProfileEdit(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        account_form = EditAccountForm(request.POST, instance=request.user.account, files=request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect("app1:profile")
    else:
        user_form = EditUserForm(instance=request.user)
        account_form = EditAccountForm(instance=request.user.account)
    context = {
        'user_form': user_form,
        'account_form': account_form
    }
    return render(request, 'registration/edit_account_form.html', context)


def post_list(request, category=None, page=1):
    if category is not None:
        posts = Post.published.filter(categories=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 12)
    page_number = page
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
        'category': category,
        'all_categories': Post.CATEGORY_CHOICE
    }
    return render(request, "app/blog.html", context)




@login_required()
def show_user_post_comment(request, slug: str):
    """ Show user post comment

    Parameters
    ---------
    slug : str
        The Slug Of The User Post

    """
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'app/show_post_detail.html', {"post": post})


def user_info(request, username: str, page: int = 1):
    """ Show user information By username

    Parameters
    ---------
    username : str
        The Username of the User
    page : str (optional)
        The Page of User Post
    """

    user = get_object_or_404(User, username=username)
    posts = user.user_post.all()
    paginator = Paginator(posts, 2)
    page_number = page
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'app/user_info.html', {"user": user, "posts": posts})
