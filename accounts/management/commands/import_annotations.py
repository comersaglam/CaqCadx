import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from labeling.models import ImageItem


#! old py to import annotations, now replaced by update_annotations.py

class Command(BaseCommand):
    help = "Import image metadata from dataset/db_annotations.csv into ImageItem table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            default="dataset/db_annotations.csv",
            help="Path to db_annotations.csv (default: dataset/db_annotations.csv)",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv"])
        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        created, skipped = 0, 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj, is_created = ImageItem.objects.get_or_create(
                    path=row["path"],
                    defaults={
                        "polyp_pos_xywh": row.get("polyp_pos_xywh"),
                        "size": row.get("size"),
                        "pathology_diagnosis": row.get("pathology_diagnosis"),
                        "is_polyp": bool(int(row.get("is_polyp", 1))),  # default = 1
                        "is_cut":   bool(int(row.get("is_cut", 0))),    # default = 0
                        "localization_label": int(row.get("localization_label", -1)),
                        "size_label": int(row.get("size_label", -1)),
                        "cleanliness_label": int(row.get("cleanliness_label", -1)),
                        "overall": int(row.get("overall", -1)),
                        "colonexpansion_label": int(row.get("colonexpansion_label", -1)),
                        "img_cleanliness": int(row.get("img_cleanliness", -1)),
                        "img_overall": int(row.get("img_overall", -1)),
                        "annotator_mail": row.get("annotator_mail", "none"),
                    },
                )
                if is_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created} new ImageItem(s), skipped {skipped} already existing."
        ))
