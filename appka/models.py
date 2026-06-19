from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
import datetime


class Customer(models.Model):
    GENDER_CHOICES = [
        ("male", "Muž"),
        ("female", "Žena"),
    ]

    # use default automatic `id` field (AutoField) instead of manual customer_id
    name = models.CharField(max_length=100)
    origin = models.CharField("Odkud je", max_length=100, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    reliable = models.BooleanField("Spolehlivý", default=False)

    # additional independent info
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    registered_at = models.DateField(default=datetime.date.today)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                  validators=[MinValueValidator(0)])
    # photo: ImageField stored in MEDIA_ROOT/customers/
    photo = models.ImageField(upload_to='customers/', blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.id})"

    def order_count(self):
        return self.order_set.count()

    def photo_path(self):
        # keep helper for compatibility: use media URL when available
        try:
            return self.photo.url
        except Exception:
            return ""

    class Meta:
        verbose_name = "Zákazník"
        verbose_name_plural = "Zákazníci"
        ordering = ["name"]

    def clean(self):
        # enforce customer is at least 10 years old (birth_date <= today - 10 years)
        if self.birth_date:
            today = datetime.date.today()
            try:
                cutoff = today.replace(year=today.year - 10)
            except ValueError:
                # handle Feb 29 on leap years by falling back to Feb 28
                cutoff = today.replace(month=2, day=28, year=today.year - 10)

            if self.birth_date > cutoff:
                raise ValidationError({
                    'birth_date': 'Zákazník musí být starší alespoň 10 let.'
                })

        # require photo when creating a new customer
        if not self.photo:
            raise ValidationError({
                'photo': 'Musíte zadat fotku zákazníka.'
            })


class Employee(models.Model):
    GENDER_CHOICES = [
        ("male", "Muž"),
        ("female", "Žena"),
    ]

    employee_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    start_date = models.DateField()
    birth_date = models.DateField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    class Meta:
        verbose_name = "Pracovník"
        verbose_name_plural = "Pracovníci"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    description = models.TextField()

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2,
                                          validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    time_estimate = models.FloatField(validators=[MinValueValidator(0)])  # hodiny
    work_time = models.FloatField(validators=[MinValueValidator(0)])      # hodiny
    final_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

    class Meta:
        verbose_name = "Objednávka"
        verbose_name_plural = "Objednávky"