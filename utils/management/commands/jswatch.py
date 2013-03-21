import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    SOURCE = 'coffee/*.coffee'
    DESTINATION = 'static/js/packed.js'
    help = 'Watches and builds %s into %s' % (SOURCE, DESTINATION)

    def handle(self, *args, **options):
        self.stdout.write('Watching changes for %s\n' % self.SOURCE)

        command = 'coffee --watch --join %s --compile %s\n'\
                  % (self.DESTINATION, self.SOURCE)
        self.stdout.write(' > %s' % command)
        os.system(command)
