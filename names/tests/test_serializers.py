import pytest

from names.models import NameGroup, NameEntity
from names.serializers import NameGroupSerializer, NameEntitySerializer


@pytest.mark.django_db
class TestNameGroupSerializer:
    def test_serialize(self):
        # given
        name_group = NameGroup.objects.create(name="name")
        NameEntity.objects.create(name_group=name_group, name="name_1")
        NameEntity.objects.create(name_group=name_group, name="name_2")

        # when
        serializer = NameGroupSerializer(name_group)

        # then
        expected_data = {
            "id": name_group.pk,
            "name": "name",
            "entities": ["name_1", "name_2"]
        }
        assert serializer.data["id"] == expected_data["id"]
        assert serializer.data["name"] == expected_data["name"]
        assert list(serializer.data["entities"]) == expected_data["entities"]

    def test_create__valid(self):
        # given
        data = {
            "name": "name",
        }
        serializer = NameGroupSerializer(data=data)

        # when
        assert serializer.is_valid()
        name_group = serializer.save()

        # then
        assert name_group.name == "name"
        assert name_group.names.count() == 0

    def test_create__missing_name(self):
        # given
        data = {}
        serializer = NameGroupSerializer(data=data)

        # when / then
        assert not serializer.is_valid()
        assert "name" in serializer.errors


@pytest.mark.django_db
class TestNameEntitySerializer:
    def test_serialize(self):
        # given
        name_group = NameGroup.objects.create(name="name")
        name_entity = NameEntity.objects.create(name_group=name_group, name="name1")

        # when
        serializer = NameEntitySerializer(name_entity)

        # then
        assert serializer.data["id"] == name_entity.id
        assert serializer.data["name"] == "name1"
