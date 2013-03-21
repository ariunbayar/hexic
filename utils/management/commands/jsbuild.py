import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    SOURCE = 'coffee/*.coffee'
    DESTINATION = 'static/js/packed.js'
    help = 'Builds %s into %s' % (SOURCE, DESTINATION)

    def handle(self, *args, **options):
        self.stdout.write(
            'Building %s to %s\n' % (self.SOURCE, self.DESTINATION))

        command = 'coffee --join %s --compile %s\n'\
                  % (self.DESTINATION, self.SOURCE)
        self.stdout.write(' > %s' % command)
        os.system(command)
