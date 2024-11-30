from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.db.models import Q

from . import forms, models

from allauth.account.models import EmailAddress
from django.contrib.auth import logout
from django.contrib import messages
from allauth.account.utils import send_email_confirmation

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = forms.MyLoginForm  # Specify your custom form

    def get(self, request, *args, **kwargs):
        print("CustomLoginView GET method called")  # Debugging print
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("CustomLoginView POST method called")  # Debugging print
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Form is valid")  # Debugging print
        user = form.get_user()
        print(f'User: {user}')  # Debugging print

        # Check if the user's email is verified
        email_address = EmailAddress.objects.filter(user=user).first()
        if email_address and not email_address.verified:
            # Resend email verification link
            send_email_confirmation(self.request, user)
            # Log out the user and display a message
            logout(self.request)
            messages.error(
                self.request,
                "Your email is not verified. A new verification link has been sent to your email address."
            )
            return redirect('account_email_verification_sent')  # Adjust this to your verification page URL name

        # Proceed with login if the email is verified
        backend = 'allauth.account.auth_backends.AuthenticationBackend'
        login(self.request, user, backend=backend)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid")  # Debugging print
        print(form.errors)  # Debugging print
        return super().form_invalid(form)

    def get_success_url(self):
        print("Determining success URL")  # Debugging print
        user = self.request.user
        if user.is_authenticated:
            if user.account_type == 2:  # Shop owner
                return reverse_lazy('restaurant_list_2', kwargs={'pk': user.pk})  # Redirect shop owner
            else:
                return reverse_lazy('top_page')  # Redirect normal user
        return super().get_success_url()
    
class UserDetailView(generic.DetailView):
  model = models.CustomUser
  template_name = 'user/user_detail.html'

class UserUpdateView(generic.UpdateView):
    model = models.CustomUser
    template_name = 'user/user_update.html'
    form_class = forms.UserUpdateForm

    def get_success_url(self):
        # Redirect to the login page after updating the user
        user = self.request.user
        if user.is_authenticated and user.account_type == 3:
          return reverse_lazy('user_list_3')  # Adjust this to your login URL name
        else:
          return reverse_lazy('login')  # Adjust this to your login URL name

    def form_valid(self, form):
        # Save the form, including the new password if provided
        user = form.save(commit=False)
        new_password = form.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)  # Set the new password
        user.save()  # Save the user with the updated details
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class SubscribeRegisterView(View):
  template = 'subscribe/subscribe_register.html'
  def get(self, request):
    context = {}
    return render(self.request, self.template, context)
  def post(self, request):
    user_id = request.user.id
    card_name = request.POST.get('card_name')
    card_number = request.POST.get('card_number')
    correct_cord_number = '4242424242424242'
    if card_number != correct_cord_number:
      context = {
        'error_message': 'クレジットカード番号が正しくありません'
        }
      return render(self.request, self.template, context)
    models.CustomUser.objects.filter(id=user_id).update(is_subscribed=True, card_name=card_name, card_number=card_number)
    return redirect(reverse_lazy('top_page'))
  
class SubscribeCancelView(generic.TemplateView):
  template_name = 'subscribe/subscribe_cancel.html'

  def post(self, request):
    user_id = request.user.id
    models.CustomUser.objects.filter(id=user_id).update(is_subscribed=False)
    return redirect(reverse_lazy('top_page'))

class SubscribePaymentView(View):
  template = 'subscribe/subscribe_payment.html'
  def get(self, request):
    user_id = request.user.id
    user = models.CustomUser.objects.get(id=user_id)
    context = {'user': user}
    return render(self.request, self.template, context)
  def post(self, request):
    user_id = request.user.id
    card_name = request.POST.get('card_name')
    card_number = request.POST.get('card_number')
    expiry = request.POST.get('expiry')
    print(card_name, card_number, expiry)
    models.CustomUser.objects.filter(id=user_id).update(card_name=card_name, card_number=card_number, expiry=expiry)
    return redirect(reverse_lazy('top_page'))
  
class UserListView3(generic.ListView):
    template_name = "user/user_list_3.html"
    model = models.CustomUser
    paginate_by = 15

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'id')
        return ordering

    def get_queryset(self):
        # Order the queryset based on the ordering parameter
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve current sorting order and search query in the template
        context['current_ordering'] = self.request.GET.get('ordering', 'id')
        context['search_query'] = self.request.GET.get('q', '')
        return context

    def get(self, request, **kwargs):
        user = request.user
        # Restrict access to users with account_type = 3
        if user.is_authenticated and user.account_type == 3:
            return super().get(request, **kwargs)
        else:
            return redirect(reverse_lazy('top_page'))

class UserDeleteView(generic.DeleteView):
    model = models.CustomUser
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy('user_list_3')