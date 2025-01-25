from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from companies.models import Company

class ProductCatalog(BaseModel):
    """Catálogo de produtos de uma empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='catalogs')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    hierarchy_settings = models.JSONField(default=dict)
    is_public = models.BooleanField(default=True)
    visibility_rules = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Product Catalog')
        verbose_name_plural = _('Product Catalogs')

    def __str__(self):
        return f"{self.name} - {self.company}"

class Product(BaseModel):
    """Produto no catálogo"""
    catalog = models.ForeignKey(ProductCatalog, on_delete=models.CASCADE, related_name='products')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    sku_prefix = models.CharField(max_length=20)
    view_count = models.PositiveIntegerField(default=0)
    categories = models.JSONField(default=list)
    attributes = models.JSONField(default=dict)
    media_gallery = models.JSONField(default=list)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_class = models.CharField(max_length=50)
    requires_shipping = models.BooleanField(default=True)
    shipping_settings = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    seo_data = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        unique_together = ['company', 'sku_prefix']

    def __str__(self):
        return f"{self.name} ({self.sku_prefix})"

class ProductVariant(BaseModel):
    """Variante de um produto"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True)
    variant_attributes = models.JSONField(default=dict)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    barcode = models.CharField(max_length=100, blank=True)
    dimensions = models.JSONField(default=dict)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    is_active = models.BooleanField(default=True)
    stock_settings = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product')
                                
                                
class Customer(BaseModel):
    """Cliente final da empresa"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ('individual', _('Individual')),
            ('business', _('Business')),
        ]
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200, blank=True)
    favorite_products = models.ManyToManyField(Product, related_name='favorited_by', blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    contact_preferences = models.JSONField(default=dict)
    marketing_preferences = models.JSONField(default=dict)
    segments = models.JSONField(default=list)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = ['company', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CustomerAddress(BaseModel):
    """Endereços do cliente"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(
        max_length=20,
        choices=[
            ('billing', _('Billing')),
            ('shipping', _('Shipping')),
            ('both', _('Both')),
        ]
    )
    street_line1 = models.CharField(max_length=200)
    street_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2)  # ISO country code
    is_default = models.BooleanField(default=False)
    address_metadata = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Customer Address')
        verbose_name_plural = _('Customer Addresses')

class Order(BaseModel):
    """Pedido realizado pelo cliente"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', _('Draft')),
            ('pending', _('Pending')),
            ('confirmed', _('Confirmed')),
            ('processing', _('Processing')),
            ('shipped', _('Shipped')),
            ('delivered', _('Delivered')),
            ('cancelled', _('Cancelled')),
        ],
        default='draft'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.PROTECT,
        related_name='shipping_orders'
    )
    billing_address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.PROTECT,
        related_name='billing_orders'
    )
    payment_info = models.JSONField(default=dict)
    shipping_info = models.JSONField(default=dict)
    notes = models.TextField(blank=True)
    custom_fields = models.JSONField(default=dict)
    
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', _('Pending')),
            ('paid', _('Paid')),
            ('failed', _('Failed')),
            ('refunded', _('Refunded')),
        ],
        default='pending'
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

class OrderItem(BaseModel):
    """Item individual em um pedido"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='order_items'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='order_items'
    )
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_metadata = models.JSONField(default=dict)
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')


class Cart(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    is_active = models.BooleanField(default=True)

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class ProductReview(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)