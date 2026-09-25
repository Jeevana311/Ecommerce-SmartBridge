from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_remove_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("request_type", models.CharField(choices=[("Return", "Return"), ("Exchange", "Exchange")], max_length=10)),
                ("reason", models.CharField(max_length=200)),
                ("details", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("Requested", "Requested"), ("Approved", "Approved"), ("Rejected", "Rejected"), ("Completed", "Completed")], default="Requested", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="order_requests", to="store.order")),
                ("order_item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requests", to="store.orderitem")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="order_requests", to="auth.user")),
            ],
        ),
    ]