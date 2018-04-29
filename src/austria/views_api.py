from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from austria import models
from austria import serializers


class ElectionInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.Election.objects.all()
	serializer_class = serializers.ElectionSerializer


class PollingStationResultInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.PollingStationResult.objects.all()
	serializer_class = serializers.PollingStationResultSerializer


class DistrictInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.District.objects.all()
	serializer_class = serializers.DistrictSerializer


class MunicipalityInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.Municipality.objects.all()
	serializer_class = serializers.MunicipalitySerializer


class PartyInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.Party.objects.all()
	serializer_class = serializers.PartySerializer


class PollingStationInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.PollingStation.objects.all()
	serializer_class = serializers.PollingStationSerializer


class ListInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.List.objects.all()
	serializer_class = serializers.ListSerializer


class RegionalElectoralDistrictInterface(viewsets.ReadOnlyModelViewSet):
	queryset = models.RegionalElectoralDistrict.objects.all()
	serializer_class = serializers.RegionalElectoralDistrictSerializer
