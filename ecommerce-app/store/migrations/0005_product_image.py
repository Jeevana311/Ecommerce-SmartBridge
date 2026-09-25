from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_orderrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]