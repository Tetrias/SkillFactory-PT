from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


def category_list():
    category_list_str = ''
    for category in Category.objects.all():
        category_list_str += f'| ID:{category.id} - {category.name} '
    return category_list_str


class Command(BaseCommand):
    help = f'Команда для удаления всех постов в выбранной категории. Список категорий: {category_list()}'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all posts in this category? Y/n')
        answer = input()

        if answer == 'Y':
            category = Category.objects.get(pk=options['category_id'][0])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS('Successfully wiped posts!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))
