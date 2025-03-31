import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
django.setup()
pytest.main()
