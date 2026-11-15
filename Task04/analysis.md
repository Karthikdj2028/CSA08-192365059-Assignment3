# Q4 – Set operations and clash detection

For elective sets A and B:

- `A & B` (intersection): students in both electives (clashes).
- `A ^ B` (symmetric difference): students in exactly one elective.
- `all_students - (A | B)`: students registered in neither.
- `A | B` (union): students in at least one elective.

The expected sample output is:

```text
clash : ['192311004', '192311009']
exactly one: ['192311001', '192311002', '192311007', '192311010']
neither : ['192311003', '192311005', '192311006', '192311008']
```

Sets remove duplicates because each element can appear only once. Average membership in a set is O(1); list membership is O(n). Sets cannot contain lists because lists are mutable/unhashable, but can contain tuples whose elements are hashable. Sorting a report costs O(n log n) and makes output deterministic.

A Venn diagram is included in `venn_diagram.png`: A-only and B-only are the symmetric difference, the overlap is the intersection, and the outside region is neither.

## Experiments and complexity

The membership experiment tests 10,000, 100,000 and 1,000,000 register numbers with a mixture of hits and misses. It records query time for list and set membership. The common-student experiment compares nested loops O(n × m) with set intersection O(n + m) average time (including converting lists to sets; if already sets, intersection is proportional to the smaller set on average).

A list preserves order and duplicate counts. Convert it to a set when membership and uniqueness matter more than order or repeated entries. The set loses duplicate counts and original ordering.


## Sorted-list alternative

Another way to find common registrations is to sort copies of both lists and walk them with two indexes:

```python
left = sorted(ai_list)
right = sorted(iot_list)
i = 0
j = 0
common = []
while i < len(left) and j < len(right):
    if left[i] == right[j]:
        common.append(left[i])
        i += 1
        j += 1
    elif left[i] < right[j]:
        i += 1
    else:
        j += 1
```

Sorting costs O(n log n + m log m), and the two-pointer walk costs O(n + m). If the lists are sorted copies, the temporary storage is O(n + m). Nested loops cost O(n × m) time and can be used without sorting. Set operations are usually the simplest option when the data is already represented as sets; the sorted walk is useful when deterministic sorted order is needed and the input is already sorted.
