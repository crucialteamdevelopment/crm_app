import os
import django

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Настройте Django
django.setup()

# Импортируйте модели
from users.models import CustomUser, LenderType

def fix_lender_type():
    # Заменяем пустые значения на NULL
    CustomUser.objects.filter(lender_type='').update(lender_type=None)
    print('Successfully fixed invalid lender_type values.')

if __name__ == '__main__':
    fix_lender_type()
