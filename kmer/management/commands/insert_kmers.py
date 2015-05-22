""" Insert Jellyfish output into the database. """
import time
import random
import sys
from bitarray import bitarray

from optparse import make_option

from django.db import connection, transaction
from django.core.management.base import BaseCommand

from kmer.models import Kmer, KmerString, KmerBinary


class Command(BaseCommand):
    help = 'Insert Kmer data into the database.'

    option_list = BaseCommand.option_list + (
        make_option('--empty', dest='empty', action='store_true',
                    help='Empty each of the tables'),
    )

    @transaction.atomic
    def handle(self, *args, **opts):
        self.test_results = {}
        tests = [
            10 ** 1,
            10 ** 2,
            10 ** 3,
            10 ** 4,
            10 ** 5,
            10 ** 6,
            10 ** 7,
            10 ** 8,
            10 ** 9,
        ]
        for test in tests:
            self.run_test(test)

        columns = [
            'Test',
            'KmerString INSERT',
            'KmerBinary INSERT',
            'KmerString Size',
            'KmerBinary Size',
            'KmerString SELECT',
            'KmerString SELECT queries',
            'KmerBinary SELECT',
            'KmerBinary SELECT queries',
        ]

        fh = open('kmer_anlaysis.out', 'w')
        fh.write('{0}\n'.format('\t'.join(columns)))
        for test in tests:
            string = []
            for column in columns:
                string.append(str(self.test_results[test][column]))
            fh.write('{0}\n'.format('\t'.join(string)))
        fh.close()

    def run_test(self, total_kmers):
        print "Running test with {0} kmers.".format(total_kmers)
        self.test_results[total_kmers] = {'Test': total_kmers}

        # Empty Tables
        print "Emptying tables..."
        self.empty_tables()

        # Generate kmers
        kmers = {}
        print 'Generating {0} kmers...'.format(total_kmers)
        while len(kmers) < total_kmers:
            kmers[''.join(random.choice('ATGC') for _ in range(31))] = 1

        # Prep insert
        print "Prepping inserts..."
        kmer_string = []
        kmer_binary = []
        for key in kmers:
            kmer_string.append(KmerString(string=key))
            kmer_binary.append(KmerBinary(string=key))

        # Insert KmerString, KmerBinaryString, KmerBinary
        print "Inserting kmer strings..."
        insert_time = self.insert_kmers(kmer_string, 'KmerString')
        self.test_results[total_kmers]['KmerString INSERT'] = insert_time

        print "Inserting bit encoded kmers..."
        insert_time = self.insert_kmers(kmer_binary, 'KmerBinary')
        self.test_results[total_kmers]['KmerBinary INSERT'] = insert_time

        self.test_results[total_kmers]['KmerString Size'] = self.get_table_size('kmer_kmerstring')[0]
        self.test_results[total_kmers]['KmerBinary Size'] = self.get_table_size('kmer_kmerbinary')[0]

        print 'Testing lookup speed...'
        total = min(int(total_kmers * 0.2), 2000)
        subsample = random.sample(kmers.keys(), total)
        runtime = self.test_select(subsample, 'KmerString')
        self.test_results[total_kmers]['KmerString SELECT'] = runtime / total
        self.test_results[total_kmers]['KmerString SELECT queries'] = total

        runtime = self.test_select(subsample, 'KmerBinary')
        self.test_results[total_kmers]['KmerBinary SELECT'] = runtime / total
        self.test_results[total_kmers]['KmerBinary SELECT queries'] = total

        return None

    @transaction.atomic
    def insert_kmers(self, kmers, table):
        start_time = time.time()
        print table
        if table == 'KmerString':
            KmerString.objects.bulk_create(kmers, batch_size=1000)
        elif table == 'KmerBinary':
            KmerBinary.objects.bulk_create(kmers, batch_size=1000)

        return time.time() - start_time

    def test_select(self, kmers, table):
        start_time = time.time()
        for kmer in kmers:
            if table == 'KmerString':
                KmerString.objects.get(string=kmer)
            elif table == 'KmerBinary':
                _code = {
                    'A': bitarray('01'),
                    'C': bitarray('11'),
                    'G': bitarray('00'),
                    'T': bitarray('10')
                }
                a = bitarray()
                a.encode(_code, kmer)
                KmerBinary.objects.get(_string=a.tobytes())._string

        return float(time.time() - start_time)

    def get_table_size(self, table):
        cursor = connection.cursor()
        cursor.execute("SELECT pg_size_pretty(pg_relation_size('{0}'));".format(table))
        row = cursor.fetchone()

        return row

    @transaction.atomic
    def empty_tables(self):
        KmerString.objects.all().delete()
        KmerBinary.objects.all().delete()
        Kmer.objects.all().delete()
