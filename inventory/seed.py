from faker import Faker
from inventory.models import Vendor, Brand, Category, SubCategory

fake = Faker()

def data(n):
    
    vendors = [Vendor(vendor_name=fake.company()) for _ in range(n)]
    Vendor.objects.bulk_create(vendors)

    brands = [Brand(brand_name=fake.word(), vendor=vendor) for vendor in Vendor.objects.all()]
    Brand.objects.bulk_create(brands)

    categories = [Category(category_name=fake.word(), brand=brand) for brand in Brand.objects.all()]
    Category.objects.bulk_create(categories)

    subcategories = [SubCategory(sub_category_name=fake.word(), category=category) for category in Category.objects.all()]
    SubCategory.objects.bulk_create(subcategories)
        

