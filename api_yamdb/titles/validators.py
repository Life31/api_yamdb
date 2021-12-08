from django.core.validators import MaxValueValidator
from datetime import datetime


def max_value_this_year(value):
    return MaxValueValidator(
        datetime.now().year,
        'Нельзя добавить с такой датой.'
    )
