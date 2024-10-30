from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from names.models import NameGroup, NameEntity
from names.serializers import NameGroupSerializer, NameEntitySerializer


class NameGroupViewSet(viewsets.ModelViewSet):
    """
    Return a list of all name groups with a list of containing name entities.

    DEV NOTES:
    According to the task directly - there are two endpoints requested, one for NameGroup creation only for
    authenticated users, and one for displaying list of NameGroup objects, authentication not mentioned. Possibly
    it would be good that other views are available for admins just in case.
    """
    queryset = NameGroup.objects.all()
    serializer_class = NameGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        elif self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


class NameEntityMoveView(APIView):
    """
    "Move" entity to another name group.

    De facto update name group for entity specified in URL.
    """
    serializer_class = NameEntitySerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            name_entity = NameEntity.objects.get(pk=pk)
        except NameEntity.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(name_entity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
