from django.urls import path

from . import views

urlpatterns = [
    path("", views.TopPageView.as_view(), name="top_page"),
    path("company/", views.CompanyView.as_view(), name="company_page"),
    path("terms/", views.TermsView.as_view(), name="terms_page"),
    path(
        "restaurant-detail/<int:pk>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
    path(
        "restaurant-list/", views.RestaurantListView.as_view(), name="restaurant_list"
    ),
    path("favorite-list/", views.FavoriteListView.as_view(), name="favorite_list"),
    path("favorite-delete/", views.favorite_delete, name="favorite_delete"),
    path(
        "reservation-create/<int:pk>/",
        views.ReservationCreateView.as_view(),
        name="reservation_create",
    ),
    path(
        "reservation-list/",
        views.ReservationListView.as_view(),
        name="reservation_list",
    ),
    path("reservation-delete", views.reservation_delete, name="reservation_delete"),
    path("review-list/<int:pk>/", views.ReviewListView.as_view(), name="review_list"),
    path(
        "review-create/<int:pk>/",
        views.ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "review-update/<int:pk>/",
        views.ReviewUpdateView.as_view(),
        name="review_update",
    ),
    path("review-delete", views.review_delete, name="review_delete"),
    path(
        "restaurant-list-2/<int:pk>/",
        views.RestaurantListView2.as_view(),
        name="restaurant_list_2",
    ),
    path(
        "restaurant-create/",
        views.RestaurantCreateView.as_view(),
        name="restaurant_create",
    ),
    path(
        "restaurant-update/<int:pk>/",
        views.RestaurantUpdateView.as_view(),
        name="restaurant_update",
    ),
    path(
        "restaurant/<int:restaurant_id>/dining-tables/",
        views.DiningTableListView.as_view(),
        name="dining_table_list",
    ),
    path(
        "restaurant/<int:restaurant_id>/dining-tables/update/<int:pk>/",
        views.DiningTableUpdateView.as_view(),
        name="dining_table_update",
    ),
    path(
        "restaurant/<int:restaurant_id>/dining-tables/<int:pk>/delete/",
        views.dining_table_delete,
        name="dining_table_delete",
    ),
    path(
        "restaurant/<int:restaurant_id>/dining-tables/create/",
        views.DiningTableCreateView.as_view(),
        name="dining_table_create",
    ),
    path(
        "restaurant/<int:restaurant_id>/menu/",
        views.MenuListView.as_view(),
        name="menu_list",
    ),
    path(
        "restaurant/<int:restaurant_id>/menu/update/<int:pk>/",
        views.MenuUpdateView.as_view(),
        name="menu_update",
    ),
    path(
        "restaurant/<int:restaurant_id>/menu/create/",
        views.MenuCreateView.as_view(),
        name="menu_create",
    ),
    path(
        "restaurant/<int:restaurant_id>/menu/delete/<int:pk>/",
        views.MenuDeleteView.as_view(),
        name="menu_delete",
    ),
    path(
        "restaurant/<int:pk>/review-list-2/",
        views.ReviewListView2.as_view(),
        name="review_list_2",
    ),
    path(
        "restaurant/<int:restaurant_id>/review-update-2/<int:pk>/edit/",
        views.ReviewUpdateView2.as_view(),
        name="review_update2",
    ),
    path(
        "reviews/<int:pk>/toggle-display/",
        views.toggle_display_masked,
        name="toggle_display_masked",
    ),
    path(
        "restaurant/<int:restaurant_id>/reservations",
        views.ReservationListView2.as_view(),
        name="reservation_list2",
    ),
    path(
        "restaurant/<int:restaurant_id>/reservations/reservation-management",
        views.ReservationManagementView.as_view(),
        name="reservation_management",
    ),
    path(
        "restaurant/<int:restaurant_id>/reservations/reservation-slots/",
        views.ReservationSlotCreateView.as_view(),
        name="reservation_slot_create",
    ),
    path(
        "restaurant-list-3/",
        views.RestaurantListView3.as_view(),
        name="restaurant_list_3",
    ),
    path(
        "restaurant-update3/<int:pk>/",
        views.RestaurantUpdateView3.as_view(),
        name="restaurant_update3",
    ),
    path(
        "restaurant-delete3/<int:pk>/",
        views.RestaurantDeleteView3.as_view(),
        name="restaurant_delete3",
    ),
    path(
        "restaurant/review-list-3/",
        views.ReviewListView3.as_view(),
        name="review_list_3",
    ),
    path(
        "category/category-list-3/",
        views.CategoryListView3.as_view(),
        name="category_list_3",
    ),
    path(
        "category/category-update-3/<int:pk>/",
        views.CategoryUpdateView3.as_view(),
        name="category_update3",
    ),
    path(
        "category/category-create-3/",
        views.CategoryCreateView3.as_view(),
        name="category_create_3",
    ),
    path(
        "category/category-delete3/<int:pk>/",
        views.CategoryDeleteView3.as_view(),
        name="category_delete3",
    ),
    path("readme/", views.readme_view, name="readme"),
    # path('test-flatpickr/', views.test_flatpickr, name='test_flatpickr'),
    # path('restaurant/<int:restaurant_id>/reservations/reservation-slots-test/', views.ReservationSlotCreateTestView.as_view(), name='reservation_slot_create_test'),
]
