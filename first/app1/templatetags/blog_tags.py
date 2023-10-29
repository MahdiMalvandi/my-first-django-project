from django import template
from ..models import Post, Comment, User
from django.db.models import Sum, Max, Min, Count

register = template.Library()


@register.simple_tag(takes_context=True)
def total_posts(context):
    return Post.published.count()



@register.simple_tag(takes_context=True)
def total_comments(context):
    return Comment.objects.count()


@register.simple_tag(takes_context=True)
def total_users(context):
    return User.objects.count()

  

@register.inclusion_tag("partials/p.html")
def get_template(name, lastname, email, age):
    content = {
        "firstname": name,
        "lastname": lastname,
        "email": email,
        "age": age
    }

    return {"content": content}


@register.simple_tag()
def get_sum_reading_time():
    sum_reading_time = Post.published.aggregate(Sum("reading_time"))
    return sum_reading_time["reading_time__sum"]


@register.filter(name="cencorship")
def cencorship(text):
    bad_words = ["خر","بیشعور","بی پدر مادر","سگ","گاو"]
    for word in bad_words:
        if word in text:
            count_of_star = len(word)
            text = text.replace(word, "*"*count_of_star)
    return text

@register.simple_tag()
def get_max_post():
    max_reading_time = Post.published.aggregate(Max("reading_time"))
    return Post.published.filter(reading_time=max_reading_time["reading_time__max"])

@register.simple_tag()
def get_min_post():
    max_reading_time = Post.published.aggregate(Min("reading_time"))
    return Post.published.filter(reading_time=max_reading_time["reading_time__min"])



@register.simple_tag()
def get_active_user():
    active_users = User.objects.annotate(posts=Count("user_post")).order_by("-posts")
    return active_users[:4]