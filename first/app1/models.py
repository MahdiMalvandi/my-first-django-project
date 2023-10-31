from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count
from django_resized import ResizedImageField
import os
import shutil
from django.template.defaultfilters import slugify
from django.dispatch import receiver


# Create your models here.


# publish manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


# post model
class Post(models.Model):
    """ post model for posts in my website """

    class Status(models.TextChoices):
        DRAFT = 'DR', 'draft'
        PUBLISH = 'PB', 'publish'
        REJECT = 'RJ', 'reject'

    CATEGORY_CHOICE = (
        ('python','python'),
        ('go lang', 'go lang'),
        ('java', 'java'),
        ('other','other'),
        ('ai', 'ai '),
    )

    # auther
    users = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_post', )

    reading_time = models.PositiveIntegerField(verbose_name="reading time")
    # data fields
    title = models.CharField(max_length=150)
    text = models.TextField()
    slug = models.SlugField(max_length=200)

    # date
    publish = models.DateTimeField(
        default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # choice fields
    status = models.CharField(
        max_length=3, choices=Status.choices, default=Status.DRAFT)
    categories = models.CharField(choices=CATEGORY_CHOICE, default='other', max_length=100)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        """ ORDERING """
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        """ str for class """
        return self.title

    def get_absolute_url(self):
        return reverse('app1:blog_detail_page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', "-")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            storage, path = image.imgfile.storage, image.imgfile.path
            storage.delete(path)
        super().delete(*args, **kwargs)




class Ticket(models.Model):
    """model for ticket """

    # db columns
    message = models.TextField()
    name = models.CharField( max_length=250)
    email = models.EmailField( max_length=254)
    phone = models.CharField( max_length=50)
    title = models.CharField( max_length=50)

    # str for model
    def __str__(self):
        """ str for class """
        return self.title

    # meta class
    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"


class Comment(models.Model):
    # db columns
    name = models.CharField(max_length=500)
    body = models.TextField(verbose_name="پیام")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    postFor = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        """ str for class """
        return self.name

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def get_absolute_url(self):
        return reverse('app1:post_comment', args=[Post.slug])


class PostsImage(models.Model):
    postFor = models.ForeignKey(Post, related_name="images",  on_delete=models.CASCADE)
    title = models.CharField(max_length=150,  null=True, blank=True)
    discription = models.TextField( null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    imgfile = ResizedImageField(upload_to="articles_img/")

    class Meta:
        verbose_name = "عکس پست"
        verbose_name_plural = "عکس پست ها"

    def __str__(self):
        return self.title if self.title else self.imgfile.name

    def delete(self, *args, **kwargs):
        storage, path = self.imgfile.storage, self.imgfile.path
        storage.delete(path)
        super().delete(*args, **kwargs)


class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True, )
    bio = models.TextField(null=True, blank=True)
    photo = ResizedImageField(upload_to='account-image/', size=[500, 500], crop=["middle", "center"], quality=60,
                              null=True, blank=True)
    job = models.CharField(null=True, blank=True,  max_length=250)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"






