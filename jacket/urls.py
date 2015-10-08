"""jacket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
	url(r'^$', 'hw.views.index', name='root'),

    # 作业
    url(r'^homework/(?P<myMajor_id>\d+)/$', 'hw.views.hw_all_now', name='now_hws'),
    url(r'^homework/pass/(?P<myMajor_id>\d+)/$', 'hw.views.hw_all_pass', name='pass_hws'),
    url(r'^homework/detail/(?P<pk>\d+)/$', 'hw.views.hw_detail', name='hw_detail'),
    url(r'^homework/aboutMe', 'hw.views.aboutMe', name='aboutMe'),

    # 课程
    url(r'^course/(?P<myMajor_id>\d+)/$', 'hw.views.course_all', name='course_all'),
    url(r'^course/detail/(?P<pk>\d+)/$', 'hw.views.course_detail', name='course_detail'),

    # 专业
    url(r'^major/(?P<mySchool_id>\d+)/$', 'hw.views.major_all', name='major_all'),
    url(r'^major/detail/(?P<pk>\d+)/$', 'hw.views.major_detail', name='major_detail'),

    # 学院
    url(r'^school/(?P<myCollege_id>\d+)/$', 'hw.views.school_all', name='school_all'),
    url(r'^school/detail/(?P<pk>\d+)/$', 'hw.views.school_detail', name='school_detail'),

    # 大学
    url(r'^colleges/$', 'hw.views.college_all', name='college_all'),
    url(r'^college/detail/(?P<pk>\d+)/$', 'hw.views.college_detail', name='college_detail'),

    url(r'^add_hw_zan/$', 'hw.views.add_hw_zan', name='add_hw_zan'),
    url(r'^add_ok_num/$', 'hw.views.add_ok_num', name='add_ok_num'),
    #url(r'^homework/iFinished/$', 'hw.views.addOKNum', name='addOKNum'),


    url(r'^giveSuggestion/$', 'hw.views.giveSuggestion', name='giveSuggestion'),

	url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }), 
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += staticfiles_urlpatterns()
