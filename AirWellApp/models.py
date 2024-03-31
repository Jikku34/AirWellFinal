from django.db import models


class ProductCategoryModel(models.Model):
    """
    Model representing product categories.

    Fields:
        category_id (AutoField): Primary Key for the category.
        category_name (CharField): Name of the category.
    """
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category_table"


class ProductModel(models.Model):
    """
    Model representing products.

    Fields:
        product_id (AutoField): Primary Key for the product.
        product_name (CharField): Name of the product.
        product_description (TextField): Description of the product.
        product_material (CharField): Material of the product.
        product_color (CharField): Color of the product.
        product_price (CharField): Price of the product.
        product_create_at (DateTimeField): Date and time when the product was created.
        product_status (CharField): Status of the product (default set to "Active").
        product_category (ForeignKey): Category to which the product belongs.
    """
    product_id = models.CharField(max_length=200,primary_key=True)
    product_name = models.CharField(max_length=100)

    product_description = models.TextField()
    product_material = models.CharField(max_length=100)
    product_color = models.CharField(max_length=100)
    product_price = models.CharField(max_length=100)
    product_create_at = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=100, default="Active")
    product_category = models.ForeignKey(
        ProductCategoryModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product_table"


class ProductImageModel(models.Model):
    """
    Model representing images associated with products.

    Fields:
        product_id (ForeignKey): Product to which the image belongs.
        product_image (ImageField): Image file associated with the product.
    """
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='images/', null=True)

    def __int__(self):
        return self.product_id

    class Meta:
        db_table = "product_images"


class UserEnquiryModel(models.Model):
    """
    Model representing user enquiries.

    Fields:
        enquiry_id (AutoField): Primary Key for the enquiry.
        enquiry_user (CharField): Name of the user making the enquiry.
        enquiry_phone (CharField): Phone number of the user.
        enquiry_subject (CharField): Subject of the enquiry.
        enquiry_message (TextField): Message content of the enquiry.
        enquiry_create_at (DateTimeField): Date and time when the enquiry was created.
        enquiry_status (CharField): Status of the enquiry (default set to "pending").
    """
    enquiry_id = models.AutoField(primary_key=True)
    enquiry_user = models.CharField(max_length=200)
    enquiry_phone = models.CharField(max_length=100)
    enquiry_subject = models.CharField(max_length=300)
    enquiry_message = models.TextField()
    enquiry_create_at = models.DateTimeField(auto_now_add=True, null=True)
    enquiry_status = models.CharField(max_length=100, default="pending")

    class Meta:
        db_table = "enquiry_table"


class BannerModel(models.Model):
    """
    Model representing banners.

    Fields:
        banner_id (AutoField): Primary Key for the banner.
        banner_image (ImageField): Image file associated with the banner.
        banner_created_at (DateTimeField): Date and time when the banner was created.
        banner_status (CharField): Status of the banner (default set to "Active").
    """
    banner_id = models.AutoField(primary_key=True)
    banner_image = models.ImageField(upload_to='images/', null=True)

    banner_created_at = models.DateTimeField(auto_now_add=True)
    banner_status = models.CharField(max_length=100, default="Active")


class ServiceVideo(models.Model):
    """
    Model representing service videos.

    Fields:
        video_id (AutoField): Primary Key for the video.
        video (FileField): Video file associated with the service.
    """
    video_id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to='videos/', null=True)
