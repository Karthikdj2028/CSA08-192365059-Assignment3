"""Q4: Use sets to detect elective registration clashes."""
import csv
import random
import time


def membership_benchmark():
    rows = []
    for size in (10000, 100000, 1000000):
        values = [f"S{i:08d}" for i in range(size)]
        value_set = set(values)
        # Mix hits and misses; repeat enough queries to make timing visible.
        queries = [values[-1], values[size // 2], "NOT-REGISTERED"] * 20
        start = time.perf_counter()
        list_hits = sum(query in values for query in queries)
        list_time = time.perf_counter() - start
        start = time.perf_counter()
        set_hits = sum(query in value_set for query in queries)
        set_time = time.perf_counter() - start
        rows.append((size, len(queries), list_time, set_time, list_hits == set_hits))
    return rows


def intersection_benchmark():
    first = [f"S{i:05d}" for i in range(5000)]
    second = [f"S{i:05d}" for i in range(2500, 7500)]
    start = time.perf_counter()
    nested = set()
    for left in first:
        for right in second:
            if left == right:
                nested.add(left)
    nested_time = time.perf_counter() - start
    start = time.perf_counter()
    common = set(first) & set(second)
    set_time = time.perf_counter() - start
    return nested_time, set_time, nested == common, len(common)


def main():
    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)
    union = ai_elective | iot_elective

    print("Q4 - ELECTIVE REGISTRATION CLASH DETECTION")
    print("clash:", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither:", sorted(neither))
    print("union:", sorted(union))
    print("Duplicates removed automatically by sets:", len(["192311004", "192311004"]), "list entries ->", len({"192311004", "192311004"}), "set entry")
    print("Empty elective test:", set() & ai_elective, set() ^ ai_elective)
    print("Identical electives test:", ai_elective & ai_elective, ai_elective ^ ai_elective)
    print("Hand-check: two clash, four exactly one, four neither.")

    print("\nMEMBERSHIP BENCHMARK")
    membership_rows = membership_benchmark()
    for row in membership_rows:
        print(f"n={row[0]:>7} queries={row[1]:>3} list={row[2]:.6f}s set={row[3]:.6f}s same={row[4]}")

    nested_time, set_time, same, common_count = intersection_benchmark()
    print("\nCOMMON STUDENTS")
    print(f"Nested loops: {nested_time:.6f}s | set &: {set_time:.6f}s | same={same} | common={common_count}")

    with open("Task04/sets_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["size", "query_count", "list_membership_seconds", "set_membership_seconds", "same_hits"])
        writer.writerows(membership_rows)
        writer.writerow([])
        writer.writerow(["nested_loop_seconds", "set_intersection_seconds", "same_result", "common_count"])
        writer.writerow([nested_time, set_time, same, common_count])
    print("Raw measurements saved to Task04/sets_benchmark.csv")


if __name__ == "__main__":
    main()
