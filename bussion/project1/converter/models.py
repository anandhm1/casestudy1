from django.db import models

class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    currency_name = models.CharField(max_length=10)
    file1 = models.FileField(upload_to="file")
    def __str__(self):
        return self.name

class MoneyConverter(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=10)
    amount = models.FloatField()
    Date = models.CharField(max_length=100)
    converted_currency = models.CharField(max_length=10)
    converted_amount = models.FloatField()



