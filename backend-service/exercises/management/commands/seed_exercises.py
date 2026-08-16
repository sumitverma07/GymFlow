import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from categories.models import Category
from exercises.models import  Exercise
from exercise_images.models import ExerciseImage


IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "yuhonas/free-exercise-db/main/exercises/"
)


MUSCLE_MAPPING = {
    # Chest
    "chest": {
        "body_part": "CHEST",
        "primary_muscle": "CHEST",
    },

    # Back
    "lats": {
        "body_part": "BACK",
        "primary_muscle": "LATS",
    },
    "middle back": {
        "body_part": "BACK",
        "primary_muscle": "MIDDLE_BACK",
    },
    "lower back": {
        "body_part": "BACK",
        "primary_muscle": "LOWER_BACK",
    },
    "traps": {
        "body_part": "BACK",
        "primary_muscle": "TRAPS",
    },

    # Arms
    "biceps": {
        "body_part": "ARMS",
        "primary_muscle": "BICEPS",
    },
    "triceps": {
        "body_part": "ARMS",
        "primary_muscle": "TRICEPS",
    },
    "forearms": {
        "body_part": "ARMS",
        "primary_muscle": "FOREARMS",
    },

    # Legs
    "quadriceps": {
        "body_part": "LEGS",
        "primary_muscle": "QUADRICEPS",
    },
    "hamstrings": {
        "body_part": "LEGS",
        "primary_muscle": "HAMSTRINGS",
    },
    "glutes": {
        "body_part": "LEGS",
        "primary_muscle": "GLUTES",
    },
    "calves": {
        "body_part": "LEGS",
        "primary_muscle": "CALVES",
    },
    "abductors": {
        "body_part": "LEGS",
        "primary_muscle": "ABDUCTORS",
    },
    "adductors": {
        "body_part": "LEGS",
        "primary_muscle": "ADDUCTORS",
    },

    # Shoulders
    "shoulders": {
        "body_part": "SHOULDERS",
        "primary_muscle": "SHOULDERS",
    },

    # Core
    "abdominals": {
        "body_part": "CORE",
        "primary_muscle": "ABDOMINALS",
    },

    # Neck
    "neck": {
        "body_part": "NECK",
        "primary_muscle": "NECK",
    },
}


class Command(BaseCommand):

    help = "Seed exercises and exercise images from exercises.json"

    @transaction.atomic
    def handle(self, *args, **options):

        # --------------------------------------------------
        # Locate exercises.json
        # --------------------------------------------------

        file_path = (
            Path(__file__).resolve().parents[3]
            / "data"
            / "exercises.json"
        )

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"File not found: {file_path}"
                )
            )
            return

        self.stdout.write(
            f"Reading exercises from: {file_path}"
        )

        # --------------------------------------------------
        # Load JSON
        # --------------------------------------------------

        with open(file_path, "r", encoding="utf-8") as file:
            exercises_data = json.load(file)

        exercises_created = 0
        exercises_existing = 0
        exercises_skipped = 0
        images_created = 0

        # --------------------------------------------------
        # Process exercises
        # --------------------------------------------------

        for item in exercises_data:

            name = item.get("name")
            category_name = item.get("category")
            primary_muscles = item.get("primaryMuscles", [])
            instructions = item.get("instructions", [])
            images = item.get("images", [])

            # ----------------------------------------------
            # Validate exercise name
            # ----------------------------------------------

            if not name:
                exercises_skipped += 1

                self.stdout.write(
                    self.style.WARNING(
                        "Skipping exercise without a name."
                    )
                )

                continue

            # ----------------------------------------------
            # Validate primary muscle
            # ----------------------------------------------

            if not primary_muscles:

                exercises_skipped += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping '{name}': "
                        "no primary muscle found."
                    )
                )

                continue

            primary_muscle_name = (
                primary_muscles[0].strip().lower()
            )

            muscle_data = MUSCLE_MAPPING.get(
                primary_muscle_name
            )

            # ----------------------------------------------
            # Make sure our mapping supports the dataset
            # ----------------------------------------------

            if not muscle_data:

                exercises_skipped += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping '{name}': "
                        f"unknown primary muscle "
                        f"'{primary_muscle_name}'."
                    )
                )

                continue

            # ----------------------------------------------
            # Category
            # ----------------------------------------------

            category = None

            if category_name:

                category, _ = Category.objects.get_or_create(
                    name=category_name
                )

            # ----------------------------------------------
            # Instructions
            # ----------------------------------------------

            instructions_text = "\n".join(
                instructions
            )

            # ----------------------------------------------
            # Create / get Exercise
            # ----------------------------------------------

            exercise, created = (
                Exercise.objects.get_or_create(
                    name=name,
                    defaults={
                        "category": category,
                        "body_part": muscle_data["body_part"],
                        "primary_muscle": (
                            muscle_data["primary_muscle"]
                        ),
                        "instructions": instructions_text,
                    },
                )
            )

            if created:

                exercises_created += 1

            else:

                exercises_existing += 1

            # ----------------------------------------------
            # Create Exercise Images
            # ----------------------------------------------

            for image_path in images:

                image_url = (
                    f"{IMAGE_BASE_URL}{image_path}"
                )

                _, image_created = (
                    ExerciseImage.objects.get_or_create(
                        exercise=exercise,
                        image_url=image_url,
                    )
                )

                if image_created:
                    images_created += 1

        # --------------------------------------------------
        # Final output
        # --------------------------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Exercise seeding completed successfully!"
            )
        )

        self.stdout.write(
            f"Exercises created : {exercises_created}"
        )

        self.stdout.write(
            f"Exercises existing: {exercises_existing}"
        )

        self.stdout.write(
            f"Exercises skipped : {exercises_skipped}"
        )
        print('ok')

        self.stdout.write(
            f"Images created    : {images_created}"
        )