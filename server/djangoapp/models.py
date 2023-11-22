from django.db import models
from django.utils.timezone import now


CAR_TYPES = [
    ('SEDAN', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'Wagon'),
    ('COUPE', 'Coupe'),
    ('COMPACT', 'Compact'),
]


class CarMake(models.Model):
    name = models.CharField(max_length=30, null=False, default='Car make name')
    description = models.CharField(max_length=100)
    origin = models.CharField(max_length=30, default='USA')

    def __str__(self):
        return f'<CarMake {self.name}>'


class CarModel(models.Model):
    car_make = models.ForeignKey('CarMake', on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=30, null=False, default='Car model name')
    car_type = models.CharField(choices=CAR_TYPES, null=False, default='SEDAN', max_length=30)
    year = models.DateField()
    engine = models.CharField(max_length=30)

    def __str__(self):
        return f'<CarModel {self.year.year} {self.car_make.name} {self.name}>'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
