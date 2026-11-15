"""Q6: Store and query a railway timetable using nested data."""
import csv
import random
import sys
import time


def sample_timetable():
    return {
        "12601": {"name": "Chennai Mail", "stops": [("Chennai", "06:00", "06:10"), ("Arakkonam", "07:20", "07:22"), ("Renigunta", "09:10", "09:15")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}},
        "12602": {"name": "Coastal Express", "stops": [("Chennai", "07:00", "07:10"), ("Tambaram", "07:35", "07:37"), ("Villupuram", "09:30", "09:35")], "days": {"Mon", "Wed", "Fri", "Sun"}},
        "12603": {"name": "Hill Passenger", "stops": [("Katpadi", "05:20", "05:22"), ("Arakkonam", "06:30", "06:35"), ("Chennai", "08:00", "08:10")], "days": {"Tue", "Thu", "Sat"}},
        "12604": {"name": "City Intercity", "stops": [("Chennai", "08:00", "08:05"), ("Tambaram", "08:30", "08:32"), ("Chengalpattu", "09:20", "09:22")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri"}},
        "12605": {"name": "Southern Link", "stops": [("Villupuram", "10:00", "10:05"), ("Tambaram", "12:00", "12:02"), ("Chennai", "12:40", "12:50")], "days": {"Sat", "Sun"}},
    }


def build_station_index(timetable):
    """Map station name to train stop entries for faster repeated queries."""
    index = {}
    for train_no, details in timetable.items():
        for station, arrival, departure in details["stops"]:
            index.setdefault(station, []).append((train_no, arrival, departure, details["days"]))
    return index


def query_scan(timetable, station, day):
    results = []
    for train_no, details in timetable.items():
        if day in details["days"]:
            for stop, arrival, departure in details["stops"]:
                if stop == station:
                    results.append((train_no, details["name"], arrival, departure))
    return sorted(results, key=lambda row: row[3])


def query_index(index, timetable, station, day):
    results = []
    for train_no, arrival, departure, days in index.get(station, []):
        if day in days:
            results.append((train_no, timetable[train_no]["name"], arrival, departure))
    return sorted(results, key=lambda row: row[3])


def make_timetable(train_count, seed=12):
    rng = random.Random(seed + train_count)
    stations = [f"Station{i:02d}" for i in range(20)]
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    timetable = {}
    for number in range(train_count):
        start = rng.randrange(len(stations))
        chosen = [stations[(start + offset) % len(stations)] for offset in range(8)]
        stops = []
        base_minutes = rng.randrange(0, 600)
        for position, station in enumerate(chosen):
            arrival_minutes = base_minutes + position * 25
            departure_minutes = arrival_minutes + 2
            arrival = f"{arrival_minutes // 60:02d}:{arrival_minutes % 60:02d}"
            departure = f"{departure_minutes // 60:02d}:{departure_minutes % 60:02d}"
            stops.append((station, arrival, departure))
        days = set(rng.sample(weekdays, 5))
        train_no = f"T{number:05d}"
        timetable[train_no] = {"name": f"Train {number}", "stops": stops, "days": days}
    return timetable


def approximate_index_size(index):
    total = sys.getsizeof(index)
    for station, entries in index.items():
        total += sys.getsizeof(station) + sys.getsizeof(entries)
        for entry in entries:
            total += sys.getsizeof(entry)
    return total


def benchmark():
    rows = []
    for count in (100, 1000, 10000):
        timetable = make_timetable(count)
        start = time.perf_counter()
        index = build_station_index(timetable)
        build_time = time.perf_counter() - start
        station = "Station07"
        day = "Mon"
        # Repeat query 200 times to make very small queries measurable.
        start = time.perf_counter()
        scan_results = None
        for _ in range(200):
            scan_results = query_scan(timetable, station, day)
        scan_time = time.perf_counter() - start
        start = time.perf_counter()
        index_results = None
        for _ in range(200):
            index_results = query_index(index, timetable, station, day)
        index_time = time.perf_counter() - start
        rows.append((count, build_time, scan_time, index_time, scan_results == index_results,
                     len(index.get(station, [])), approximate_index_size(index)))
    with open("Task06/timetable_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["trains", "index_build_seconds", "200_scan_queries_seconds", "200_index_queries_seconds", "same_result", "station_entries", "approx_index_shallow_bytes"])
        writer.writerows(rows)
    print("\nTIMETABLE INDEX BENCHMARK (200 repeated station/day queries)")
    for row in rows:
        print(f"trains={row[0]:>5} build={row[1]:.6f}s scan={row[2]:.6f}s index={row[3]:.6f}s same={row[4]} entries={row[5]} approx_index_bytes={row[6]}")
    print("Raw measurements saved to Task06/timetable_benchmark.csv")


def main():
    timetable = sample_timetable()
    index = build_station_index(timetable)
    print("Q6 - RAILWAY TIMETABLE")
    for train_no, details in timetable.items():
        print(train_no, details["name"], "days:", ",".join(sorted(details["days"])))
        for station, arrival, departure in details["stops"]:
            print("  ", station, arrival, departure)
    print("\nExpression for third station departure of train 12601:", timetable["12601"]["stops"][2][2])
    station, day = "Tambaram", "Mon"
    print(f"\nTrains stopping at {station} on {day}, sorted by departure:")
    print(query_index(index, timetable, station, day))
    print("Unknown station:", query_index(index, timetable, "Unknown Station", "Mon"))
    not_running_result = query_index(index, timetable, "Chennai", "Mon")
    print("Not-running day example (12605 runs Sat/Sun):", not any(row[0] == "12605" for row in not_running_result))
    print("Approximate station-index shallow size:", approximate_index_size(index), "bytes")
    benchmark()


if __name__ == "__main__":
    main()
