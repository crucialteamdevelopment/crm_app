from django.db import models

class Violation(models.Model):
    violation_number = models.CharField(max_length=255)
    issuing_agency = models.CharField(max_length=255)
    agency_violation_number = models.CharField(max_length=255)
    issued_to = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    standard_penalty = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_penalty = models.DecimalField(max_digits=10, decimal_places=2)
    face_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    court_decision = models.CharField(max_length=255)
    government_link = models.URLField()

class Field(models.Model):
    violation = models.ForeignKey(Violation, related_name='additional_fields', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
