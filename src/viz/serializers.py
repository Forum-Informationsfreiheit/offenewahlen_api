# from rest_framework import serializers
#
# from viz import models
#
#
# class WikidataHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
# 	def get_url(self, obj, view_name, request, format):
# 		"""
# 		Given an object, return the URL that hyperlinks to the object.
# 		May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
# 		attributes are not configured to correctly match the URL conf.
# 		"""
# 		if obj.wikidata_id:
# 			return 'https://www.wikidata.org/wiki/' + obj.wikidata_id
#
# 		return ''
#
#
# class ElectionSerializer(serializers.ModelSerializer):
# 	wikidata_url = WikidataHyperlinkedIdentityField('wikidata_id')
#
# 	class Meta:
# 		model = models.Election
# 		fields = ('short_name', 'wikidata_id', 'wikidata_url')
#
#
# class StateSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = models.State
# 		fields = ('name',)
#
#
# class DistrictSerializer(serializers.ModelSerializer):
# 	state = StateSerializer()
#
# 	class Meta:
# 		model = models.District
# 		fields = ('short_code', 'name', 'state')
#
#
# class MunicipalitySerializer(serializers.ModelSerializer):
# 	district = DistrictSerializer()
#
# 	class Meta:
# 		model = models.Municipality
# 		fields = ('name', 'code', 'kennzahl',
# 			'regional_electoral_district', 'district')
#
#
# class PartySerializer(serializers.ModelSerializer):
# 	wikidata_url = WikidataHyperlinkedIdentityField('wikidata_id')
#
# 	class Meta:
# 		model = models.Party
# 		fields = ('short_name', 'short_name_text', 'full_name',
# 			'family', 'wikidata_id', 'wikidata_url', 'website')
#
#
# class PollingStationSerializer(serializers.ModelSerializer):
# 	municipality = MunicipalitySerializer()
#
# 	class Meta:
# 		model = models.PollingStation
# 		fields = ('name', 'type', 'municipality')
#
#
# class PollingStationResultSerializer(serializers.ModelSerializer):
# 	polling_station = PollingStationSerializer()
# 	election = ElectionSerializer()
#
# 	class Meta:
# 		model = models.PollingStationResult
# 		fields = ('election', 'polling_station', 'election',
# 			'eligible_voters', 'votes', 'valid', 'invalid',
# 			'ts_result', 'is_final')
#
#
# class ListSerializer(serializers.ModelSerializer):
# 	party = PartySerializer()
#
# 	class Meta:
# 		model = models.List
# 		fields = ('short_name', 'short_name_text', 'full_name', 'party')
#
#
# #class GeomSerializer(serializers.ModelSerializer):
#
# 	#class Meta:
# 		#content = JSONRenderer().render(serializer.data)
# 		#fields = ('short_name', 'short_name_text', 'full_name', 'party')
#
# class RegionalElectoralDistrictSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = models.RegionalElectoralDistrict
# 		fields = ('short_code', 'name')
