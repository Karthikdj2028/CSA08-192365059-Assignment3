# Q6 – Nested railway timetable

## Data structure

```text
 timetable
   train number (dictionary key)
      name: string
      stops: list of (station, arrival, departure) tuples
      days: set of running weekdays
```

For train `12601`, the departure from the third station is:

` timetable["12601"]["stops"][2][2] `

A dictionary is suitable for direct access by train number; a list preserves the order of stops; each stop is a fixed tuple; and a set stores unique running days with fast membership tests.

## Query work and index

Without an index, a query scans every train and every stop, so the work is O(total stops). A station index maps a station to only the trains stopping there. After building it once in O(total stops) time and extra O(total stops) space, a query examines O(k) entries for that station, where k is the number of trains stopping there, plus O(k log k) if results must be sorted by departure time.

The script compares 200 repeated queries for 100, 1,000 and 10,000 synthetic trains. It records index construction time, scan time, indexed query time, result equality and an approximate shallow memory size. Some inner objects (for example the running-day sets) are shared with the timetable, so the size is an estimate of additional container structure, not a full process memory profile.

## Alternative flat list

A flat list of `(train, station, arrival, departure, days)` tuples is simple but every query scans all stop records: O(total stops). A station index uses additional memory but reduces a query to O(trains at that station) before sorting. This is useful when many station queries are made against a timetable that changes infrequently.
