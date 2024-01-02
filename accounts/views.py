from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from books.models import BorrowedBook

# Create your views here.
class UserRegistrationFormView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name='user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(View):
     def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))

class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        return render(request, self.template_name, {'form': form})
    
class UserProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        user = request.user
        borrowed_books = BorrowedBook.objects.filter(user=user,returned_date=None)
        context = {'user': user, 'borrowed_books': borrowed_books}
        return render(request, self.template_name, context)
    
