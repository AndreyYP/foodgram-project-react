import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file',
                            type=str,
                            help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            ingredients_data = json.load(json_file)

        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_data['name'],
                measurement_unit=ingredient_data['measurement_unit']
            )

            self.stdout.write(self.style.SUCCESS(
                'Successfully imported ingredients.')
            )
