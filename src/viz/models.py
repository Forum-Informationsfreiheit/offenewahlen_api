from django.db import models

class Party(models.Model):
	id = models.AutoField(primary_key=True)
	party_id = models.CharField(max_length=20)
	wikidata_id = models.CharField(max_length=20)
	name = models.CharField(max_length=200)
	short = models.CharField(max_length=20)
	family = models.CharField(max_length=50)
	description = models.CharField(max_length=200)

	def __str__(self):
		return "%s" % (self.short)

	class Meta:
		ordering = ('short',)

class Municipality(models.Model):
	id = models.AutoField(primary_key=True)
	spatial_id = models.CharField(max_length=20, null=True, default=None)
	name = models.CharField(max_length=100)
	district = models.CharField(max_length=100)
	state = models.CharField(max_length=100)

	def __str__(self):
		return "%s %s" % (self.spatial_id, self.district)

	class Meta:
		ordering = ('spatial_id',)

class MunicipalityResult(models.Model):
	id = models.AutoField(primary_key=True)
	spatial_id = models.ForeignKey(Municipality,
		on_delete=models.PROTECT, null=True, default=None)
	eligible_voters = models.IntegerField(default=-1)
	votes = models.IntegerField(default=-1)
	valid = models.IntegerField(default=-1)
	invalid = models.IntegerField(default=-1)
	ts_result = models.DateTimeField('timestamp of bmi result')
	is_final = models.BooleanField()

	def __str__(self):
		return "%s %s" % (self.spatial_id, self.ts_result)

	class Meta:
		ordering = ('ts_result', 'spatial_id',)

class PartyResult(models.Model):
	id = models.AutoField(primary_key=True)
	municipality = models.ForeignKey(MunicipalityResult, on_delete=models.PROTECT)
	party = models.ForeignKey(Party, on_delete=models.PROTECT)
	votes = models.IntegerField(default=-1)

	def __str__(self):
		return "%s %s %s" % (self.municipality_result, self.party, self.votes)

	class Meta:
		ordering = ('municipality', 'party',)

class RawData(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField('creation date of BMI xml')
	hash = models.CharField(max_length=100)
	content = models.TextField()
	header = models.TextField()
	dataformat = models.CharField(max_length=10)

	def __str__(self):
		return "%s" % (self.timestamp)

	class Meta:
		ordering = ('timestamp',)

# class PollingStation(models.Model):
# 	id = models.AutoField()
# 	spatial_id = models.CharField(max_length=20)
# 	adress = models.CharField(max_length=200)
# 	city = models.CharField(max_length=100)
# 	post_code = models.CharField(max_length=10)
# 	lat
# 	lon
# 	contact = models.CharField(max_length=50)
# 	supervisor = models.CharField(max_length=100)

# class Candidate(models.Model):
# 	id = models.AutoField()
# 	first_name = models.CharField(max_length=100)
# 	family_name = models.CharField(max_length=100)
#	description = models.CharField(max_length=1000)
# 	wikidata_id = models.CharField(max_length=20)
# 	party = models.ForeignKey(Party, on_delete=models.CASCADE)
#	list = models.CharField(max_length=20)


