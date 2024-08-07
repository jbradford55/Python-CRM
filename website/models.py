"""from django.db import models

class Records(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")"""

from django.db import models

class Records(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    
    # New fields
    lead_source = models.CharField(max_length=100, null=True, blank=True)
    project_status = models.CharField(max_length=100, null=True, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    system_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sales_representative = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    incentives = models.TextField(null=True, blank=True)
    contract = models.FileField(upload_to='contracts/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('appointment', 'Appointment'),
        ('phone_call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ]

    record = models.ForeignKey(Records, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    outcome = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.get_interaction_type_display()} on {self.date.strftime('%Y-%m-%d %H:%M')} - {self.outcome}"



class SalesRep(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

