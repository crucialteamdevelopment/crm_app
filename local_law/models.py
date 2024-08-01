from django.db import models

class LocalLaw(models.Model):
    official_ll_name = models.CharField(max_length=255)
    ll_nickname = models.CharField(max_length=255)
    how_often = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        # Добавьте другие статусы по мере необходимости
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    standard_penalty = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_penalty = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField()  # Если только 4 цифры
    floor = models.CharField(max_length=255, blank=True)  # Если это не обязательно

    government_link = models.URLField()

class LocalLawField(models.Model):
    local_law = models.ForeignKey(LocalLaw, related_name='additional_fields', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class LocalLawDates(models.Model):
    local_law = models.ForeignKey(LocalLaw, related_name='dates', on_delete=models.CASCADE, blank=True, null=True)
    due_date = models.DateTimeField()
    service_date = models.DateTimeField()

class LocalLawContacts(models.Model):
    local_law = models.ForeignKey(LocalLaw, related_name='contacts', on_delete=models.CASCADE, blank=True, null=True)
    building_contact = models.CharField(max_length=255, blank=True)
    respondent = models.CharField(max_length=255, blank=True)
    other = models.CharField(max_length=255, blank=True)

class LocalLawNote(models.Model):
    local_law = models.ForeignKey(LocalLaw, related_name='notes', on_delete=models.CASCADE, blank=True, null=True)
    local = models.TextField(blank=True)
    shared = models.TextField(blank=True)
