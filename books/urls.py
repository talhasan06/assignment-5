from django.urls import path,include
from .views import DetailBookView,BorrowView
from django.conf import settings
from django.conf.urls.static import static
from core.views import home
urlpatterns = [
    path('details/<int:id>/',DetailBookView.as_view(),name="book_detail"),
    path('purchase/<int:id>/',BorrowView.as_view(), name='borrow_book')
]
