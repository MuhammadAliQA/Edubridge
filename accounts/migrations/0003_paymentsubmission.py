
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_enrollment_yonalish_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name="Summa (so'm)")),
                ('method', models.CharField(choices=[('card', 'Karta'), ('payme', 'Payme'), ('click', 'Click'), ('cash', 'Naqd'), ('other', 'Boshqa')], default='card', max_length=20)),
                ('payer_name', models.CharField(blank=True, max_length=120, verbose_name="To'lov qiluvchi (ixtiyoriy)")),
                ('payer_phone', models.CharField(blank=True, max_length=50, verbose_name='Telefon (ixtiyoriy)')),
                ('transaction_ref', models.CharField(blank=True, max_length=120, verbose_name='Tranzaksiya ID (ixtiyoriy)')),
                ('note', models.TextField(blank=True, verbose_name='Izoh (ixtiyoriy)')),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('approved', 'Tasdiqlandi'), ('rejected', 'Rad etildi')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_submissions', to='accounts.enrollment', verbose_name='Yozilish')),
            ],
            options={
                'verbose_name': "To'lov arizasi",
                'verbose_name_plural': "To'lov arizalari",
                'ordering': ['-created_at'],
            },
        ),
    ]
