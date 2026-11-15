"""Q5: Clean and convert cold-storage sensor readings."""
import csv
import random
import sys
import time


def valid_reading(value):
    return -50 <= value <= 50


def clean_loop(readings):
    result = []
    for minute, celsius in enumerate(readings, start=1):
        if valid_reading(celsius):
            result.append((minute, celsius, celsius * 9 / 5 + 32))
    return result


def clean_comprehension(readings):
    return [
        (minute, celsius, celsius * 9 / 5 + 32)
        for minute, celsius in enumerate(readings, start=1)
        if valid_reading(celsius)
    ]


def clean_map_filter(readings):
    indexed = enumerate(readings, start=1)
    valid_items = filter(lambda item: valid_reading(item[1]), indexed)
    return list(map(lambda item: (item[0], item[1], item[1] * 9 / 5 + 32), valid_items))


def alarm_minutes(readings):
    return [
        minute for minute, value in enumerate(readings, start=1)
        if valid_reading(value) and not (2 <= value <= 8)
    ]


def benchmark():
    rows = []
    for count in (10000, 100000, 1000000):
        rng = random.Random(101 + count)
        readings = [round(rng.uniform(-60, 60), 2) for _ in range(count)]
        times = []
        outputs = []
        for function in (clean_loop, clean_comprehension, clean_map_filter):
            start = time.perf_counter()
            output = function(readings)
            times.append(time.perf_counter() - start)
            outputs.append(output)
        same = outputs[0] == outputs[1] == outputs[2]
        rows.append((count, times[0], times[1], times[2], same, len(outputs[0])))
    with open("Task05/sensor_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["readings", "loop_seconds", "comprehension_seconds", "map_filter_seconds", "same_result", "valid_count"])
        writer.writerows(rows)
    print("\nSENSOR PERFORMANCE")
    print("Readings | for+append | comprehension | map/filter | same | valid")
    for row in rows:
        print(f"{row[0]:>9} | {row[1]:.6f} | {row[2]:.6f} | {row[3]:.6f} | {row[4]} | {row[5]}")
    print("Raw timings saved to Task05/sensor_benchmark.csv")


def main():
    readings = [4.0, 5.5, 9.2, 1.5, 55.0, -55.0, 6.0, 12.0, 7.0, 0.0, 3.0, 51.0]
    loop_result = clean_loop(readings)
    comp_result = clean_comprehension(readings)
    map_result = clean_map_filter(readings)
    errors = [(minute, value) for minute, value in enumerate(readings, start=1) if not valid_reading(value)]

    print("Q5 - SENSOR READING CLEANING")
    print("Valid records (minute, C, F):")
    for row in loop_result:
        print(row[0], f"{row[1]:.2f} C", f"{row[2]:.2f} F")
    print("Sensor-error minutes and values:", errors)
    print("Alarm minutes outside 2-8 C:", alarm_minutes(readings))
    print("All three methods give same result:", loop_result == comp_result == map_result)
    print("All-valid test count:", len(clean_comprehension([3.0, 4.0, 5.0])))
    print("All-invalid test count:", len(clean_comprehension([55.0, -60.0, 100.0])))
    print("Empty list test:", clean_comprehension([]))

    valid_list = [value for value in readings if valid_reading(value)]
    valid_generator = (value for value in readings if valid_reading(value))
    print("List comprehension shallow size:", sys.getsizeof(valid_list), "bytes")
    print("Generator object size:", sys.getsizeof(valid_generator), "bytes")
    print("Note: getsizeof is shallow; a generator produces values on demand.")
    print("Dictionary comprehension example:", {minute: value for minute, value in enumerate(readings, 1) if valid_reading(value)})
    print("Set comprehension example:", {round(value, 1) for value in readings if valid_reading(value)})
    benchmark()


if __name__ == "__main__":
    main()
