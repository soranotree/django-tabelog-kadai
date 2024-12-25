import stripe
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic

from . import forms, models


class CustomLoginView(LoginView):
    template_name = "account/login.html"
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
        print(f"User: {user}")  # Debugging print

        # Check if the user's email is verified
        email_address = EmailAddress.objects.filter(user=user).first()
        if email_address and not email_address.verified:
            # Resend email verification link
            send_email_confirmation(self.request, user)
            # Log out the user and display a message
            logout(self.request)
            messages.error(
                self.request,
                "Your email is not verified. A new verification link has been sent to your email address.",
            )
            return redirect(
                "account_email_verification_sent"
            )  # Adjust this to your verification page URL name

        # Proceed with login if the email is verified
        backend = "allauth.account.auth_backends.AuthenticationBackend"
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
                return reverse_lazy(
                    "restaurant_list_2", kwargs={"pk": user.pk}
                )  # Redirect shop owner
            else:
                return reverse_lazy("top_page")  # Redirect normal user
        return super().get_success_url()


class UserDetailView(generic.DetailView):
    model = models.CustomUser
    template_name = "user/user_detail.html"


class UserUpdateView(generic.UpdateView):
    model = models.CustomUser
    template_name = "user/user_update.html"
    form_class = forms.UserUpdateForm

    def get_success_url(self):
        # Redirect to the login page after updating the user
        user = self.request.user
        if user.is_authenticated and user.account_type == 3:
            return reverse_lazy("user_list_3")  # Adjust this to your login URL name
        else:
            return reverse_lazy("login")  # Adjust this to your login URL name

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


class UserListView3(generic.ListView):
    template_name = "user/user_list_3.html"
    model = models.CustomUser
    paginate_by = 15

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "id")
        return ordering

    def get_queryset(self):
        # Order the queryset based on the ordering parameter
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(user_name__icontains=query) | Q(email__icontains=query)
            )
        return queryset.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve current sorting order and search query in the template
        context["current_ordering"] = self.request.GET.get("ordering", "id")
        context["search_query"] = self.request.GET.get("q", "")
        return context

    def get(self, request, **kwargs):
        user = request.user
        # Restrict access to users with account_type = 3
        if user.is_authenticated and user.account_type == 3:
            return super().get(request, **kwargs)
        else:
            return redirect(reverse_lazy("top_page"))


class UserDeleteView(generic.DeleteView):
    model = models.CustomUser
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("user_list_3")


# Stripe APIキーを設定
stripe.api_key = settings.STRIPE_SECRET_KEY


# Stripeの支払いview
# class CreateCheckoutSessionView(LoginRequiredMixin, View):
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to top page if user is not authenticated
            return redirect("login")

        # Fetch user account type
        account_type = request.user.account_type

        # Determine the price ID based on account type
        if account_type == 1:
            price_id = "price_1QTJEeFFoc76Aq0w4zqfDUjD"
        elif account_type == 2:
            price_id = "price_1QTjgfFFoc76Aq0whQ6F2KID"
        else:
            # Redirect to top page for other cases (e.g., account_type = 3 or any other case)
            return redirect("top_page")

        # Create checkout session with the determined price
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{settings.YOUR_DOMAIN}/accounts/subscription_success/?session_id={{CHECKOUT_SESSION_ID}}&user_id={request.user.id}",
            cancel_url=f"{settings.YOUR_DOMAIN}/accounts/subscription_cancel/",
        )

        # Redirect to Stripe checkout session URL
        return redirect(checkout_session.url, code=303)

    def get(self, request, *args, **kwargs):
        return render(request, "subscribe/subscribe_register.html")


# 支払い成功（会員のみ）
class CheckoutSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        user_id = request.GET.get("user_id")

        if not session_id or not user_id:
            return HttpResponse("Invalid request", status=400)
        # ユーザーの subscription 項目を更新
        user = get_object_or_404(models.CustomUser, id=user_id)
        session = stripe.checkout.Session.retrieve(session_id)
        user.subscription_id = session.subscription  # Save the subscription ID
        user.is_subscribed = True
        user.save()

        return render(request, "subscribe/subscription_success.html")


class SubscribeCancelView(View):
    template_name = "subscribe/subscribe_cancel.html"

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse("login"))  # Redirect to login if not authenticated
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse("login"))  # Redirect to login if not authenticated

        try:
            # Cancel subscription on Stripe
            stripe_subscription_id = user.subscription_id
            stripe.Subscription.delete(stripe_subscription_id)

            # Update user's subscription status
            user.is_subscribed = False
            user.stripe_subscription_id = None
            user.save()

            # Redirect to success page
            return redirect(reverse("top_page"))

        except Exception as e:
            # Handle errors during cancellation
            print(f"Error during subscription cancellation: {e}")
            return redirect(reverse("subscribe_cancel_error"))


# サブスク（解約エラー）
class SubscribeCancelErrorView(generic.TemplateView):
    template_name = "subscribe/subscribe_cancel_error.html"


# サブスク（キャンセル）
class SubscriptionCancelView(generic.TemplateView):
    template_name = "subscribe/subscription_cancel.html"


# セキュリティの観点からアプリでは保存しない。すべてStripeで入力⇒課題必須項目なので復活
class SubscribePaymentView(View):
    template = "subscribe/subscribe_payment.html"

    def get(self, request):
        user_id = request.user.id
        user = models.CustomUser.objects.get(id=user_id)
        context = {"user": user}
        return render(self.request, self.template, context)

    def post(self, request):
        user_id = request.user.id
        card_name = request.POST.get("card_name")
        card_number = request.POST.get("card_number")
        expiry = request.POST.get("expiry")
        print(card_name, card_number, expiry)
        models.CustomUser.objects.filter(id=user_id).update(
            card_name=card_name, card_number=card_number, expiry=expiry
        )
        return redirect(reverse_lazy("top_page"))
