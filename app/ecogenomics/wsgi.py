"""
WSGI config for EcoGenomics Suite project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecogenomics.settings')

application = get_wsgi_application()