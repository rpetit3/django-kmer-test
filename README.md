Work In Progress

# django-kmer-test
Compare two methods for storing DNA *k*-mers in a database. DNA *k*-mers are DNA sequences of length *k*. For example:

    # k = 1
    A, T, G, C
    
    # k = 10
    ATGCATGCAT
    
    # k = 31
    ATGCATGCATATGCATGCATATGCATGCATA

#### Installation 

    git clone git@github.com:rpetit3/django-kmer-test.git
    cd django-kmer-test
    
    # Install Python Packages
    sudo pip install -r requirements.txt
    
    # Create User and Database (Assume PostgreSQL is setup)
    sudo -u postgres bash -c "psql -c \"CREATE USER kmer WITH PASSWORD 'kmer';\""
    sudo -u postgres bash -c "psql -c \"CREATE DATABASE kmer;\""
    sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE kmer to kmer;\""
    
    # Run test
    python manage insert_kmers
    
    # Wait ...

#### For documentation later
[bitarray](https://pypi.python.org/pypi/bitarray)

[2-bit format](http://jcomeau.freeshell.org/www/genome/2bitformat.html)

[model 2-bit encoding](https://djangosnippets.org/snippets/1597/)
