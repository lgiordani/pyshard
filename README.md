# pyshard: a simple sharding system in Python

The goal of this small project is to provide a simple implementation of a sharding system.

The requirements the final code shall provide are:

* The object `Comment(id = number, text = string)` will provide `save()` and `get_object_by_id(id=[number])` methods, which saves and retrieves the object from a storage system.
* Save objects in one of 4 tables (tables have the same structure and named like comment0, comment1, comment2, comment3) based on the object id (i.e. create a mapping function that maps each object to a given table). Populate the tables with random comments (in such a way that the tables are reasonably populated with approximately the same number of records).
* Add two new tables: comment4 and comment5 and create code to rebalance (move) the objects according to your mapping function (still ensuring the tables are reasonably populated with approximately the same number of records). Output the number of objects that have moved tables. Try to choose a mapping function that minimises the number of objects that have to be moved as part of the rebalancing step.

Such requirements may easily be matched by a consistent hashing system, so this will be the core of the project. 
 
 
 