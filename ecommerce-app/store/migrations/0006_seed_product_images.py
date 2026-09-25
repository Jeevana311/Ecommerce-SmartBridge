from django.db import migrations


PRODUCT_IMAGES = {
    "Laptop": "products/laptop.svg",
    "Wireless Headphones": "products/wireless-headphones.svg",
    "Casual Cotton T-Shirt": "products/casual-cotton-t-shirt.svg",
    "Denim Jacket": "products/denim-jacket.svg",
    "The Power of Habit": "products/the-power-of-habit.svg",
    "Python Programming Basics": "products/python-programming-basics.svg",
    "Leather Wallet": "products/leather-wallet.svg",
    "Sunglassess": "products/sunglassess.svg",
    "Electric Kettle": "products/electric-kettle.svg",
    "Ceramic Coffee Mug": "products/ceramic-coffee-mug.svg",
}


def assign_product_images(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    for name, image_path in PRODUCT_IMAGES.items():
        Product.objects.filter(name=name, image__isnull=True).update(image=image_path)
        Product.objects.filter(name=name, image="").update(image=image_path)


def clear_product_images(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Product.objects.filter(image__in=PRODUCT_IMAGES.values()).update(image=None)


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_product_image"),
    ]

    operations = [
        migrations.RunPython(assign_product_images, clear_product_images),
    ]