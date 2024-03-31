from django.urls import path
from . import views

urlpatterns = [
    # Admin Section URLs

    # Admin Home Page
    path('airwelladmin', views.admin_home, name='admin_home'),

    # Admin Products Management
    path('admin_products', views.admin_products, name='admin_products'),

    # Admin Banner Management
    path('admin_poster', views.admin_poster, name='admin_poster'),

    # Add New Banner
    path('admin_add_poster', views.admin_add_poster, name='admin_add_poster'),

    # Delete Banner by ID
    path('delete-banner/<int:banner_id>/', views.delete_banner, name='delete_banner'),

    # Admin Category Management
    path("admin_category", views.admin_category, name='admin_category'),

    # Add New Category
    path('admin_add_category', views.admin_add_category, name='admin_add_category'),

    # Remove Category by ID
    path('admin_remove_category/<int:category_id>/', views.admin_remove_category, name='admin_remove_category'),

    # Edit Category by ID
    path('admin_edit_category/<int:category_id>/', views.admin_edit_category, name='admin_edit_category'),

    # Admin Service Video Management
    path('admin_service_video', views.admin_service_video, name='admin_service_video'),

    # Add New Product
    path('admin_add_product', views.add_product, name='admin_add_product'),

    # Delete Product by ID
    path('delete-product/<str:product_id>/', views.delete_product, name='delete_product'),

    # Admin Enquiry Management
    path('admin_enquiry', views.admin_enquiry, name='admin_enquiry'),

    # Delete Enquiry by ID
    path('delete-enquiry/<int:enquiry_id>/', views.delete_enquiry, name='delete_enquiry'),

    # Update Enquiry Status by ID
    path('update-enquiry-status/<int:enquiry_id>/', views.update_enquiry_status, name='update_enquiry_status'),

    # Admin Login
    path('login', views.admin_login),


    # User Section URLs

    # User Home Page
    path('', views.user_home_page, name='user_home'),

    # User Product Page
    path('product', views.user_product, name='user_product'),

    # View Product by ID
    path('product/<str:id>', views.product_view, name='product_view'),

    # User Contact Page
    path('contact', views.user_contact_page, name='contact_user'),

    # User About Page
    path('about', views.user_about_page, name='user_about'),

    # User Contact Form Submission
    path('user_contact', views.user_contact, name='user_contact'),
]
