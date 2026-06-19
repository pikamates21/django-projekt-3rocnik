from django.shortcuts import render
from .models import Customer, Employee, Order
from django.db.models import Avg, Sum


def index(request):
    return render(request, "index.html")


def orders(request):
    orders = Order.objects.select_related("customer", "worker")
    return render(request, "orders.html", {"orders": orders})


def customers(request):
    customers = Customer.objects.all()

    data = []
    for c in customers:
        orders = c.order_set.all()
        data.append({
            "customer": c,
            "count": orders.count(),
            "total": sum(o.final_price for o in orders)
        })

    return render(request, "customers.html", {"data": data})


def customer_detail(request, pk):
    c = Customer.objects.filter(pk=pk).first()
    if not c:
        return render(request, "customers.html", {"data": []})

    orders = c.order_set.all()
    return render(request, "customer_detail.html", {
        "customer": c,
        "orders": orders,
        "order_count": orders.count(),
    })


def employees(request):
    employees = Employee.objects.all()
    return render(request, "employees.html", {"employees": employees})


def stats(request):
    orders = Order.objects.all()

    total_spent = orders.aggregate(total=Sum("final_price"))["total"] or 0
    avg_price = orders.aggregate(avg=Avg("final_price"))["avg"] or 0
    total_weight = orders.aggregate(total=Sum("weight"))["total"] or 0
    avg_weight = orders.aggregate(avg=Avg("weight"))["avg"] or 0
    total_orders = orders.count()

    frequent_customer = None
    frequent_count = 0
    frequent_total = 0
    frequent_weight = 0

    for c in Customer.objects.all():
        customer_orders = c.order_set.all()
        count = customer_orders.count()
        if count > frequent_count:
            frequent_count = count
            frequent_customer = c
            frequent_total = sum(o.final_price for o in customer_orders)
            frequent_weight = sum(o.weight for o in customer_orders)

    frequent_avg_weight = frequent_weight / frequent_count if frequent_count else 0

    return render(request, "stats.html", {
        "total_spent": total_spent,
        "avg_price": avg_price,
        "total_weight": total_weight,
        "avg_weight": avg_weight,
        "total_orders": total_orders,
        "frequent_customer": frequent_customer,
        "frequent_count": frequent_count,
        "frequent_total": frequent_total,
        "frequent_avg_weight": frequent_avg_weight,
    })