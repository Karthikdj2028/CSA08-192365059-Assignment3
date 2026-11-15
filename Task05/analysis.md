# Q5 – Cleaning sensor readings

A sensor value is valid when `-50 <= celsius <= 50`. The three implementations return the same `(minute, Celsius, Fahrenheit)` records:

1. A `for` loop with `append()`.
2. A list comprehension with an `if` condition.
3. `filter()` and `map()` with lambda functions.

The Fahrenheit conversion is `F = C * 9 / 5 + 32`. The alarm list contains minute numbers for valid readings outside 2°C to 8°C. Invalid sensor readings are reported separately and are not treated as a temperature alarm; this is an explicit assumption.

## Comprehensions and generators

General form: `[expression for item in iterable if condition]`.

Example dictionary comprehension: `{minute: value for minute, value in enumerate(readings, 1) if -50 <= value <= 50}`.

Example set comprehension: `{round(value, 1) for value in readings if -50 <= value <= 50}`.

A comprehension creates a complete list immediately. A generator expression `(expression for item in iterable if condition)` creates values lazily. A long comprehension with nested conditions or side effects is harder to read and should be replaced by a normal loop.

## Experimental investigation

The program creates 10,000, 100,000 and 1,000,000 readings, times all three approaches with `time.perf_counter()` and writes `sensor_benchmark.csv`. It verifies that each output list is identical. It also reports `sys.getsizeof()` for a valid-values list and a generator object. This is a shallow object-size measurement; it does not include all referenced values.

All three approaches need O(n) time. A list result uses O(n) space. A generator itself uses O(1) extra state (not counting any data retained elsewhere) and can be consumed without storing all results. A list comprehension is convenient and readable, but it is not always the best choice when the input is huge and streaming is enough.
