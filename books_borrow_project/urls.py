
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home
urlpatterns = [
    path('',home,name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('books/', include('books.urls')),
    path('books/<slug:category_slug>/',home,name="category_wise_post"),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)