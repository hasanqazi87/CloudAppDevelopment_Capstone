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


class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, _id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = _id

    def __str__(self):
        return f'{self.car_year} {self.car_make} {self.car_model}'