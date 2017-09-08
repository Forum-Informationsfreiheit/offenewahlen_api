from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from viz.models import Election
from viz.serializers import ElectionSerializer


class ElectionInterface(viewsets.ReadOnlyModelViewSet):
	queryset = Election.objects.all()
	serializer_class = ElectionSerializer
