""" Table models for analysis results. """
from bitarray import bitarray
from django.db import models


class Kmer(models.Model):

    """ A linking table for Sample and Kmers. """

    version = models.TextField(default='1.0', db_index=True)


class KmerString(models.Model):

    """ Unique 31-mer strings stored as strings. """

    string = models.CharField(max_length=31, unique=True, db_index=True)


class KmerBinary(models.Model):

    """ Unique 31-mer strings stored as binary. """

    _string = models.BinaryField(max_length=8, unique=True,
                                 db_index=True, db_column='string')

    _code = {
        'A': bitarray('01'),
        'C': bitarray('11'),
        'G': bitarray('00'),
        'T': bitarray('10')
    }

    def set_string(self, string):
        a = bitarray()
        a.encode(self._code, string)
        self._string = a.tobytes()

    def get_string(self):
        a = bitarray()
        a.frombytes(self._string)
        return a.decode(self._code)[0:31]

    string = property(get_string, set_string)

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
