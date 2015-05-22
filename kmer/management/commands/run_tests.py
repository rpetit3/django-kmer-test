""" Insert Jellyfish output into the database. """
import time
import itertools
import random

from bitarray import bitarray

from django.db import connection, transaction
from django.core.management.base import BaseCommand

from kmer.models import KmerString, KmerBinary


class Command(BaseCommand):
    help = 'Insert Kmer data into the database.'

    _code = {
        'A': bitarray('01'),
        'C': bitarray('11'),
        'G': bitarray('00'),
        'T': bitarray('10')
    }

    _columns = ['kmers', 'KmerString INSERT', 'KmerBinary INSERT',
                'KmerString Size', 'KmerBinary Size', 'KmerString SELECT',
                'KmerBinary SELECT', 'SELECT queries']

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
        print self.print_columns()
        for p in itertools.product(['A', 'T', 'G', 'C'], repeat=opts['k']):
            if total % 100000 == 0 and total > 0:
                self.totals.append(total)
                self.test_results[total] = {'kmers': total}

                # Insert Kmers
                self.insert(total)

                # Get table sizes
                self.table_size(total)

                # Test Select times
                self.select(total)

                # Print progress
                print self.print_progress(total)

                if total == opts['rows']:
                    break

            kmer = ''.join(p)
            # Use ~5% of kmers to test select times
            if random.random() <= 0.05:
                self.kmers.append(kmer)
            self.kmer_string.append(KmerString(string=kmer))
            self.kmer_binary.append(KmerBinary(string=self.encode(kmer)))
            total += 1

        self.output_results()

    def encode(self, seq):
        a = bitarray()
        a.encode(self._code, seq)
        return a.tobytes()

    def insert(self, total):
        # Insert kmer strings
        time = self.insert_kmers('KmerString')
        self.test_results[total]['KmerString INSERT'] = "{0:.7f}".format(time)

        # Insert bit encoded kmers
        time = self.insert_kmers('KmerBinary')
        self.test_results[total]['KmerBinary INSERT'] = "{0:.7f}".format(time)

        # Reset kmer lists
        self.kmer_string = []
        self.kmer_binary = []

        return None

    @transaction.atomic
    def insert_kmers(self, table):
        start_time = time.time()
        if table == 'KmerString':
            KmerString.objects.bulk_create(self.kmer_string, batch_size=1000)
        elif table == 'KmerBinary':
            KmerBinary.objects.bulk_create(self.kmer_binary, batch_size=1000)

        return (time.time() - start_time) / len(self.kmer_binary)

    def table_size(self, total):
        # Get KmerString table size
        size = self.get_table_size('kmer_kmerstring')[0]
        self.test_results[total]['KmerString Size'] = size

        # Get KmerBinary table size
        size = self.get_table_size('kmer_kmerbinary')[0]
        self.test_results[total]['KmerBinary Size'] = size

        return None

    def get_table_size(self, table):
        cursor = connection.cursor()
        cursor.execute("SELECT pg_relation_size('{0}');".format(table))
        row = cursor.fetchone()

        return row

    def select(self, total):
        # select kmer strings
        time = self.test_select('KmerString')
        self.test_results[total]['KmerString SELECT'] = "{0:.7f}".format(time)

        # select bit encoded kmers
        time = self.test_select('KmerBinary')
        self.test_results[total]['KmerBinary SELECT'] = "{0:.7f}".format(time)

        # Reset kmer list
        self.test_results[total]['SELECT queries'] = len(self.kmers)
        self.kmers = []

        return None

    def test_select(self, table):
        start_time = time.time()
        for kmer in self.kmers:
            if table == 'KmerString':
                KmerString.objects.get(string=kmer)
            elif table == 'KmerBinary':
                KmerBinary.objects.get(string=self.encode(kmer))

        return float(time.time() - start_time) / len(self.kmers)

    @transaction.atomic
    def empty_tables(self):
        KmerString.objects.all().delete()
        KmerBinary.objects.all().delete()

    def print_columns(self):
        return '\t'.join(self._columns)

    def print_progress(self, total):
        string = []
        for column in self._columns:
            string.append(str(self.test_results[total][column]))

        return '\t'.join(string)

    def output_results(self):
        fh = open("run_tests.txt", "w")
        fh.write("{0}\n".format(self.print_columns()))
        for total in self.totals:
            string = []
            for column in self._columns:
                string.append(str(self.test_results[total][column]))

            fh.write("{0}\n".format('\t'.join(string)))
        fh.close()

        return None
