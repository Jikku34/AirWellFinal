from django.db.models import Q, Count
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import *
import re


# Create your views here.

# ++++++++++++++++++++++++++++++++ Admin Section ++++++++++++++++++++++++++++++++++++++++++++++++
def admin_login(request):
    """
    View for admin login.
    This view handles the authentication of admin users.
    If the request method is POST, it attempts to authenticate the user
    using the provided username and password.
    If authentication is successful, the user is logged in and redirected to the homepage.
    If authentication fails, an appropriate message is printed.
    """

    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/airwelladmin')
        else:
            return HttpResponse('Incorrect username or password')

    return render(request, 'admin/admin_login.html')


@login_required(login_url='/login')
def admin_logout(request):
    """
    View for admin logout.
    This view logs out the currently authenticated admin user.
    After logging out, it redirects the user to a specified URL, such as the login page.
    """
    try:
        logout(request)
        return redirect('/login')
    except:

        return redirect('/login')




@login_required(login_url='/login')
def admin_home(request):
    """
    Admin dashboard view.
    This view displays various statistics about user enquiries on the admin dashboard.
    """
    admin_home_data = {
        'enquiry_count': UserEnquiryModel.objects.filter(enquiry_status="pending").count(),
        'total_enquiry_count': UserEnquiryModel.objects.all().count(),
        'enquiry_year_count': UserEnquiryModel.objects.filter(enquiry_create_at__year=timezone.now().year).count(),
        'recent_enquiry': UserEnquiryModel.objects.filter(enquiry_status="pending").order_by('-enquiry_create_at')
    }
    return render(request, 'admin/admin_home.html', admin_home_data)


@login_required(login_url='/login')
def delete_banner(request, banner_id):
    """
    View for deleting a banner.
    This view allows admins to delete a banner.
    """
    try:
        banner = BannerModel.objects.get(pk=banner_id)
        banner.delete()
        return redirect('/admin_poster')
    except BannerModel.DoesNotExist:
        return redirect('/admin_poster')


@login_required(login_url='/login')
def admin_add_poster(request):
    """
    View for adding a new banner.
    This view allows admins to add a new banner with various details including images.
    """
    context = {'count': BannerModel.objects.all().count()}
    if request.method == 'POST':
        banner = BannerModel()
        banner.banner_image = request.FILES['poster_file']
        banner.save()
        return redirect('/admin_poster')
    return render(request, 'admin/admin_add_poster.html', context)


@login_required(login_url='/login')
def admin_category(request):
    """
    View for managing categories.
    This view displays a list of categories and allows filtering by category.
    """

    category = {'category': ProductCategoryModel.objects.annotate(product_count=Count('productmodel'))}

    return render(request, 'admin/admin_category.html', category)


@login_required(login_url='/login')
def admin_add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()

        if ProductCategoryModel.objects.filter(category_name__iexact=category_name).exists():
            return render(request, 'admin/admin_add_category.html', {'status': 'invalid'})

        category = ProductCategoryModel(category_name=category_name)
        category.save()
        return redirect('/admin_category')
    return render(request, 'admin/admin_add_category.html')


@login_required(login_url='/login')
def admin_remove_category(request, category_id):
    try:

        category = get_object_or_404(ProductCategoryModel, pk=category_id)
        other_category = ProductCategoryModel.objects.get_or_create(category_name="Other")[0]
        products_to_move = ProductModel.objects.filter(product_category=category)
        print(products_to_move.values())
        for product in products_to_move:
            product.product_category = other_category
            product.save()

        # Now delete the category
        category.delete()
        return redirect('/admin_category')
    except:
        return redirect('/admin_category')


@login_required(login_url='/login')
def admin_edit_category(request, category_id):
    category = get_object_or_404(ProductCategoryModel, pk=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()
        if category_name.lower() != category.category_name.lower():
            if ProductCategoryModel.objects.filter(category_name__iexact=category_name).exists():
                return render(request, 'admin/admin_edit_category.html', {'status': 'invalid'})

        category.category_name = category_name
        category.save()
        return redirect('/admin_category')
    return render(request, 'admin/admin_edit_category.html', {'category': category})


@login_required(login_url='/login')
def admin_products(request):
    """
    View for managing products.
    This view displays a list of products and allows filtering by category.
    """
    product_data = {'products': ProductModel.objects.all(
    ), 'categories': ProductCategoryModel.objects.all()}
    if request.method == 'POST':
        if request.POST.get('sort_field') != "all":
            product_data['products'] = ProductModel.objects.filter(
                product_category=ProductCategoryModel.objects.get(category_id=int(request.POST.get('sort_field'))))
    return render(request, 'admin/admin_product.html', product_data)


@login_required(login_url='/login')
def add_product(request):
    """
    View for adding a new product.
    This view allows admins to add a new product with various details including images.
    """
    category = ProductCategoryModel.objects.all()
    status = 'ok'
    if request.method == 'POST':
        if ProductModel.objects.filter(product_name__iexact=request.POST.get('product_name')).exists():
            status = 'invalid'
        else:
            product = ProductModel()
            product.product_id = request.POST.get('product_name').replace(" ", "_").lower()
            product.product_name = request.POST.get('product_name')

            product.product_color = request.POST.get('product_color')
            product.product_material = request.POST.get('product_material')
            product.product_description = request.POST.get('product_description')
            product.product_price = request.POST.get('product_price')
            product.product_category = ProductCategoryModel.objects.get(
                category_id=int(request.POST.get('product_category')))
            product.save()

            # Saving product images
            images = request.FILES.getlist('product_images')
            for image in images:
                ProductImageModel.objects.create(
                    product_id=product, product_image=image)
            return redirect('/admin_products')

    return render(request, 'admin/admin_add_product.html', {'category': category, "status": status})


@login_required(login_url='/login')
def delete_product(request, product_id):
    """
    View for deleting a product.
    This view deletes a product along with its associated images.
    """
    if request.method == 'DELETE':
        product = get_object_or_404(ProductModel, pk=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url='/login')
def admin_poster(request):
    """
    View for managing banners.
    This view displays a list of banners.
    """
    banner_data = {'banners': BannerModel.objects.all()}
    return render(request, 'admin/admin_banner.html', banner_data)


@login_required(login_url='/login')
def admin_enquiry(request):
    """
    View for managing user enquiries.
    This view provides functionalities to search, filter, and sort user enquiries.
    """
    current_week = timezone.now().isocalendar()[1]

    admin_enquiry_data = {
        'total_enquiry_count': UserEnquiryModel.objects.all().count(),
        'enquiry_month_count': UserEnquiryModel.objects.filter(enquiry_create_at__month=timezone.now().month).count(),
        'enquiry_week_count': UserEnquiryModel.objects.filter(enquiry_create_at__week=current_week).count(),
        'enquiry': UserEnquiryModel.objects.all().order_by('-enquiry_create_at')
    }
    if request.method == "POST":
        search = request.POST.get("userSearch")
        start_date = request.POST.get("startDate")
        end_date = request.POST.get("endDate")
        results = UserEnquiryModel.objects.filter(
            Q(enquiry_user__icontains=search) | Q(
                enquiry_phone__icontains=search) | Q(
                enquiry_subject__icontains=search) | Q(
                enquiry_message__icontains=search)
        )

        if request.POST.get('sort_field'):
            if request.POST.get('sort_field') == 'read':
                results = results.filter(enquiry_status="read")
            elif request.POST.get('sort_field') == 'pending':
                results = results.filter(enquiry_status="pending")
        if start_date and end_date:
            results = results.filter(
                enquiry_create_at__range=[start_date, end_date]).order_by('-enquiry_create_at')

        admin_enquiry_data['enquiry'] = results.order_by('-enquiry_create_at')

    return render(request, 'admin/admin_enquiry.html', admin_enquiry_data)


@login_required(login_url='/login')
def delete_enquiry(request, enquiry_id):
    """
    View for deleting a user enquiry.
    """
    if request.method == 'DELETE':
        enquiry = UserEnquiryModel.objects.get(pk=enquiry_id)
        enquiry.delete()
        return JsonResponse({'message': 'Enquiry deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url='/login')
def admin_service_video(request):
    """
    View for managing service videos.
    This view allows admins to update the service video.
    """
    video = ServiceVideo.objects.get(video_id=1)

    if request.method == "POST":
        video = ServiceVideo()
        video.video_id = 1
        video.video = request.FILES.get('video')
        video.save()
        return redirect('/admin_service_video')
    return render(request, 'admin/admin_service_video.html', {'video': video})


@login_required(login_url='/login')
def update_enquiry_status(request, enquiry_id):
    """
    View for updating the status of a user enquiry.
    This view updates the status of a user enquiry to "read".
    """
    if request.method == 'PATCH':
        enquiry = UserEnquiryModel.objects.get(pk=enquiry_id)
        enquiry.enquiry_status = 'read'
        enquiry.save()
        return JsonResponse({'message': 'Enquiry status updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# +++++++++++++++++++++++++++++++++++++++  user section +++++++++++++++++++++++++++++++++++++++++
def user_home_page(request):
    """
    View for displaying the user home page.
    - Fetches all products, an associated service video, and active banners.
    - Prefetches related products for each category for better performance.
    - Renders the 'user_home_page.html' template with fetched data.
    """
    products = ProductModel.objects.all()
    video = ServiceVideo.objects.get(video_id=1)
    banner = BannerModel.objects.filter(banner_status="Active")

    return render(request, 'user/user_home_page.html',
                  {'products': products, 'video': video,
                   'banner_data': banner})


def user_product(request):
    """
    View for displaying the user product page.
    - Fetches all products, and search products.
    - Prefetches related products for each category for better performance.
    - Renders the 'user_product.html' template with fetched data.
    """

    products = ProductModel.objects.all()
    categories = ProductCategoryModel.objects.all()
    search = ''
    if request.method == 'POST':
        search = request.POST.get('search_text')
        if search:
            search = re.sub(r'\s+', ' ', search)
            search_terms = search.split()
            query = Q()
            for term in search_terms:
                query |= Q(product_name__icontains=term) | \
                         Q(product_description__icontains=term) | \
                         Q(product_price__icontains=term) | \
                         Q(product_material__icontains=term) | \
                         Q(product_category__category_name__icontains=term)
            products = products.filter(query)

        if request.POST.get('category'):
            category_id = int(request.POST.get('category'))
            products = products.filter(product_category__category_id=category_id)

    return render(request, 'user/user_product.html', {'products': products, 'categories': categories, 'search': search})


def product_view(request, id):
    """
    View for displaying details of a specific product.
    - Fetches the product with the given 'id' from the database.
    - Prefetches related product images for better performance.
    - Renders the 'product_view.html' template with the fetched product and all product categories.
    """
    categories_with_products = ProductCategoryModel.objects.prefetch_related('productmodel_set').all()
    product_data = ProductModel.objects.prefetch_related('productimagemodel_set').get(product_id=id)
    context = {'product': product_data}
    return render(request, 'user/product_view.html', context)


def user_about_page(request):
    """
    View for displaying the user about page.
    - Renders the 'user_about_page.html' template.
    - Fetches all product categories with their associated products for navigation.
    """

    return render(request, 'user/user_about_page.html')


def user_contact_page(request):
    """
    View for displaying the user contact page.
    - Renders the 'user_contact_page.html' template.
    - Fetches all product categories with their associated products for navigation.
    """

    return render(request, 'user/user_contact_page.html', )


def user_contact(request):
    """
    View for handling user enquiries submitted via the contact form.
    - If the request method is POST, extracts form data (name, email, subject, message).
    - Creates a new 'UserEnquiryModel' instance and saves it to the database.
    - Returns a JSON response with success status upon successful form submission.
    """
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        user_enquiry_obj = UserEnquiryModel()
        user_enquiry_obj.enquiry_user = name
        user_enquiry_obj.enquiry_phone = email
        user_enquiry_obj.enquiry_subject = subject
        user_enquiry_obj.enquiry_message = message
        user_enquiry_obj.save()

        return JsonResponse({"success": True})

    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})


def user_privacy_policy(request):
    return render(request, 'user/user_privacy_policy.html')
