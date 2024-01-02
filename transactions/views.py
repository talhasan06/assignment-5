
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import CreateView
from transactions.constants import DEPOSIT
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from transactions.forms import (
    DepositForm,
)
from transactions.models import Transaction

def send_transaction_email(user,amount,subject,template):
        message = render_to_string(template,{
            'user':user,
            'amount':amount,
        })
        send_email=EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,"text/html")
        send_email.send()


class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account,
        })
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context
    
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
 
    def get_initial(self):
        initial = {'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f"{amount}$ was deposited to your account successfully")

        send_transaction_email(self.request.user,amount,"Deposite Message","deposite_email.html")

        return super().form_valid(form)

    