from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    description = models.TextField()

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.FloatField()
    time_estimate = models.FloatField()  # hodiny
    work_time = models.FloatField()      # hodiny
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"