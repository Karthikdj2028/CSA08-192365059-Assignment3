"""Q2: Demonstrate tuples, aliasing, shallow copy and deep copy."""
import copy
import sys
import time


def main():
    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for column in range(cols)] for row in range(rows)]
    good[0][1] = 7

    print("Q2 - GRID ALIASING")
    print("bad :", bad)
    print("good:", good)
    print("bad rows are same object:", bad[0] is bad[1])
    print("good rows are same object:", good[0] is good[1])
    print("bad row ids:", [id(row) for row in bad])
    print("good row ids:", [id(row) for row in good])

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar",
    }
    print("\nTUPLE DICTIONARY KEY:")
    print(stops[(13.0418, 80.2341)])
    try:
        invalid = [13.0418, 80.2341]
        print(stops[invalid])
    except TypeError as error:
        print("List key error:", error)

    print("\nALIASING AND COPIES:")
    original = [[1, 2], [3, 4]]
    alias = original
    shallow = copy.copy(original)
    sliced = original[:]
    deep = copy.deepcopy(original)
    original[0][0] = 99
    print("original:", original)
    print("alias sees change:", alias)
    print("shallow sees inner change:", shallow)
    print("slice sees inner change:", sliced)
    print("deep copy is independent:", deep)
    print("original is alias:", original is alias)
    print("original is shallow:", original is shallow)
    print("original first row is shallow first row:", original[0] is shallow[0])

    print("\nTUPLE CONTAINING A LIST:")
    route = ("Route 1", ["Central", "Egmore"])
    route[1].append("Beach")
    print(route, "(tuple itself is fixed; nested list can change)")

    print("\nTUPLE UNPACKING:")
    for latitude, longitude in [(13.0827, 80.2707), (13.0418, 80.2341)]:
        print("Latitude:", latitude, "Longitude:", longitude)

    print("\nMEMORY AND ACCESS EXPERIMENT (one million values):")
    values = list(range(1_000_000))
    values_tuple = tuple(values)
    print("List shallow size:", sys.getsizeof(values), "bytes")
    print("Tuple shallow size:", sys.getsizeof(values_tuple), "bytes")
    print("Note: getsizeof reports the container only, not all referenced objects.")

    # Time construction separately using the same number of values.
    create_repeat = 3
    start = time.perf_counter()
    for _ in range(create_repeat):
        new_list = list(range(1_000_000))
    list_create_time = time.perf_counter() - start
    start = time.perf_counter()
    for _ in range(create_repeat):
        new_tuple = tuple(range(1_000_000))
    tuple_create_time = time.perf_counter() - start
    print(f"Create 1,000,000 values {create_repeat} times - list: {list_create_time:.6f}s, tuple: {tuple_create_time:.6f}s")

    repeat = 500_000
    start = time.perf_counter()
    for _ in range(repeat):
        result = values[500_000]
    list_access = time.perf_counter() - start
    start = time.perf_counter()
    for _ in range(repeat):
        result = values_tuple[500_000]
    tuple_access = time.perf_counter() - start
    print(f"Index {repeat:,} times - list: {list_access:.6f}s, tuple: {tuple_access:.6f}s")


if __name__ == "__main__":
    main()
