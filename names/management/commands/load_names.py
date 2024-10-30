import csv

from django.core.management.base import BaseCommand

from names.serializers import NameGroupSerializer
from names.services import group_names


class Command(BaseCommand):
    help = "Group name entities given in .csv file by their prefixes, optionally save it to database"

    def add_arguments(self, parser):
        parser.add_argument("--save", action="store_true", help="Save results to database")

    def handle(self, *args, **options):
        with open("names.csv", newline="") as names_file:
            reader = csv.reader(names_file, delimiter=" ")
            names = [row[0] for row in reader if row]

        name_groups_dict = group_names(names, delimiter="_")
        if options["save"]:
            for name_group_key in name_groups_dict.keys():
                serializer = NameGroupSerializer(data={
                    "name": name_group_key,
                    "entities_keys": name_groups_dict[name_group_key]
                })
                if serializer.is_valid():
                    serializer.create(validated_data=serializer.validated_data)
        else:
            print(name_groups_dict)
