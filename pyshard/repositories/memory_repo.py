import bisect
from pyshard import hash_functions as hf


class MemoryRepo(object):
    def __init__(self, shards=1, replicas=1000, method='md5'):
        # This is the number of replicas for each shard
        self._num_replicas = replicas
        self._hashing_method = method

        self._shards = []

        # Each is made by (replica_hash, shard_idx)
        # Every item with an hash greater than replica_hash goes here
        # (if it does not fall into the next bin)
        # The two bins are there to provide a boundary when computing
        # ranges for new bins
        self._bins = [(0, 0), (2, 0)]

        self.add_shards(shards, balance=False)

    @property
    def num_shards(self):
        return len(self._shards)

    @property
    def num_keys(self):
        return sum(self.get_shards_population())

    def _hash_key(self, key):
        return hf.hash_key(key, self._hashing_method, 1e7)

    def _get_hashed_labels(self):
        return [i[0] for i in self._bins]

    def _key_to_shard_idx(self, key):
        # This hashes the key, maps it to a replica and then to a shard
        hashed_key = self._hash_key(key)
        hashed_labels = self._get_hashed_labels()

        hashed_key_idx = bisect.bisect_left(hashed_labels, hashed_key)

        # bisect has been designed for insert() so the index may be higher that the last one
        if hashed_key_idx > len(self._bins) - 1:
            hashed_key_idx = 0

        # Return the shard index for this bin
        return self._bins[hashed_key_idx][1]

    def _add_shard(self):
        self._shards.append({})
        shard_index = len(self._shards) - 1
        shard_label = "shard{}".format(shard_index)

        new_bins = []

        # Compute the label of each replica
        # Each label is then hashed and the relative bin is computed
        for replica_num in range(self._num_replicas):
            replica_label = "{}/replica{}".format(shard_label, replica_num)
            replica_hash = self._hash_key(replica_label)
            replica_bin = (replica_hash, shard_index)
            self._bins.append(replica_bin)
            new_bins.append(replica_bin)

        self._bins = sorted(self._bins, key=lambda x: x[0])

        # Now that bins are ordered find the new ones and return the ranges
        bin_ranges = []
        for new_bin in new_bins:
            # It could have been removed in the optimization phase
            if new_bin in self._bins:
                # Compute index
                bin_idx = self._bins.index(new_bin)

                # Find the first bin that refers to a different shard (i.e. the original shard)
                original_shards = [bin[1] for bin in self._bins[bin_idx:] if bin[1] != new_bin[1]] + [None]
                original_shard = original_shards[0]

                # bin_range is (lower_hash, higher_hash, original_shard)
                # original_shard is where the key is located at the moment
                # lower_hash shall be excluded, higher_hash included
                bin_range = (self._bins[bin_idx - 1], new_bin, original_shard)

                bin_ranges.append(bin_range)

        return bin_ranges

    def add_shards(self, num, balance=True):
        total_number_of_migrated_keys = 0

        for shard_idx in range(num):
            bin_ranges = self._add_shard()

            if not balance:
                continue

            for previous_bin, new_bin, original_shard in bin_ranges:
                src_shard = self._shards[original_shard]
                dst_shard = self._shards[new_bin[1]]

                balanced_keys = []
                for key in src_shard:
                    hashed_key = self._hash_key(key)
                    if previous_bin[0] < hashed_key <= new_bin[0]:
                        balanced_keys.append(key)

                for balanced_key in balanced_keys:
                    dst_shard[balanced_key] = src_shard.pop(balanced_key)

                total_number_of_migrated_keys += len(balanced_keys)

        return total_number_of_migrated_keys

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

        # Normalize the shards population
        norm = sum(shards_population)
        norm_pop = [int(i * 100 / norm) for i in shards_population]

        # Pretty print it
        for idx, i in enumerate(norm_pop):
            print("{} ({}%) {}".format(idx, str(i).zfill(2), ''.join(['x' for i in range(i)])))
        print()
