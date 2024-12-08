from django.urls import path
from . import views
urlpatterns = [
  path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
  path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
  path("login/", views.CustomLoginView.as_view(), name='login'),
  path("user-list-3/", views.UserListView3.as_view(), name="user_list_3"),
  path("user_delete/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
  # 以下レッスン後に適用20241205
  path('subscribe_register', views.CreateCheckoutSessionView.as_view(), name='subscribe_register'),
  # 支払い処理の成功メッセージ
  path('subscription_success/', views.CheckoutSuccessView.as_view(), name='subscription_success'),
  # 支払い処理のキャンセルメッセージ（解約ではなく、Stripeサイトで契約しない場合の処理）
  path('subscription_cancel/', views.SubscriptionCancelView.as_view(), name='subscription_cancel'),
  # 解約処理
  path("subscribe_cancel/", views.SubscribeCancelView.as_view(), name="subscribe_cancel"),
  # 解約処理がうまくいかなかった場合に通知（知らぬ間の課金継続を阻止）
  path("subscribe_cancel_error/", views.SubscribeCancelErrorView.as_view(), name="subscribe_cancel_error"),
  # カード情報はアプリでは扱わないこととする
  # path("subscribe-payment/", views.SubscribePaymentView.as_view(), name="subscribe_payment"),
]