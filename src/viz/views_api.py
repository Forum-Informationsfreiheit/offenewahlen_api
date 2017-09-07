from rest_framework import generics

from viz.models import Election
from viz.serializers import ElectionSerializer


class ElectionInterface(generics.ListCreateAPIView):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
