from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^logout$',views.user_logout,name='logout'),
    url(r'^uploadcsv',views.upload_csv,name='upload_csv'),
    url(r'^generatefromcsv',views.generate_table,name='generate'),
    url(r'^all',views.all_products,name='all_products'),
    url(r'^deploy/spider$',views.deploy_spider,name='deploy_spider'),
    url(r'^csv$',views.some_view,name='csv'),
    url(r'^create$',views.create,name='create'),
]
