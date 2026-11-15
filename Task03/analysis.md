# Q3 – Dictionary complaint analysis

## Complete the Code logic

`frequencies()` loops through every complaint, converts it into lower-case words, removes punctuation, ignores stop words and updates a dictionary with `counts.get(word, 0) + 1`. `top()` sorts `(word, count)` pairs by `(-count, word)` so larger counts appear first and alphabetical order breaks ties. `group_by_district()` uses `setdefault(district, [])` to create a list only when a district is first seen.

For the supplied sample, the result is:

```text
[('seeds', 3), ('price', 2), ('received', 2)]
```

Price comes before received because their counts tie and `price` is alphabetically before `received`.

## Dictionary lookup

A dictionary uses a hash of a key to find a bucket. Average lookup, insertion and update are O(1), assuming a good hash distribution. In the worst case of many collisions, lookup can degrade. Python 3.7+ guarantees insertion order for dictionaries. `keys()`, `values()` and `items()` return dynamic view objects that reflect later dictionary changes.

## Complexity comparison

Let n be the number of word tokens and d the number of distinct words:
- Dictionary counting: average O(n) time and O(d) space.
- `list.count()` for every distinct word: O(n × d) time, plus O(d) result space.
- `collections.Counter`: concise frequency counting with average O(n) time and O(d) space.

The script creates 1,000, 10,000 and 100,000 synthetic complaints. It measures dictionary counting, list.count() and Counter using `time.perf_counter()` and writes the raw measurements to CSV.

## Deployment decision

For 100,000 complaints a day, deploy dictionary counting or `Counter`, not repeated `list.count()`. Keep the raw text separately for audit. A production system should use a language-aware tokenizer and a department-maintained stop-word list.
