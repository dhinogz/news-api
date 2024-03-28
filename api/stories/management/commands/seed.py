from stories.models import Story
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
from django.core.management.base import BaseCommand

from config import settings

""" Clear all data and creates stories """
MODE_REFRESH = "refresh"

""" Clear all data and do not create any object """
MODE_CLEAR = "clear"


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write("seeding data...")
        run_seed(self, options["mode"])
        self.stdout.write("done.")


def clear_data():
    """Deletes all the table data"""
    User.objects.all().delete()
    Story.objects.all().delete()


def run_seed(self, mode):
    """Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Dummy data for seeding
    headlines = ["Breaking News!", "Local Events Update",
                 "Weather Forecast", "Community Announcement", "Sports Update"]
    details = [
        "New breakthrough in artificial intelligence research.",
        "Recent developments in parliamentary negotiations.",
        "Art exhibition showcasing local talent.",
        "Did you know? The world's largest pizza was made in Italy.",
        "Rain expected in the region tomorrow. Stay prepared!"
    ]
    categories = ["tech", "politics", "art", "trivia"]
    regions = ["eu", "uk", "w"]
    first_names = ["John", "Juan", "David",
                   "Daniel", "Jose", "Bryan", "Thomas"]
    last_names = ["Smith", "Hernandez",
                  "Martinez", "Hart", "Finn", "Rodriguez"]

    User.objects.create_superuser(
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        email=settings.ADMIN_EMAIL,
        first_name="Super",
        last_name="User",
    )
    User.objects.create_superuser(
        username=settings.PROFESSOR_USERNAME,
        password=settings.PROFESSOR_PASSWORD,
        email=settings.PROFESSOR_EMAIL,
        first_name=settings.PROFESSOR_FIRST_NAME,
        last_name=settings.PROFESSOR_LAST_NAME,
    )
    for _ in range(10):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        random_num = random.randint(10, 100)
        User.objects.create_user(
            username=f"{first_name}-{last_name}{random_num}",
            email=f"{first_name}.{last_name}{random_num}@test.com",
            password=f"pretty{first_name}random",
            first_name=first_name,
            last_name=last_name,
        )

    authors = User.objects.all()
    for _ in range(20):
        headline = random.choice(headlines)
        detail = random.choice(details)
        category = random.choice(categories)
        region = random.choice(regions)
        author = random.choice(authors)
        date = datetime.now() - timedelta(days=random.randint(1, 30))

        story = Story.objects.create(
            headline=headline,
            details=detail,
            category=category,
            region=region,
            author=author,
            date=date,
        )
        story.save()
