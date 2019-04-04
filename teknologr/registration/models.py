from django.db import models


class LimboMember(models.Model):
    # NAMES
    surname = models.CharField(max_length=100)
    given_names = models.CharField(max_length=64)
    preferred_name = models.CharField(max_length=32)
    # ADDRESS
    street_address = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    # CONTACT INFO
    phone = models.CharField(max_length=128)
    email = models.EmailField(max_length=64)
    # DATE OF BIRTH
    birth_date = models.DateField()
    # STUDIES
    student_id = models.CharField(max_length=10)
    school = models.CharField(max_length=100, default="")
    degree_programme = models.CharField(max_length=256)
    enrolment_year = models.IntegerField()
    # MEMBERSHIP MOTIVATION
    motivation = models.TextField(max_length=2048, default="")
    # CONSENTS
    subscribed_to_modulen = models.BooleanField(default=False)
    allow_publish_info = models.BooleanField(default=False)
