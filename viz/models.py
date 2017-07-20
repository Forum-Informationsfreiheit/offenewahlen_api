from django.db import models

class Election(models.Model):
	id = models.AutoField(primary_key=True)
	eligible_voters = models.IntegerField(default=-1)
	votes = models.IntegerField(default=-1)
	valid = models.IntegerField(default=-1)
	invalid = models.IntegerField(default=-1)
	spatial_id = models.CharField(max_length=20)
	ts_result = models.DateTimeField('timestamp of bmi result')
	ts_storage = models.DateTimeField('timestamp of database storage')
	spoe = models.IntegerField(default=-1)
	fpoe = models.IntegerField(default=-1)
	oevp = models.IntegerField(default=-1)
	neos = models.IntegerField(default=-1)
	gruene = models.IntegerField(default=-1)
	kpoe = models.IntegerField(default=-1)
	is_final = models.BooleanField()

class RawData(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField('creation date of BMI xml')
	hash = models.CharField(max_length=100)
	content = models.TextField()
	header = models.TextField()

# class Party(models.Model):
# 	id = models.AutoField()
# 	party_id = models.CharField(max_length=20)
# 	wikidata_id = models.CharField(max_length=20)
# 	name = models.CharField(max_length=200)
# 	short = models.CharField(max_length=20)
# 	family = models.CharField(max_length=50)
#	description = models.CharField(max_length=200)

# class Candidate(models.Model):
# 	id = models.AutoField()
# 	first_name = models.CharField(max_length=100)
# 	family_name = models.CharField(max_length=100)
#	description = models.CharField(max_length=1000)
# 	wikidata_id = models.CharField(max_length=20)
# 	party = models.ForeignKey(Party, on_delete=models.CASCADE)
#	list = models.CharField(max_length=20)

# class Municipality(models.Model):
# 	name = models.CharField(max_length=100)
# 	district = models.CharField(max_length=100)
# 	state = models.CharField(max_length=100)

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



