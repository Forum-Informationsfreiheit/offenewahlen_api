from django.db import models

class ElectionManager(models.Manager):
	def get_by_natural_key(self, full_name):
	    return self.get(full_name=full_name)

class Election(models.Model):
	objects = ElectionManager()

	short_name = models.CharField(primary_key=True, max_length=50)
	short_name_text = models.CharField(max_length=50, null=True)
	full_name = models.CharField(max_length=200)
	election_type = models.CharField(max_length=100) # presidential, national-council, state-council, municipal-council, mayor
	election_id = models.CharField(max_length=20, null=True) # from BMI
	wikidata_id = models.CharField(max_length=20, null=True, unique=True)
	administrative_level = models.CharField(max_length=100) # municipality, district, state, nation
	election_day = models.DateTimeField('timestamp of election day') # yyyy-mm-dd
	state = models.CharField(max_length=200, null=False, default='init')

	def __str__(self):
		return "%s" % (self.short_name)

	class Meta:
		ordering = ['short_name']
		get_latest_by = 'election_day'
		verbose_name = 'election'
		verbose_name_plural = 'elections'
		indexes = [
			models.Index(fields=['full_name', 'short_name']),
		]

	def natural_key(self):
		return (self.full_name)

class RegionalElectoralDistrict(models.Model):
	short_code = models.CharField(primary_key=True, max_length=2)
	name = models.CharField(max_length=100, default=None)
	
	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		ordering = ['short_code']
		verbose_name = 'regional electoral district'
		verbose_name_plural = 'regional electoral districts'
		indexes = [
			models.Index(fields=['name', 'short_code']),
		]


class Party(models.Model):
	short_name = models.CharField(primary_key=True, max_length=50)
	short_name_text = models.CharField(max_length=50, unique=True, default=None)
	full_name = models.CharField(max_length=200, unique=True)
	family = models.CharField(max_length=200, null=True, default=None) # parent party in european union
	wikidata_id = models.CharField(max_length=20, null=True, default=None, unique=True)
	website = models.CharField(max_length=100, null=True, default=None) # official party website
	location = models.CharField(max_length=100, null=True, default=None) # austria, eu

	def __str__(self):
		return "%s" % (self.short_name)

	class Meta:
		ordering = ['short_name']
		verbose_name = 'party'
		verbose_name_plural = 'parties'
		indexes = [
			models.Index(fields=['full_name', 'short_name', 'short_name_text']),
		]

class List(models.Model):
	short_name = models.CharField(primary_key=True, max_length=50)
	short_name_text = models.CharField(max_length=50, default=None)
	full_name = models.CharField(max_length=200, default=None)
	party = models.ForeignKey(Party, on_delete=models.PROTECT, null=True, default=None)

	def __str__(self):
		return "%s" % (self.short_name)

	class Meta:
		ordering = ['short_name']
		verbose_name = 'list'
		verbose_name_plural = 'lists'
		indexes = [
			models.Index(fields=['short_name', 'full_name', 'short_name_text']),
		]


class State(models.Model):
	short_code = models.CharField(primary_key=True, max_length=1)
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		ordering = ['short_code']
		verbose_name = 'state'
		verbose_name_plural = 'states'
		indexes = [
			models.Index(fields=['name']),
		]

class District(models.Model):
	short_code = models.CharField(primary_key=True, max_length=3)
	name = models.CharField(max_length=100, unique=True)
	state = models.ForeignKey(State, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (str(self.name))

	class Meta:
		ordering = ['short_code']
		verbose_name = 'district'
		verbose_name_plural = 'districts'
		indexes = [
			models.Index(fields=['name']),
		]

class MunicipalityManager(models.Manager):
	def get_by_natural_key(self, code):
	    return self.get(code=code)

class Municipality(models.Model):
	objects = MunicipalityManager()

	code = models.CharField(primary_key=True, max_length=5)
	name = models.CharField(max_length=200)
	kennzahl = models.CharField(max_length=5, default=None)
	regional_electoral_district = models.ForeignKey(RegionalElectoralDistrict, on_delete=models.PROTECT, default=None)
	district = models.ForeignKey(District, on_delete=models.PROTECT, default=None)


	def __str__(self):
		return "%s" % (self.code, self.name)

	class Meta:
		ordering = ['code']
		verbose_name = 'municipality'
		verbose_name_plural = 'municipalities'
		indexes = [
			models.Index(fields=['name', 'code']),
		]

	def natural_key(self):
		return (self.code)

class PollingStationManager(models.Manager):
	def get_by_natural_key(self, name):
	    return self.get(name=name)

class PollingStation(models.Model):
	objects = PollingStationManager()

	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True, default=None)
	type = models.CharField(max_length=30) # municipal, absentee ballot, 
	municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		order_with_respect_to = 'municipality'
		verbose_name = 'polling station'
		verbose_name_plural = 'polling stations'
		indexes = [
			models.Index(fields=['name']),
		]

	def natural_key(self):
		return (self.name)

class PollingStationResultManager(models.Manager):
	def get_by_natural_key(self, polling_station, election):
	    return self.get(polling_station=polling_station, election=election)

class PollingStationResult(models.Model):
	objects = PollingStationResultManager()

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
		return "%s" % (self.ts_result)

	class Meta:
		ordering = ['ts_result']
		get_latest_by = 'ts_result'
		verbose_name = 'polling station result'
		verbose_name_plural = 'polling station results'

	def natural_key(self):
		return (self.polling_station, self.election)

class ListResult(models.Model):
	id = models.AutoField(primary_key=True)
	polling_station_result = models.ForeignKey(PollingStationResult, on_delete=models.PROTECT)
	election_list = models.ForeignKey(List, on_delete=models.PROTECT)
	votes = models.IntegerField(null=True, default=-1)

	def __str__(self):
		return "%s %s %s" % (self.votes, self.polling_station_result, self.party)

	class Meta:
		ordering = ['id']
		verbose_name = 'party result'
		verbose_name_plural = 'party results'

class RawData(models.Model):
	id = models.AutoField(primary_key=True)
	ts_file = models.DateTimeField('creation date of original file', null=True)
	ts_import = models.DateTimeField('import date of file into database', default=None)
	hash = models.CharField(max_length=100)
	content = models.TextField()
	header = models.TextField(null=True, default=None)
	dataformat = models.CharField(max_length=50)
	description = models.TextField(default=None)
	election = models.ForeignKey(Election, on_delete=models.PROTECT, default=None)

	def __str__(self):
		return "%s" % (self.ts_import)

	class Meta:
		ordering = ['ts_import']
		get_latest_by = 'ts_file'
		verbose_name = 'raw data'
		verbose_name_plural = 'raw data'

# class Candidate(models.Model):
# 	id = models.AutoField()
# 	first_name = models.CharField(max_length=100)
# 	last_name = models.CharField(max_length=100)
#	description = models.CharField(max_length=1000)
# 	wikidata_id = models.CharField(max_length=20)
# 	party = models.ForeignKey(Party, on_delete=models.CASCADE)
#	list = models.CharField(max_length=20)
#
#	@property
#    def full_name(self):
#        "Returns the candidate's full name."
#        return '%s %s' % (self.first_name, self.last_name)


