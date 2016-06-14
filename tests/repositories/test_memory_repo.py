from faker import Faker
from pyshard.repositories import memory_repo as mr


def test_store_key_value():
    repo = mr.MemoryRepo()
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"

def test_hashing_is_stable():
    fake = Faker()

    repo = mr.MemoryRepo(shards=4)
    dataset = []

    for i in range(1000):
        value = fake.text()
        repo.store(value[:50], value)

    repo._add_shards(num=1)

    shards_population = repo.get_shards_population()
    total_population = sum(shards_population)

    assert all([i < total_population / 2 for i in shards_population])
    assert all([i > 0 for i in shards_population])


def test_init_accepts_number_of_shards():
    repo = mr.MemoryRepo(shards=4)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_init_accepts_number_of_replicas():
    repo = mr.MemoryRepo(replicas=2)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_init_accepts_noth_number_of_shards_and_replicas():
    repo = mr.MemoryRepo(shards=4, replicas=2)
    repo.store("akey", "avalue")

    assert repo.load("akey") == "avalue"


def test_repo_knows_the_numer_of_shards():
    repo = mr.MemoryRepo(shards=4)
    assert repo.num_shards == 4


def test_repo_can_add_shard_when_empty():
    repo = mr.MemoryRepo(shards=4)
    repo.add_shards(num=1)
    assert repo.num_shards == 5


def test_get_shards_population():
    repo = mr.MemoryRepo(shards=4)

    assert repo.get_shards_population() == [0, 0, 0, 0]


def test_storing_key_value_populates_a_single_shard():
    repo = mr.MemoryRepo(shards=4)
    repo.store("akey", "avalue")

    assert repo.get_shards_population().count(1) == 1


def test_massive_population_is_balanced():
    fake = Faker()

    repo = mr.MemoryRepo(shards=4)
    for i in range(1000):
        value = fake.text()
        repo.store(value[:50], value)

    shards_population = repo.get_shards_population()
    total_population = sum(shards_population)

    assert all([i < total_population / 2 for i in shards_population])
    assert all([i > 0 for i in shards_population])


def test_massive_population_after_shard_addition_is_balanced():
    fake = Faker()

    repo = mr.MemoryRepo(shards=4)
    for i in range(1000):
        value = fake.text()
        repo.store(value[:50], value)

    repo._add_shards(num=1)

    shards_population = repo.get_shards_population()
    total_population = sum(shards_population)

    assert all([i < total_population / 2 for i in shards_population])
    assert all([i > 0 for i in shards_population])
