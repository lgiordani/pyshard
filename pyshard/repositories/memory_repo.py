from pyshard import hash_functions as hf
import bisect

class MemoryRepo(object):
    def __init__(self, shards=1, replicas=10):
        self._num_replicas = replicas

        self._shards = []

        # Each shard tuple is made by (shard_idx, replica_hash)
        self._shard_tuples = []

        self.add_shards(shards)

    @property
    def num_shards(self):
        return len(self._shards)

    def _hash_key(self, key):
        return hf.hash_key(key, 'md5', 1e7)

    def _key_to_shard_idx(self, key):
        # This hashes the key, maps it to a replica and then to a shard
        hashed_key = self._hash_key(key)
        hashed_labels = [i[1] for i in self._shard_tuples]

        hashed_labels_idx = bisect.bisect_left(hashed_labels, hashed_key)

        # bisect has been designed for insert() so the index may be higher that the last one
        if hashed_labels_idx > len(self._shard_tuples) - 1:
            hashed_labels_idx = 0

        return self._shard_tuples[hashed_labels_idx][0]

    def add_shards(self, num):
        for i in range(num):
            self._shards.append({})

            # This computes the hash of each replica label
            for replica_num in range(self._num_replicas):
                replica_label = "shard{}/{}".format(len(self._shards), replica_num)
                hashed_replica_label = self._hash_key(replica_label)
                self._shard_tuples.append((i, hashed_replica_label))

            self._shard_tuples = sorted(self._shard_tuples, key=lambda x: x[1])

    def store(self, key, value):
        idx = self._key_to_shard_idx(key)
        self._shards[idx][key] = value

    def load(self, key):
        idx = self._key_to_shard_idx(key)
        return self._shards[idx][key]

    def get_shards_population(self):
        return [len(sh) for sh in self._shards]

    def print_statistics(self):
        shards_population = self.get_shards_population()
        norm = sum(shards_population)
        norm_pop = [int(i*100/norm) for i in shards_population]
        for idx, i in enumerate(norm_pop):
            print("{} {}".format(idx, ''.join(['x' for i in range(i)])))


