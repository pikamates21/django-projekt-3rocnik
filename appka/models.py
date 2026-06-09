from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Customer(models.Model):
    GENDER_CHOICES = [
        ("male", "Muž"),
        ("female", "Žena"),
    ]

    customer_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    origin = models.CharField("Odkud je", max_length=100, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    reliable = models.BooleanField("Spolehlivý", default=False)

    def __str__(self):
        return f"{self.name} ({self.customer_id})"


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

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.FloatField()
    time_estimate = models.FloatField()  # hodiny
    work_time = models.FloatField()      # hodiny
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"