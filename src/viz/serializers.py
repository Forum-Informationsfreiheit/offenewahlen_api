from rest_framework import serializers

from viz.models import Election


class ElectionSerializer(serializers.Serializer):
	class Meta:
		model = Election
		fields = ('short_name',)
