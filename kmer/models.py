""" Table models for kmers. """
from django.db import models


class Kmer(models.Model):

    """ A linking table for Sample and Kmers. """

    version = models.TextField(default='1.0', db_index=True)


class KmerString(models.Model):

    """ Unique 31-mer strings stored as strings. """

    string = models.CharField(max_length=31, unique=True, db_index=True)


class KmerBinary(models.Model):

    """ Unique 31-mer strings stored as binary. """

    string = models.BinaryField(max_length=8, unique=True, db_index=True)

'''
Ignore for now

class KmerCount(models.Model):

    """ Kmer counts from each sample. """

    kmer = models.ForeignKey('Kmer', on_delete=models.CASCADE)
    string = models.ForeignKey('KmerString', on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('kmer', 'string')


class KmerTotal(models.Model):

    """ Total kmer counts from each sample. """

    kmer = models.ForeignKey('Kmer', on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
'''
