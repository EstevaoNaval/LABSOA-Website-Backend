from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from urllib.parse import urlparse

class Command(BaseCommand):
    help = "Creates a new site with the specified domain"

    def handle(self, *args, **options):
        domain = urlparse(settings.FRONTEND_URL).netloc
        site, _ = Site.objects.get_or_create(id=settings.SITE_ID)
        site.domain = domain
        site.name = domain
        site.save()
        self.stdout.write(self.style.SUCCESS(f'Site "{domain}" created successfully.'))