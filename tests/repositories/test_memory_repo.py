from pyshard.repositories import memory_repo as mr


def test_store_key_value():
    repo = mr.MemoryRepo()
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_init_accepts_number_of_shards():
    repo = mr.MemoryRepo(shards=4)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_init_accepts_the_hashing_method():
    repo = mr.MemoryRepo(shards=4, method='sha256')
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"

def test_init_accepts_number_of_replicas():
    repo = mr.MemoryRepo(replicas=2)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_init_accepts_both_number_of_shards_and_replicas():
    repo = mr.MemoryRepo(shards=4, replicas=2)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_repo_knows_the_numer_of_shards():
    repo = mr.MemoryRepo(shards=4)
    assert repo.num_shards == 4

def test_repo_knows_the_numer_of_keys():
    repo = mr.MemoryRepo(shards=4)
    for i in range(50):
        repo.store(i, "avalue")

    assert repo.num_keys == 50

def test_repo_can_add_shard_when_empty():
    repo = mr.MemoryRepo(shards=4)
    repo.add_shards(num=1)
    assert repo.num_shards == 5


def test_repo_can_add_shard_without_balancing():
    repo = mr.MemoryRepo(shards=4)
    repo.add_shards(num=1, balance=False)
    assert repo.num_shards == 5


def test_get_shards_population():
    repo = mr.MemoryRepo(shards=4)

    assert repo.get_shards_population() == [0, 0, 0, 0]


def test_storing_key_value_populates_a_single_shard():
    repo = mr.MemoryRepo(shards=4)
    repo.store("akey", "avalue")

    assert repo.get_shards_population().count(1) == 1


def test_massive_population_is_balanced():
    repo = mr.MemoryRepo(shards=4)
    for i in range(1000):
        repo.store(i, "avalue")

    shards_population = repo.get_shards_population()
    total_population = sum(shards_population)

    assert all([i < total_population / (repo.num_shards - 1) for i in shards_population])
    assert all([i > 0 for i in shards_population])


def test_adding_shard_without_balancing_works():
    repo = mr.MemoryRepo(shards=4)
    for i in range(1000):
        repo.store(i, "avalue")

    repo.add_shards(num=1, balance=False)
    assert 0 in repo.get_shards_population()


def test_massive_population_after_shard_addition_is_balanced():
    repo = mr.MemoryRepo(shards=4)
    for i in range(1000):
        repo.store(i, "avalue")

    migrated_keys = repo.add_shards(num=2)

    shards_population = repo.get_shards_population()
    total_population = sum(shards_population)

    assert all([i < total_population / 2 for i in shards_population])
    assert all([i > 0 for i in shards_population])
    assert migrated_keys > 0

def test_initial_shards_behave_like_added_shards():
    repo1 = mr.MemoryRepo(shards=6)
    for i in range(1000):
        repo1.store(i, "avalue")

    repo2 = mr.MemoryRepo(shards=4)
    for i in range(1000):
        repo2.store(i, "avalue")
    repo2.add_shards(num=2)

    assert repo1.get_shards_population() == repo2.get_shards_population()

