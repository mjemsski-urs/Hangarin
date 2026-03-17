from django.core.management.base import BaseCommand
from faker import Faker
from tasks.models import Task, SubTask, Note, Priority, Category
from django.utils import timezone

class Command(BaseCommand):
    help = "Create initial data for Hangarin"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Priorities
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        for p in priorities:
            Priority.objects.get_or_create(name=p)

        # Categories
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        for c in categories:
            Category.objects.get_or_create(name=c)

        # Tasks
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                category=Category.objects.order_by("?").first(),
                priority=Priority.objects.order_by("?").first(),
            )

            # Notes
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

            # SubTasks
            for _ in range(3):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                )

        self.stdout.write(self.style.SUCCESS("Initial data created successfully!"))
