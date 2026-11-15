"""Q1: Analyse daily rainfall using lists and slicing."""
import csv
import random
import time

DAYS_IN_WEEK = 7


def weekly_totals(readings):
    """Return one total for each 7-day slice (the last week may be shorter)."""
    totals = []
    for start in range(0, len(readings), DAYS_IN_WEEK):
        week = readings[start:start + DAYS_IN_WEEK]
        totals.append(sum(week))
    return totals


def moving_average_naive(readings, window=7):
    """Calculate each average by summing the full window again."""
    if len(readings) < window:
        return []
    averages = []
    for start in range(len(readings) - window + 1):
        averages.append(sum(readings[start:start + window]) / window)
    return averages


def moving_average_running(readings, window=7):
    """Calculate averages by updating one running total."""
    if len(readings) < window:
        return []
    averages = []
    current_total = sum(readings[:window])
    averages.append(current_total / window)
    for index in range(window, len(readings)):
        current_total = current_total - readings[index - window] + readings[index]
        averages.append(current_total / window)
    return averages


def make_readings(count, seed=42):
    """Create reproducible rainfall readings in millimetres."""
    rng = random.Random(seed + count)
    return [round(rng.uniform(0, 45), 1) for _ in range(count)]


def benchmark():
    """Time naive and running-sum moving averages for the required sizes."""
    rows = []
    for count in (365, 36500, 365000):
        readings = make_readings(count)
        start = time.perf_counter()
        naive = moving_average_naive(readings)
        naive_time = time.perf_counter() - start
        start = time.perf_counter()
        running = moving_average_running(readings)
        running_time = time.perf_counter() - start
        same = len(naive) == len(running) and all(
            abs(a - b) < 1e-9 for a, b in zip(naive, running)
        )
        rows.append((count, naive_time, running_time, same,
                     6 * max(0, count - 6), 6 + max(0, count - 7)))
    with open("Task01/rainfall_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["days", "naive_seconds", "running_seconds", "same_result",
                         "naive_addition_count_estimate", "running_addition_count_estimate"])
        writer.writerows(rows)
    print("\nMOVING-AVERAGE BENCHMARK")
    print("Days | naive s | running s | same | naive additions | running additions")
    for row in rows:
        print(f"{row[0]:>6} | {row[1]:.6f} | {row[2]:.6f} | {row[3]} | {row[4]} | {row[5]}")
    print("Raw measurements saved to Task01/rainfall_benchmark.csv")


def main():
    readings = make_readings(365)
    # Add a few dry days to make the dry-day requirement easy to observe.
    for day in (20, 80, 200, 300):
        readings[day - 1] = 0.0

    weeks = weekly_totals(readings)
    max_value = max(readings)
    min_value = min(readings)
    wettest_week = weeks.index(max(weeks)) + 1
    driest_week = weeks.index(min(weeks)) + 1
    wettest_day = readings.index(max_value) + 1
    driest_day = readings.index(min_value) + 1
    dry_days = [day for day, value in enumerate(readings, start=1) if value == 0]
    averages = moving_average_running(readings)

    print("Q1 - DAILY RAINFALL RECORDS")
    print("Number of daily readings:", len(readings))
    print("First 14 readings:", readings[:14])
    print("readings[7:14]:", readings[7:14])
    print("readings[-7:]:", readings[-7:])
    print("readings[::7] (every seventh value):", readings[::7][:10], "...")
    print("First five weekly totals:", [round(x, 1) for x in weeks[:5]])
    print("Wettest week:", wettest_week, "total:", round(max(weeks), 1), "mm")
    print("Driest week:", driest_week, "total:", round(min(weeks), 1), "mm")
    print("Maximum daily rainfall:", max_value, "mm on day", wettest_day)
    print("Minimum daily rainfall:", min_value, "mm on day", driest_day)
    print("First five 7-day moving averages:", [round(x, 2) for x in averages[:5]])
    print("Dry days (1-based day numbers):", dry_days)
    print("Empty list test:", moving_average_running([]))
    print("Short list test:", moving_average_running([1, 2, 3, 4, 5, 6]))
    naive_result = moving_average_naive(readings)
    running_result = moving_average_running(readings)
    results_match = len(naive_result) == len(running_result) and all(
        abs(first - second) < 1e-9 for first, second in zip(naive_result, running_result)
    )
    print("Naive/running results match (within 1e-9):", results_match)
    benchmark()


if __name__ == "__main__":
    main()
