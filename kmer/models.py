""" Table models for kmers. """
from django.db import models


class FixedCharField(models.Field):
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(FixedCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length


class String(models.Model):
    """ Unique 31-mer strings stored as strings. """

    string = FixedCharField(max_length=31, unique=True)


class Binary(models.Model):

    """ Unique 31-mer strings stored as binary. """

    string = models.BinaryField(max_length=8, unique=True)
