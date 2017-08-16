from django.db import models
#from django.contrib.gis.db import models


class Election(models.Model):
	id = models.AutoField(primary_key=True)
	full_name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=100)
	election_type = models.CharField(max_length=100) # presidential, national-council, state-council, municipal-council, mayor
	election_id = models.CharField(max_length=20, null=True) # from BMI
	wikidata_id = models.CharField(max_length=20, null=True)
	administrative_level = models.CharField(max_length=100) # municipality, district, state, nation
	election_day = models.DateTimeField('timestamp of election day') # yyyy-mm-dd
	is_final = models.BooleanField(default=False) # finally approved result for the whole election?

	def __str__(self):
		return "%s" % (self.short_name)

	class Meta:
		ordering = ('short_name',)

class RegionalElectoralDistrict(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, default=None)
	short_code = models.CharField(max_length=2)
	
	def __str__(self):
		return "%s" % (self.short_code)

	class Meta:
		ordering = ('short_code',)

class Party(models.Model):
	id = models.AutoField(primary_key=True)
	short_name = models.CharField(max_length=20)
	full_name = models.CharField(max_length=200)
	family = models.CharField(max_length=200, null=True, default=None) # parent party in european union
	wikidata_id = models.CharField(max_length=20, null=True, default=None)
	website = models.CharField(max_length=100, null=True, default=None) # official party website
	location = models.CharField(max_length=100, null=True, default=None) # austria, eu

	def __str__(self):
		return "%s" % (self.short_name)

	class Meta:
		ordering = ('short_name',)

class State(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	short_code = models.CharField(max_length=1, default=None)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		ordering = ('short_code',)

class District(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	short_code = models.CharField(max_length=2, default=None)
	state = models.ForeignKey(State, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		ordering = ('short_code',)

class Municipality(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	kennzahl = models.CharField(max_length=5, default=None)
	code = models.CharField(max_length=5, null=True, default=None)
	regional_electoral_district = models.ForeignKey(RegionalElectoralDistrict, on_delete=models.PROTECT, default=None)
	district = models.ForeignKey(District, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.code)

	class Meta:
		ordering = ('kennzahl',)

class PollingStation(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True, default=None)
	type = models.CharField(max_length=30) # municipal, absentee ballot, 
	municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		ordering = ('type',)

class PollingStationResult(models.Model):
	id = models.AutoField(primary_key=True)
	polling_station = models.ForeignKey(PollingStation, on_delete=models.PROTECT, default=None)
	election = models.ForeignKey(Election, on_delete=models.PROTECT, default=None)
	eligible_voters = models.IntegerField(null=True, default=-1)
	votes = models.IntegerField(default=-1)
	valid = models.IntegerField(default=-1)
	invalid = models.IntegerField(default=-1)
	ts_result = models.DateTimeField('timestamp of bmi result')
	is_final = models.BooleanField(default=False) # is it final approved result for the municipality?

	def __str__(self):
		return "%s %s" % (self.ts_result, self.polling_station)

	class Meta:
		ordering = ('ts_result', 'polling_station',)

class PartyResult(models.Model):
	id = models.AutoField(primary_key=True)
	polling_station_result = models.ForeignKey(PollingStationResult, on_delete=models.PROTECT)
	party = models.ForeignKey(Party, on_delete=models.PROTECT)
	votes = models.IntegerField(null=True, default=-1)

	def __str__(self):
		return "%s %s %s" % (self.polling_station_result, self.party, self.votes)

	class Meta:
		ordering = ('polling_station_result', 'party',)

class RawData(models.Model):
	id = models.AutoField(primary_key=True)
	ts_file = models.DateTimeField('creation date of original file', null=True)
	ts_import = models.DateTimeField('import date of file into database', default=None)
	hash = models.CharField(max_length=100)
	content = models.TextField()
	header = models.TextField(null=True, default=None)
	dataformat = models.CharField(max_length=50)
	election = models.ForeignKey(Election, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.ts_file)

	class Meta:
		ordering = ('ts_file',)

# class Candidate(models.Model):
# 	id = models.AutoField()
# 	first_name = models.CharField(max_length=100)
# 	family_name = models.CharField(max_length=100)
#	description = models.CharField(max_length=1000)
# 	wikidata_id = models.CharField(max_length=20)
# 	party = models.ForeignKey(Party, on_delete=models.CASCADE)
#	list = models.CharField(max_length=20)


