""" Insert Jellyfish output into the database. """
import itertools
import time

from bitarray import bitarray

from django.db import connection, transaction
from django.core.management.base import BaseCommand

from kmer.models import String, Binary


class Command(BaseCommand):
    help = 'Insert random Kmer data into the database.'

    _code = {
        'A': bitarray('01'),
        'C': bitarray('11'),
        'G': bitarray('00'),
        'T': bitarray('10')
    }

    _tables = [
        'kmer_binary',
        'kmer_string'
    ]

    def add_arguments(self, parser):
        parser.add_argument('--k', type=int, dest='k', default=31,
                            help='Length of k to test.')
        parser.add_argument('--rows', type=int, dest='rows', default=10 ** 11,
                            help='Total number of rows to insert.')

    def handle(self, *args, **opts):
        self.test_results = {}
        self.totals = []

        # Empty Tables
        self.empty_tables()

        # Init variables
        total = 0
        self.kmers = []
        self.kmer_string = []
        self.kmer_binary = []

        # Generate kmers
        progress_time = time.time()
        print 'Kmers:String:Binary:kmers/second'
        for p in itertools.product(['A', 'T', 'G', 'C'], repeat=opts['k']):
            if total % (opts['rows'] / 100000) == 0 and total > 0:
                # Insert Kmers
                self.insert_kmers('String')
                self.insert_kmers('Binary')
                self.kmer_string = []
                self.kmer_binary = []

                # Get table sizes
                progress_time = float(time.time() - progress_time)
                rate = int((opts['rows'] / 100000) / progress_time)
                self.table_size(total, rate)
                progress_time = time.time()

            if total == opts['rows']:
                break

            kmer = ''.join(p)
            self.kmer_string.append(String(string=kmer))
            self.kmer_binary.append(Binary(string=self.encode(kmer)))
            total += 1

    def encode(self, seq):
        a = bitarray()
        a.encode(self._code, seq)
        return a.tobytes()

    @transaction.atomic
    def insert_kmers(self, table):
        if table == 'String':
            String.objects.bulk_create(self.kmer_string, batch_size=10000)
        elif table == 'Binary':
            Binary.objects.bulk_create(self.kmer_binary, batch_size=10000)

    def table_size(self, total, rate):
        # Get KmerString table size
        print '{0}:{1}:{2}:{3}'.format(
            total,
            self.get_table_size('kmer_string')[0],
            self.get_table_size('kmer_binary')[0],
            rate
        )

    def get_table_size(self, table):
        cursor = connection.cursor()
        cursor.execute("SELECT pg_total_relation_size('{0}');".format(table))
        row = cursor.fetchone()

        return row

    @transaction.atomic
    def empty_tables(self):
        # Empty Tables and Reset id counters to 1
        for table in self._tables:
            self.empty_table(table)

    def empty_table(self, table):
        query = "TRUNCATE TABLE {0} RESTART IDENTITY CASCADE;".format(table)
        cursor = connection.cursor()
        cursor.execute(query)
