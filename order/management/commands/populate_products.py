import csv
import os
from django.core.management.base import BaseCommand
from order.models import Product

class Command(BaseCommand):
    help = 'Populate products from a CSV file'

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.NOTICE('Products already exist. Skipping population.'))
            return
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file = os.path.join(base_dir, 'commands','products.csv')

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product.objects.create(
                    #id=row['id'],
                    name=row['name'],
                    category=row['category'],
                    description=row['description'],
                    size=row['size'],
                    image=row['image'],
                    amount=row['amount'],
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('Products populated successfully.'))
