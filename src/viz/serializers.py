from rest_framework import serializers

from viz.models import Election


class WikidataHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
	def get_url(self, obj, view_name, request, format):
		"""
		Given an object, return the URL that hyperlinks to the object.
		May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
		attributes are not configured to correctly match the URL conf.
		"""
		if obj.wikidata_id:
			return 'https://www.wikidata.org/wiki/' + obj.wikidata_id

		return ''


class ElectionSerializer(serializers.ModelSerializer):
	wikidata_url = WikidataHyperlinkedIdentityField('wikidata_id')

	class Meta:
		model = Election
		fields = ('short_name','wikidata_id', 'wikidata_url')
