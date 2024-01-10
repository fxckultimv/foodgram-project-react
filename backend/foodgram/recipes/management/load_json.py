import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Download ingredients to database'

    def add_arguments(self, parser):
        parser.add_argument(
            'path', type=str, help='Select download file location'
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        try:
            with open(path, encoding='utf-8') as file:
                data = json.load(file)
                obj = 0
                for i in data:
                    name = i['name']
                    measurement_unit = i['measurement_unit']
                    try:
                        print(name, measurement_unit)
                        ingredient, created = Ingredient.objects.get_or_create(
                            name=name,
                            measurement_unit=measurement_unit,
                        )
                        if created:
                            ingredient.save()
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Ингредиент {name} успешно сохранен.'
                                )
                            )
                            obj += 1
                        else:
                            self.stderr.write(
                                self.style.NOTICE(
                                    f'Ингредиент {name} уже существует.'
                                )
                            )
                    except Exception as error:
                        self.stderr.write(self.style.WARNING(f'{error}'))
                        raise Exception(error)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Были успешно загружены {obj} ингредиентов из {len(data)}.'
                    )
                )
        except FileNotFoundError as error:
            self.stderr.write(self.style.WARNING(f'{error}'))