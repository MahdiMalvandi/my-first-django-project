from django.contrib import admin
from .models import *

# Register your models here.

# personalization of admin panel
adminPanel = admin.sites.AdminSite
adminPanel.site_header = "پنل ادمین جنگو"
adminPanel.site_title = "پنل ادمین"
adminPanel.index_title = "پنل ادمین"


# inlines
class ImageInline(admin.TabularInline):
    """Tabular Inline View for Image"""

    model = PostsImage
    extra = 1


class CommentInline(admin.TabularInline):
    """Tabular Inline View for Comment"""

    model = Comment
    extra = 0


# post admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ post admin """

    list_display = ['title', 'users', 'publish', 'status']
    list_filter = ['status', 'users']
    search_fields = ['title', 'text']
    raw_id_fields = ['users']
    prepopulated_fields = {"slug": ["title"]}
    list_editable = ['status']
    list_display_links = ['title', 'users']
    inlines = [
        ImageInline,
        CommentInline
    ]


# ticket admin
@admin.register(Ticket)
class PostAdmin(admin.ModelAdmin):
    """ post admin """

    list_display = ['title', 'message', 'name', 'phone']
    search_fields = ['title', 'text']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """" account admin panel """

    list_display = ["user", "date_of_birth", "bio", "job"]

