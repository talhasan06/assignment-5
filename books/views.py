
from django.shortcuts import redirect,get_object_or_404
from .models import Book,BorrowedBook
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Book
from django.views import View
from . import forms
from . import models
from django.views.generic import DetailView
from django.contrib import messages
from django.views import View
from django.utils import timezone

@method_decorator(login_required,name='dispatch')
class DetailBookView(DetailView):
    model=Book
    pk_url_kwarg='id'
    template_name='book_details.html'
    
    def post(self,request,*args,**kwargs):
            review_form = forms.ReviewForm(data=self.request.POST)
            book = self.get_object()
            user = self.request.user
            if not BorrowedBook.objects.filter(user=user, book=book).exists():
                messages.error(request, "You can only review books that you have borrowed.")
                return redirect('book_detail', id=book.id)
    
            if review_form.is_valid():
                new_review = review_form.save(commit = False)
                new_review.book = book
                new_review.user = user
                new_review.save()

                messages.success(request, "Your review has been submitted successfully.")
                return redirect('book_detail', id=book.id)
            return self.get(request,*args,**kwargs)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = forms.ReviewForm()
        
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context
    
@method_decorator(login_required, name='dispatch')
class BorrowView(View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['id'])
        user = self.request.user

        if 'return_book' in request.POST:
            borrowed_book = BorrowedBook.objects.get(user=user, book=book, returned_date=None)
            borrowed_book.returned_date = timezone.now()
            borrowed_book.returned_amount = book.borrowing_price
            borrowed_book.save()

            # Add returned amount to user's account balance
            user.account.balance += borrowed_book.returned_amount
            user.account.save()

            messages.success(request, "Book returned successfully. Refund processed.")
            return redirect('book_detail', id=book.id)
        
        if user.account.balance < book.borrowing_price:
            messages.error(request, "Insufficient balance to borrow this book.")
            return redirect('book_detail', id=book.id)

        user.account.balance -= book.borrowing_price
        user.account.save()

        BorrowedBook.objects.create(user=user, book=book)


        messages.success(request, "Book borrowed successfully.")
        return redirect('book_detail', id=book.id)


        