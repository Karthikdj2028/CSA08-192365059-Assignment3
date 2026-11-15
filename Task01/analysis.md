# Q1 – Design and analysis answers

## Pseudocode: 7-day moving average with a running sum

```text
START
IF number of readings is less than 7 THEN
    OUTPUT empty list
ELSE
    SET running_total TO sum of first 7 readings
    OUTPUT running_total / 7
    FOR each new day from index 7 to the final index
        SUBTRACT the reading that leaves the window
        ADD the new reading that enters the window
        OUTPUT running_total / 7
    ENDFOR
ENDIF
END
```

## Slicing

- `readings[7:14]` returns elements at indexes 7 through 13 (the 8th through 14th readings); the stop index 14 is excluded.
- `readings[-7:]` returns the last seven readings.
- `readings[::7]` returns every seventh element starting at index 0.

## Why a list?

A list stores the year's readings in order and supports indexing, slicing, appending and sorting. `append()` is O(1) amortised; `insert()` and `pop()` in the middle are O(n) because later elements move; `sort()` is O(n log n). A 7-value slice takes O(7) time and creates a small temporary list.

## Additions

For n readings and a fixed window of 7:
- Naive: 7 additions for each of n-6 windows, `6(n-6)` additions: O(7n), which is O(n) because 7 is fixed.
- Running sum: 6 initial additions plus one addition and one subtraction for each later day: O(n), with fewer repeated additions. The code's CSV includes a simple operation-count estimate.

## Late insertion

`list.insert(position, value)` is O(n) in the worst case because elements after the insertion point move. A list remains suitable for a 365-day record because late corrections are infrequent and chronological indexing is useful. For a live stream that frequently removes from the front, a `deque` can be better.

## Alternatives

- `deque(maxlen=7)` keeps only the latest seven values. A running total gives O(n) processing and O(7) window storage, but it is not a replacement for retaining a full year's history.
- A dictionary keyed by date supports average O(1) lookup by date but uses O(n) storage and needs explicit sorting/grouping to make weekly reports.
