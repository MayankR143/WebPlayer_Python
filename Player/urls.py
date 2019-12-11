#urls.py of Player
from django.contrib import admin
from django.urls import path
from django.conf import settings
from Player.views import View
from django.conf.urls.static import static

urlpatterns = [
	path('',View.index),
	path('index.html',View.index),
	path('login.html',View.login),
	path('validate',View.validate),
	path('upload_media',View.upload_media),
	path('media.html',View.media_html),
	path('gallery.html',View.gallery_html),
	path('logout',View.logout),
	path('logout.html',View.logout_html),
	path('f_delete',View.f_delete),
	path('adminlogin.html',View.admin_login),
	path('admin_validate',View.admin_validate),
	path('admin_gallery.html',View.admin_gallery),
	path('admin_delete',View.admin_delete),
	path('register',View.register),
	path('displayusers.html',View.cust_users),
	path('del_user',View.del_user),
	path('play',View.play),
	path('registration.html',View.register_html),
	path('about.html',View.about_html),
	path('contact.html',View.contact_html),
	path('upload.html',View.upload_html),
	path('sort',View.sort),
	path('search',View.search),
	path('sortUser',View.sortUser),
	path('searchUser',View.searchUser),
	path('showUserDetails',View.showUserDetails),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)