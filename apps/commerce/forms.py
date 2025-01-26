from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ProductCatalog, Product, ProductVariant, Customer, CustomerAddress, Order, OrderItem, Cart, CartItem, ProductReview
from django.forms import ValidationError
from django.forms import JSONInput

class ProductCatalogForm(forms.ModelForm):
    class Meta:
        model = ProductCatalog
        fields = ['company', 'name', 'description', 'hierarchy_settings', 'is_public', 'visibility_rules']
        labels = {
            'company': _('Company'),
            'name': _('Name'),
            'description': _('Description'),
            'hierarchy_settings': _('Hierarchy Settings'),
            'is_public': _('Is Public'),
            'visibility_rules': _('Visibility Rules'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter a name for the product catalog.'),
                'max_length': _('The name cannot exceed 200 characters.'),
            },
            'company': {
                'required': _('Please select a company for this product catalog.'),
            },
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'hierarchy_settings': forms.JSONInput(),
            'visibility_rules': forms.JSONInput(),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and ProductCatalog.objects.filter(name=name, company=self.cleaned_data.get('company')).exists():
            raise forms.ValidationError(_('A product catalog with this name already exists for this company.'))
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['is_public'].help_text = _('If checked, this catalog will be visible to all customers.')

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Name': _('Nom'),
    'Description': _('Description'),
    'Hierarchy Settings': _('Paramètres de hiérarchie'),
    'Is Public': _('Est public'),
    'Visibility Rules': _('Règles de visibilité'),
    'Please enter a name for the product catalog.': _('Veuillez saisir un nom pour le catalogue de produits.'),
    'The name cannot exceed 200 characters.': _('Le nom ne peut pas dépasser 200 caractères.'),
    'Please select a company for this product catalog.': _('Veuillez sélectionner une entreprise pour ce catalogue de produits.'),
    'A product catalog with this name already exists for this company.': _('Un catalogue de produits avec ce nom existe déjà pour cette entreprise.'),
    'If checked, this catalog will be visible to all customers.': _('Si coché, ce catalogue sera visible pour tous les clients.'),
}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['catalog', 'company', 'name', 'description', 'sku_prefix', 'categories', 'attributes', 
                  'media_gallery', 'base_price', 'tax_class', 'requires_shipping', 'shipping_settings', 
                  'is_active', 'seo_data']
        labels = {
            'catalog': _('Catalog'),
            'company': _('Company'),
            'name': _('Name'),
            'description': _('Description'),
            'sku_prefix': _('SKU Prefix'),
            'categories': _('Categories'),
            'attributes': _('Attributes'),
            'media_gallery': _('Media Gallery'),
            'base_price': _('Base Price'),
            'tax_class': _('Tax Class'),
            'requires_shipping': _('Requires Shipping'),
            'shipping_settings': _('Shipping Settings'),
            'is_active': _('Is Active'),
            'seo_data': _('SEO Data'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter a product name.'),
                'max_length': _('The product name cannot exceed 200 characters.'),
            },
            'sku_prefix': {
                'required': _('Please enter an SKU prefix.'),
                'max_length': _('The SKU prefix cannot exceed 20 characters.'),
            },
            'base_price': {
                'required': _('Please enter a base price for the product.'),
                'invalid': _('Please enter a valid price.'),
            },
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'categories': forms.JSONInput(),
            'attributes': forms.JSONInput(),
            'media_gallery': forms.JSONInput(),
            'shipping_settings': forms.JSONInput(),
            'seo_data': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        sku_prefix = cleaned_data.get('sku_prefix')

        if company and sku_prefix:
            if Product.objects.filter(company=company, sku_prefix=sku_prefix).exists():
                raise forms.ValidationError(_('A product with this SKU prefix already exists for this company.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catalog'].widget.attrs['class'] = 'select2'
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['tax_class'].widget.attrs['class'] = 'select2'
        self.fields['is_active'].help_text = _('If unchecked, this product will not be visible in the catalog.')

# Translations for French
_ = lambda s: s

fr_translations = {
    'Catalog': _('Catalogue'),
    'Company': _('Entreprise'),
    'Name': _('Nom'),
    'Description': _('Description'),
    'SKU Prefix': _('Préfixe SKU'),
    'Categories': _('Catégories'),
    'Attributes': _('Attributs'),
    'Media Gallery': _('Galerie média'),
    'Base Price': _('Prix de base'),
    'Tax Class': _('Classe fiscale'),
    'Requires Shipping': _('Nécessite une expédition'),
    'Shipping Settings': _('Paramètres d\'expédition'),
    'Is Active': _('Est actif'),
    'SEO Data': _('Données SEO'),
    'Please enter a product name.': _('Veuillez saisir un nom de produit.'),
    'The product name cannot exceed 200 characters.': _('Le nom du produit ne peut pas dépasser 200 caractères.'),
    'Please enter an SKU prefix.': _('Veuillez saisir un préfixe SKU.'),
    'The SKU prefix cannot exceed 20 characters.': _('Le préfixe SKU ne peut pas dépasser 20 caractères.'),
    'Please enter a base price for the product.': _('Veuillez saisir un prix de base pour le produit.'),
    'Please enter a valid price.': _('Veuillez saisir un prix valide.'),
    'A product with this SKU prefix already exists for this company.': _('Un produit avec ce préfixe SKU existe déjà pour cette entreprise.'),
    'If unchecked, this product will not be visible in the catalog.': _('Si non coché, ce produit ne sera pas visible dans le catalogue.'),
}


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'sku', 'name', 'attributes', 'price_adjustment', 'stock_quantity', 
                  'weight', 'dimensions', 'media_gallery', 'is_active']
        labels = {
            'product': _('Product'),
            'sku': _('SKU'),
            'name': _('Name'),
            'attributes': _('Attributes'),
            'price_adjustment': _('Price Adjustment'),
            'stock_quantity': _('Stock Quantity'),
            'weight': _('Weight'),
            'dimensions': _('Dimensions'),
            'media_gallery': _('Media Gallery'),
            'is_active': _('Is Active'),
        }
        error_messages = {
            'sku': {
                'required': _('Please enter an SKU for the product variant.'),
                'unique': _('This SKU is already in use. Please enter a unique SKU.'),
            },
            'name': {
                'required': _('Please enter a name for the product variant.'),
                'max_length': _('The variant name cannot exceed 200 characters.'),
            },
            'stock_quantity': {
                'min_value': _('Stock quantity cannot be negative.'),
            },
        }
        widgets = {
            'attributes': forms.JSONInput(),
            'dimensions': forms.JSONInput(),
            'media_gallery': forms.JSONInput(),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        product = self.cleaned_data.get('product')
        if sku and product:
            if not sku.startswith(product.sku_prefix):
                raise forms.ValidationError(_('SKU must start with the product\'s SKU prefix: {0}').format(product.sku_prefix))
        return sku

    def clean_price_adjustment(self):
        price_adjustment = self.cleaned_data.get('price_adjustment')
        if price_adjustment is not None and price_adjustment < 0:
            raise forms.ValidationError(_('Price adjustment cannot be negative.'))
        return price_adjustment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'select2'
        self.fields['is_active'].help_text = _('If unchecked, this variant will not be available for purchase.')

# Translations for French
_ = lambda s: s

fr_translations = {
    'Product': _('Produit'),
    'SKU': _('UGS'),
    'Name': _('Nom'),
    'Attributes': _('Attributs'),
    'Price Adjustment': _('Ajustement de prix'),
    'Stock Quantity': _('Quantité en stock'),
    'Weight': _('Poids'),
    'Dimensions': _('Dimensions'),
    'Media Gallery': _('Galerie média'),
    'Is Active': _('Est actif'),
    'Please enter an SKU for the product variant.': _('Veuillez saisir une UGS pour la variante du produit.'),
    'This SKU is already in use. Please enter a unique SKU.': _('Cette UGS est déjà utilisée. Veuillez saisir une UGS unique.'),
    'Please enter a name for the product variant.': _('Veuillez saisir un nom pour la variante du produit.'),
    'The variant name cannot exceed 200 characters.': _('Le nom de la variante ne peut pas dépasser 200 caractères.'),
    'Stock quantity cannot be negative.': _('La quantité en stock ne peut pas être négative.'),
    'SKU must start with the product\'s SKU prefix: {0}': _('L\'UGS doit commencer par le préfixe UGS du produit : {0}'),
    'Price adjustment cannot be negative.': _('L\'ajustement de prix ne peut pas être négatif.'),
    'If unchecked, this variant will not be available for purchase.': _('Si non coché, cette variante ne sera pas disponible à l\'achat.'),
}


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'user', 'customer_type', 'status', 'contact_info', 'billing_address', 
                  'shipping_address', 'tax_info', 'payment_methods', 'preferences', 'notes']
        labels = {
            'company': _('Company'),
            'user': _('User'),
            'customer_type': _('Customer Type'),
            'status': _('Status'),
            'contact_info': _('Contact Information'),
            'billing_address': _('Billing Address'),
            'shipping_address': _('Shipping Address'),
            'tax_info': _('Tax Information'),
            'payment_methods': _('Payment Methods'),
            'preferences': _('Preferences'),
            'notes': _('Notes'),
        }
        error_messages = {
            'user': {
                'required': _('Please select a user for this customer.'),
            },
            'customer_type': {
                'required': _('Please select a customer type.'),
            },
            'status': {
                'required': _('Please select a status for this customer.'),
            },
        }
        widgets = {
            'contact_info': forms.JSONInput(),
            'billing_address': forms.JSONInput(),
            'shipping_address': forms.JSONInput(),
            'tax_info': forms.JSONInput(),
            'payment_methods': forms.JSONInput(),
            'preferences': forms.JSONInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_tax_info(self):
        tax_info = self.cleaned_data.get('tax_info')
        if tax_info:
            if 'tax_id' not in tax_info:
                raise forms.ValidationError(_('Tax information must include a tax ID.'))
        return tax_info

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['user'].widget.attrs['class'] = 'select2'
        self.fields['customer_type'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'User': _('Utilisateur'),
    'Customer Type': _('Type de client'),
    'Status': _('Statut'),
    'Contact Information': _('Informations de contact'),
    'Billing Address': _('Adresse de facturation'),
    'Shipping Address': _('Adresse de livraison'),
    'Tax Information': _('Informations fiscales'),
    'Payment Methods': _('Méthodes de paiement'),
    'Preferences': _('Préférences'),
    'Notes': _('Notes'),
    'Please select a user for this customer.': _('Veuillez sélectionner un utilisateur pour ce client.'),
    'Please select a customer type.': _('Veuillez sélectionner un type de client.'),
    'Please select a status for this customer.': _('Veuillez sélectionner un statut pour ce client.'),
    'Tax information must include a tax ID.': _('Les informations fiscales doivent inclure un numéro d\'identification fiscale.'),
}



class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['customer', 'address_type', 'is_default', 'name', 'street_address', 'city', 
                  'state', 'postal_code', 'country', 'phone', 'email', 'additional_info']
        labels = {
            'customer': _('Customer'),
            'address_type': _('Address Type'),
            'is_default': _('Is Default'),
            'name': _('Name'),
            'street_address': _('Street Address'),
            'city': _('City'),
            'state': _('State'),
            'postal_code': _('Postal Code'),
            'country': _('Country'),
            'phone': _('Phone'),
            'email': _('Email'),
            'additional_info': _('Additional Information'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter a name for this address.'),
            },
            'street_address': {
                'required': _('Please enter a street address.'),
            },
            'city': {
                'required': _('Please enter a city.'),
            },
            'postal_code': {
                'required': _('Please enter a postal code.'),
            },
            'country': {
                'required': _('Please select a country.'),
            },
        }
        widgets = {
            'additional_info': forms.JSONInput(),
        }

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        country = self.cleaned_data.get('country')
        if country and postal_code:
            # Here you could add country-specific postal code validation
            pass
        return postal_code

    def clean(self):
        cleaned_data = super().clean()
        address_type = cleaned_data.get('address_type')
        is_default = cleaned_data.get('is_default')
        customer = cleaned_data.get('customer')

        if is_default and customer:
            existing_default = CustomerAddress.objects.filter(
                customer=customer, 
                address_type=address_type, 
                is_default=True
            ).exclude(pk=self.instance.pk if self.instance else None).exists()

            if existing_default:
                self.add_error('is_default', _('Another address of this type is already set as default.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['class'] = 'select2'
        self.fields['country'].widget.attrs['class'] = 'select2'
        self.fields['address_type'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Customer': _('Client'),
    'Address Type': _('Type d\'adresse'),
    'Is Default': _('Est par défaut'),
    'Name': _('Nom'),
    'Street Address': _('Adresse'),
    'City': _('Ville'),
    'State': _('État/Région'),
    'Postal Code': _('Code postal'),
    'Country': _('Pays'),
    'Phone': _('Téléphone'),
    'Email': _('E-mail'),
    'Additional Information': _('Informations supplémentaires'),
    'Please enter a name for this address.': _('Veuillez entrer un nom pour cette adresse.'),
    'Please enter a street address.': _('Veuillez entrer une adresse.'),
    'Please enter a city.': _('Veuillez entrer une ville.'),
    'Please enter a postal code.': _('Veuillez entrer un code postal.'),
    'Please select a country.': _('Veuillez sélectionner un pays.'),
    'Another address of this type is already set as default.': _('Une autre adresse de ce type est déjà définie par défaut.'),
}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['company', 'customer', 'order_number', 'status', 'order_date', 'total_amount', 
                  'tax_amount', 'shipping_amount', 'discount_amount', 'currency', 'payment_status', 
                  'payment_method', 'shipping_method', 'billing_address', 'shipping_address', 
                  'notes', 'metadata']
        labels = {
            'company': _('Company'),
            'customer': _('Customer'),
            'order_number': _('Order Number'),
            'status': _('Status'),
            'order_date': _('Order Date'),
            'total_amount': _('Total Amount'),
            'tax_amount': _('Tax Amount'),
            'shipping_amount': _('Shipping Amount'),
            'discount_amount': _('Discount Amount'),
            'currency': _('Currency'),
            'payment_status': _('Payment Status'),
            'payment_method': _('Payment Method'),
            'shipping_method': _('Shipping Method'),
            'billing_address': _('Billing Address'),
            'shipping_address': _('Shipping Address'),
            'notes': _('Notes'),
            'metadata': _('Metadata'),
        }
        error_messages = {
            'customer': {
                'required': _('Please select a customer for this order.'),
            },
            'order_number': {
                'unique': _('An order with this number already exists.'),
            },
            'total_amount': {
                'min_value': _('Total amount cannot be negative.'),
            },
        }
        widgets = {
            'order_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'metadata': forms.JSONInput(),
            'billing_address': forms.JSONInput(),
            'shipping_address': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get('total_amount')
        tax_amount = cleaned_data.get('tax_amount', 0)
        shipping_amount = cleaned_data.get('shipping_amount', 0)
        discount_amount = cleaned_data.get('discount_amount', 0)

        if total_amount is not None:
            calculated_total = (tax_amount or 0) + (shipping_amount or 0) - (discount_amount or 0)
            if abs(total_amount - calculated_total) > 0.01:  # Allow for small rounding differences
                raise forms.ValidationError(_('Total amount must equal the sum of tax and shipping minus discounts.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['customer'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'
        self.fields['currency'].widget.attrs['class'] = 'select2'
        self.fields['payment_status'].widget.attrs['class'] = 'select2'
        self.fields['payment_method'].widget.attrs['class'] = 'select2'
        self.fields['shipping_method'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Customer': _('Client'),
    'Order Number': _('Numéro de commande'),
    'Status': _('Statut'),
    'Order Date': _('Date de commande'),
    'Total Amount': _('Montant total'),
    'Tax Amount': _('Montant des taxes'),
    'Shipping Amount': _('Frais de livraison'),
    'Discount Amount': _('Montant de la remise'),
    'Currency': _('Devise'),
    'Payment Status': _('Statut du paiement'),
    'Payment Method': _('Méthode de paiement'),
    'Shipping Method': _('Méthode de livraison'),
    'Billing Address': _('Adresse de facturation'),
    'Shipping Address': _('Adresse de livraison'),
    'Notes': _('Notes'),
    'Metadata': _('Métadonnées'),
    'Please select a customer for this order.': _('Veuillez sélectionner un client pour cette commande.'),
    'An order with this number already exists.': _('Une commande avec ce numéro existe déjà.'),
    'Total amount cannot be negative.': _('Le montant total ne peut pas être négatif.'),
    'Total amount must be at least the sum of tax and shipping minus discounts.': _('Le montant total doit être au moins égal à la somme des taxes et des frais de livraison moins les remises.'),
}
 

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'unit_price', 'total_price', 'tax_amount', 
                  'discount_amount', 'metadata']
        labels = {
            'order': _('Order'),
            'product': _('Product'),
            'quantity': _('Quantity'),
            'unit_price': _('Unit Price'),
            'total_price': _('Total Price'),
            'tax_amount': _('Tax Amount'),
            'discount_amount': _('Discount Amount'),
            'metadata': _('Metadata'),
        }
        error_messages = {
            'order': {
                'required': _('Please select an order for this item.'),
            },
            'product': {
                'required': _('Please select a product for this item.'),
            },
            'quantity': {
                'min_value': _('Quantity must be greater than zero.'),
            },
            'unit_price': {
                'min_value': _('Unit price cannot be negative.'),
            },
            'total_price': {
                'min_value': _('Total price cannot be negative.'),
            },
        }
        widgets = {
            'metadata': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        total_price = cleaned_data.get('total_price')
        tax_amount = cleaned_data.get('tax_amount', 0)
        discount_amount = cleaned_data.get('discount_amount', 0)

        if quantity is not None and unit_price is not None and total_price is not None:
            calculated_total = quantity * unit_price + tax_amount - discount_amount
            
            if abs(total_price - calculated_total) > 0.01:  # Allow for small rounding differences
                raise forms.ValidationError(_('Total price must equal quantity times unit price, plus tax, minus discount.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].widget.attrs['class'] = 'select2'
        self.fields['product'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Order': _('Commande'),
    'Product': _('Produit'),
    'Quantity': _('Quantité'),
    'Unit Price': _('Prix unitaire'),
    'Total Price': _('Prix total'),
    'Tax Amount': _('Montant des taxes'),
    'Discount Amount': _('Montant de la remise'),
    'Metadata': _('Métadonnées'),
    'Please select an order for this item.': _('Veuillez sélectionner une commande pour cet article.'),
    'Please select a product for this item.': _('Veuillez sélectionner un produit pour cet article.'),
    'Quantity must be greater than zero.': _('La quantité doit être supérieure à zéro.'),
    'Unit price cannot be negative.': _('Le prix unitaire ne peut pas être négatif.'),
    'Total price cannot be negative.': _('Le prix total ne peut pas être négatif.'),
    'Total price must equal quantity times unit price, plus tax, minus discount.': _('Le prix total doit être égal à la quantité multipliée par le prix unitaire, plus les taxes, moins la remise.'),
}



class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['company', 'customer', 'session_id', 'status', 'created_at', 'updated_at', 
                  'expires_at', 'metadata']
        labels = {
            'company': _('Company'),
            'customer': _('Customer'),
            'session_id': _('Session ID'),
            'status': _('Status'),
            'created_at': _('Created At'),
            'updated_at': _('Updated At'),
            'expires_at': _('Expires At'),
            'metadata': _('Metadata'),
        }
        error_messages = {
            'company': {
                'required': _('Please select a company for this cart.'),
            },
            'session_id': {
                'required': _('Session ID is required.'),
                'unique': _('A cart with this session ID already exists.'),
            },
            'expires_at': {
                'invalid': _('Please enter a valid expiration date and time.'),
            },
        }
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'updated_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'metadata': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        created_at = cleaned_data.get('created_at')
        updated_at = cleaned_data.get('updated_at')
        expires_at = cleaned_data.get('expires_at')

        if created_at and updated_at and created_at > updated_at:
            raise forms.ValidationError(_('Updated at cannot be earlier than created at.'))

        if created_at and expires_at and expires_at < created_at:
            raise forms.ValidationError(_('Expiration date cannot be earlier than creation date.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].widget.attrs['class'] = 'select2'
        self.fields['customer'].widget.attrs['class'] = 'select2'
        self.fields['status'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Company': _('Entreprise'),
    'Customer': _('Client'),
    'Session ID': _('ID de session'),
    'Status': _('Statut'),
    'Created At': _('Créé le'),
    'Updated At': _('Mis à jour le'),
    'Expires At': _('Expire le'),
    'Metadata': _('Métadonnées'),
    'Please select a company for this cart.': _('Veuillez sélectionner une entreprise pour ce panier.'),
    'Session ID is required.': _("L'ID de session est requis."),
    'A cart with this session ID already exists.': _('Un panier avec cet ID de session existe déjà.'),
    'Please enter a valid expiration date and time.': _("Veuillez entrer une date et une heure d'expiration valides."),
    'Updated at cannot be earlier than created at.': _('La date de mise à jour ne peut pas être antérieure à la date de création.'),
    'Expiration date cannot be earlier than creation date.': _("La date d'expiration ne peut pas être antérieure à la date de création."),
}
 

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'unit_price', 'total_price', 'metadata']
        labels = {
            'cart': _('Cart'),
            'product': _('Product'),
            'quantity': _('Quantity'),
            'unit_price': _('Unit Price'),
            'total_price': _('Total Price'),
            'metadata': _('Metadata'),
        }
        error_messages = {
            'cart': {
                'required': _('Please select a cart for this item.'),
            },
            'product': {
                'required': _('Please select a product for this item.'),
            },
            'quantity': {
                'required': _('Quantity is required.'),
                'min_value': _('Quantity must be greater than zero.'),
            },
            'unit_price': {
                'required': _('Unit price is required.'),
                'min_value': _('Unit price cannot be negative.'),
            },
            'total_price': {
                'required': _('Total price is required.'),
                'min_value': _('Total price cannot be negative.'),
            },
        }
        widgets = {
            'metadata': forms.JSONInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        total_price = cleaned_data.get('total_price')

        if quantity is not None and unit_price is not None and total_price is not None:
            calculated_total = quantity * unit_price
            if abs(total_price - calculated_total) > 0.01:  # Allow for small rounding differences
                raise forms.ValidationError(_('Total price must equal quantity times unit price.'))
        elif any([quantity is not None, unit_price is not None, total_price is not None]):
            # If at least one of the fields is filled, but not all of them
            raise forms.ValidationError(_('Quantity, unit price, and total price must all be provided.'))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cart'].widget.attrs['class'] = 'select2'
        self.fields['product'].widget.attrs['class'] = 'select2'

# Translations for French
_ = lambda s: s

fr_translations = {
    'Cart': _('Panier'),
    'Product': _('Produit'),
    'Quantity': _('Quantité'),
    'Unit Price': _('Prix unitaire'),
    'Total Price': _('Prix total'),
    'Metadata': _('Métadonnées'),
    'Please select a cart for this item.': _('Veuillez sélectionner un panier pour cet article.'),
    'Please select a product for this item.': _('Veuillez sélectionner un produit pour cet article.'),
    'Quantity is required.': _('La quantité est requise.'),
    'Quantity must be greater than zero.': _('La quantité doit être supérieure à zéro.'),
    'Unit price is required.': _('Le prix unitaire est requis.'),
    'Unit price cannot be negative.': _('Le prix unitaire ne peut pas être négatif.'),
    'Total price is required.': _('Le prix total est requis.'),
    'Total price cannot be negative.': _('Le prix total ne peut pas être négatif.'),
    'Total price must equal quantity times unit price.': _('Le prix total doit être égal à la quantité multipliée par le prix unitaire.'),
}


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['product', 'customer', 'rating', 'review_text', 'attributes', 'is_verified_purchase', 'is_public']
        labels = {
            'product': _('Product'),
            'customer': _('Customer'),
            'rating': _('Rating'),
            'review_text': _('Review Text'),
            'attributes': _('Attributes'),
            'is_verified_purchase': _('Verified Purchase'),
            'is_public': _('Public Review'),
        }
        error_messages = {
            'rating': {
                'required': _('Please provide a rating.'),
                'min_value': _('Rating must be at least 1.'),
                'max_value': _('Rating cannot exceed 5.'),
            },
            'review_text': {
                'required': _('Please provide a review text.'),
            },
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
            'attributes': forms.JSONInput(),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError(_('Rating must be between 1 and 5.'))
        return rating

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'select2'
        self.fields['customer'].widget.attrs['class'] = 'select2'
        self.fields['is_verified_purchase'].help_text = _('Check if this review is from a verified purchase.')
        self.fields['is_public'].help_text = _('If checked, this review will be visible to other customers.')

# Translations for French
_ = lambda s: s

fr_translations = {
    'Product': _('Produit'),
    'Customer': _('Client'),
    'Rating': _('Évaluation'),
    'Review Text': _('Texte de l\'avis'),
    'Attributes': _('Attributs'),
    'Verified Purchase': _('Achat vérifié'),
    'Public Review': _('Avis public'),
    'Please provide a rating.': _('Veuillez fournir une évaluation.'),
    'Rating must be at least 1.': _('L\'évaluation doit être d\'au moins 1.'),
    'Rating cannot exceed 5.': _('L\'évaluation ne peut pas dépasser 5.'),
    'Please provide a review text.': _('Veuillez fournir un texte d\'avis.'),
    'Rating must be between 1 and 5.': _('L\'évaluation doit être comprise entre 1 et 5.'),
    'Check if this review is from a verified purchase.': _('Cochez si cet avis provient d\'un achat vérifié.'),
    'If checked, this review will be visible to other customers.': _('Si coché, cet avis sera visible pour les autres clients.'),
}