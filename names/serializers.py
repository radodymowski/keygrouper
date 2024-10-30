from rest_framework import serializers

from names.models import NameEntity, NameGroup


class NameEntitySerializer(serializers.ModelSerializer):
    name_group = serializers.PrimaryKeyRelatedField(queryset=NameGroup.objects.all())
    class Meta:
        model = NameEntity
        fields = ["id", "name", "name_group"]


class NameGroupSerializer(serializers.ModelSerializer):
    entities = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NameGroup
        fields = ["id", "name", "entities"]

    def get_entities(self, obj) -> list[str]:
        return list(obj.names.values_list("name", flat=True))
