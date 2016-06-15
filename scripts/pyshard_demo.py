#!/user/bin/env python

from faker import Faker
from pyshard.repositories import memory_repo as mr

class Comment(object):
    repo = None

    def __init__(self, id, text):
        if self.repo is None:
            raise ValueError
        self.id = id
        self.text = text

    def save(self):
        self.repo.store(self.id, self.text)

    @classmethod
    def get_object_by_id(cls, id):
        value = cls.repo.load(id)
        return cls(id=id, text=value)

    @classmethod
    def set_repo(cls, repo):
        cls.repo = repo

initial_shards = 4
dataset_size = 1000

print("* Creating a repository with {} shards\n".format(initial_shards))
memory_repo = mr.MemoryRepo(shards=initial_shards, replicas=10)
Comment.set_repo(memory_repo)

print("* Generating a dataset with {} comments\n".format(dataset_size))
# This generates 1000 comments and stores them
fake = Faker()
for i in range(dataset_size):
    c = Comment(i, fake.text())
    c.save()

# This shows the status of the shards
print("* Show shards population\n")
Comment.repo.print_statistics()

# This adds two shards and performs balancing
migrated_keys = Comment.repo.add_shards(num=2)

# Prints the number of migrated keys
print("* {}/{} keys migrated to new_shards\n".format(migrated_keys, Comment.repo.num_keys))

# This shows the status of the shards after the migration
print("* Show shards population\n")
Comment.repo.print_statistics()

