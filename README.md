# pyshard: a simple sharding system in Python

The goal of this small project is to provide a simple implementation of a sharding system.

The requirements the final code shall provide are:

* The object `Comment(id = number, text = string)` will provide `save()` and `get_object_by_id(id=[number])` methods, which saves and retrieves the object from a storage system.
* Save objects in one of 4 tables (tables have the same structure and named like comment0, comment1, comment2, comment3) based on the object id (i.e. create a mapping function that maps each object to a given table). Populate the tables with random comments (in such a way that the tables are reasonably populated with approximately the same number of records).
* Add two new tables: comment4 and comment5 and create code to rebalance (move) the objects according to your mapping function (still ensuring the tables are reasonably populated with approximately the same number of records). Output the number of objects that have moved tables. Try to choose a mapping function that minimises the number of objects that have to be moved as part of the rebalancing step.

# Installation

* Clone the repository https://github.com/lgiordani/pyshard
* Create a virtualenv and run `pip install -r requirements.txt`
* Run `pip install .`
* Run `pyshard_demo`

to run tests

* Run `pip install -r requirements/testing.txt`
* Run `py.test -sv`

WARNING: being this a demo project not every component of the system has been isolated, so tests are a bit slow.

The `pyshard_demo` script creates a new `Comment` class according to the requirements and fills the storage with 1000 objects, showing the shards population. After that, two new shards are created and the new balanced population is shown.

# General analysis

Such requirements may easily be matched by a consistent hashing system, so this will be the core of the project. The implementation of the storage system is not the focus of the project, so a very simple in-memory storage will be implemented. This is a repository according to the clean architecture design, so any other implementation shall implement the same API. 
 
With such a low number of shard a high number of replicas is required to uniformly cover the [0,1) interval. The default number of replicas in this implementation is 1000, but may be tweaked when instantiating the `MemoryRepo` object. Using a lower number of replicas (for example 10) the shards show the obvious unbalance given by the uneven distribution of bins. 
 
# Hash values distribution

The objects in the storage system have a numerical id. A brief analysis of the quality of an MD5-based hash function can be performed with the following code  
 
``` python
import bisect
import hashlib


def _normalize_number(num, boundary):
    # Normalizes between 0 and 1
    return float(num % boundary) / boundary


def hash_key(key, method, boundary):
    hash_function = getattr(hashlib, method)
    hashed_key_base10 = int(hash_function(str(key).encode()).hexdigest(), 16)

    return _normalize_number(hashed_key_base10, boundary)

num_bins = 4
num_data = 4000

hashes = [hash_key(i, 'md5', 1e7) for i in range(num_data)]
bins = [i / num_bins for i in range(num_bins)]
positions = [bisect.bisect_left(bins, i) for i in hashes]
count = []

for i in range(num_bins):
    count.append(positions.count(i + 1))

norm = sum(count)
norm_pop = [int(i * 100 / norm) for i in count]
for idx, i in enumerate(norm_pop):
    print("{} {} {}".format(idx, ''.join(['x' for i in range(i)]), i))
```

The repository code is not limited to MD5 functions, and a different function of the `hashlib` library may be used setting the `method parameter of the `MemoryRepo` object.

# Implementation details

The code implements a simple consistent hashing system without optimizations.

When a shard is added the system performs an automatic rebalancing of the shards. The system keeps track of the bins created during the shard addition and checks only keys belonging to the new bins.
 
More than a shard may be added with a call of `add_shards()`, but the rebalancing will be performed after each shard addition.
