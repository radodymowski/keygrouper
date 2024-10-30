import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from names.models import NameGroup, NameEntity


@pytest.fixture
def client_with_token(db):
    user = User.objects.create_user(username="testuser", password="123123123")
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")
    return client


@pytest.mark.django_db
class TestNameGroupViewSet:
    def test_list(self):
        # given
        group_1 = NameGroup.objects.create(name="name1")
        group_2 = NameGroup.objects.create(name="name2")
        entity_1 = NameEntity.objects.create(name_group=group_1, name="name1_1")
        entity_2 = NameEntity.objects.create(name_group=group_1, name="name1_2")

        client = APIClient()
        url = reverse("namegroup-list")

        # when
        response = client.get(url)

        # then
        expected_group_data_1 = {"id": 1, "name": "name1", "entities": ["name1_1", "name1_2"]}
        expected_group_data_2 = {"id": 2, "name": "name2", "entities": []}
        assert response.status_code == status.HTTP_200_OK
        assert expected_group_data_1 in response.data["results"]
        assert expected_group_data_2 in response.data["results"]

    def test_create__valid(self, client_with_token):
        # given
        data = {"name": "name_333"}

        url = reverse("namegroup-list")

        # when
        response = client_with_token.post(url, data, format="json")

        # then
        assert response.status_code == status.HTTP_201_CREATED
        assert NameGroup.objects.count() == 1
        assert NameGroup.objects.first().name == "name_333"

    def test_create__not_authenticated(self):
        # given
        data = {"name": "name_333"}

        client = APIClient()
        url = reverse("namegroup-list")

        # when
        response = client.post(url, data, format="json")

        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert NameGroup.objects.count() == 0

    def test_create__invalid_data(self, client_with_token):
        # given
        data = {"name": True}

        url = reverse("namegroup-list")

        # when
        response = client_with_token.post(url, data, format="json")

        # then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert NameGroup.objects.count() == 0


    def test__only_for_admin(self, client_with_token):
        # given
        url = reverse("namegroup-detail", args=[1])

        # when
        response = client_with_token.get(url)

        # then
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {"detail": "You do not have permission to perform this action."}


@pytest.mark.django_db
class TestNameEntityMoveView:
    @pytest.fixture
    def load_data(self, db):
        group_1 = NameGroup.objects.create(name="name1")
        group_2 = NameGroup.objects.create(name="name2")
        entity = NameEntity.objects.create(name_group=group_1, name="name1_1")
        return group_1, group_2, entity

    def test_put__valid(self, client_with_token, load_data):
        # given
        group_1, group_2, entity = load_data
        data = {"name_group": group_2.pk}
        url = reverse("nameentity-move", args=[entity.pk])

        # when
        response = client_with_token.put(url, data=data, format="json")

        # then
        assert response.status_code == status.HTTP_200_OK
        entity.refresh_from_db()
        assert entity.name_group.pk == group_2.pk

    def test_put__not_authenticated(self, load_data):
        # given
        group_1, group_2, entity = load_data
        data = {"name_group": group_2.pk}
        url = reverse("nameentity-move", args=[entity.pk])
        client = APIClient()

        # when
        response = client.put(url, data=data, format="json")

        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put__not_found(self, client_with_token, load_data):
        group_1, group_2, entity = load_data
        data = {"name_group": group_2.pk}
        url = reverse("nameentity-move", args=[entity.pk + 9999])

        # when
        response = client_with_token.put(url, data=data, format="json")

        # then
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {"detail": "Not found"}

    def test_put__name_group_not_found(self, client_with_token, load_data):
        group_1, group_2, entity = load_data
        invalid_id = group_2.pk + 9999
        data = {"name_group": invalid_id}
        url = reverse("nameentity-move", args=[entity.pk])

        # when
        response = client_with_token.put(url, data=data, format="json")

        # then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name_group"][0].code == "does_not_exist"

    def test_put__invalid_payload(self, client_with_token, load_data):
        group_1, group_2, entity = load_data
        data = {"wrong_key": "nonsense"}
        url = reverse("nameentity-move", args=[entity.pk])

        # when
        response = client_with_token.put(url, data=data, format="json")

        # then
        assert response.status_code == status.HTTP_200_OK
        entity.refresh_from_db()
        assert entity.name_group.pk == group_1.pk
