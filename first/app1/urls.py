from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "app1"

urlpatterns = [
    # pages
    path("", views.home, name="home page"),
    path("blog/", views.post_list, name="blogs"),
    path("blog/<str:category>", views.post_list, name="blogs by category"),
    path("blog/<str:slug>/detail/", views.blog_detail, name="blog_detail_page"),
    path("blog/page/<str:page>", views.post_list, name="blog_detail_page_pagination"),
    path("blog/<str:category>/page/<str:page>", views.post_list, name="blog_detail_page_pagination_by_category"),
    path("contactUs/", views.ticket, name="contact_us"),
    path("profile/", views.profile, name='profile'),
    path("profile/posts/comments/<str:slug>/", views.show_user_post_comment, name="show-posts-comments"),
    path("profile/posts/page/<str:page>", views.profile, name='profile-posts-by-page'),
    path("statistics/", views.statistics, name="statistics"),
    path('404/', views.er404, name='er404'),


    path('user/<str:username>/', views.user_info, name='user-info'),
    path('user/<str:username>/posts/page/<str:page>/', views.user_info, name="user-profile-posts-by-page"),

    # do anything
    path("blog/add/new/", views.add_post, name="add_new_post"),
    path("blog/<str:slug>/comment/", views.post_comment, name="post_comment"),
    path("blog/search/", views.search_post, name="search"),
    path('blog/edit_post/<str:slug>', views.edit_post, name="edit-post"),
    path('blog/delete-img/<int:img_id>', views.delete_img, name="delete-img"),
    path('blog/delete_post/<str:slug>', views.delete_post, name="delete-post"),

    # login or log out
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),

    # password change
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url="done"), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    # reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url="done"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url="/app/password-reset/complete"),
         name="password-reset-confirmed"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password-complete"),

    # register
    path('register/', views.register, name="register"),

    # profile edit
    path('profile/edit/', views.ProfileEdit, name="profile-edit")
]
