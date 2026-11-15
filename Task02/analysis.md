# Q2 – Tuples, mutability and copying

## Tuple and list choices

A stop coordinate is a fixed pair `(latitude, longitude)`, so a tuple clearly represents one unchanging coordinate and can be a dictionary key. Tuples are hashable when all their elements are hashable. Lists are mutable and therefore unhashable; using a list as a dictionary key raises `TypeError: unhashable type: 'list'`.

## Grid memory diagrams

Bad construction: `bad = [[0] * 4] * 3`

```text
bad ──┬──> row object A [0, 7, 0, 0]
      ├──> row object A [same object]
      └──> row object A [same object]
```

Correct construction: `good = [[0 for col in range(4)] for row in range(3)]`

```text
good ─┬──> row object A [0, 7, 0, 0]
      ├──> row object B [0, 0, 0, 0]
      └──> row object C [0, 0, 0, 0]
```

The `is` test and `id()` output show whether two names point to the same object.

## Copying

- Aliasing (`alias = original`) makes a second name for the same outer list.
- A shallow copy (`copy.copy()` or `original[:]`) creates a new outer list but keeps references to the same inner lists.
- A deep copy (`copy.deepcopy()`) recursively copies nested mutable objects.
- A shallow copy is enough for a flat list of immutable values. A deep copy is needed when independent nested lists/dictionaries are required.
- A function receives a reference to the list object; mutating the list changes that same object seen by the caller.

A tuple cannot have its elements replaced, but a mutable object stored inside a tuple can still be changed. The tuple protects its references, not the internal state of nested objects.

## Memory and timing

`sys.getsizeof()` reports shallow container size. It does not recursively add the sizes of referenced integer objects. The program separately times creating a one-million-value list and tuple (three repetitions), then times repeated indexing using the same million-value data. List and tuple indexing are both O(1); creation and indexing timing differences are machine-dependent.

## Sparse dictionary alternative

A grid dictionary such as `{(row, col): passenger_count}` stores only zones with passengers. Average lookup is O(1) for both a list-of-lists and a dictionary. A dense list-of-lists uses O(rows × columns) space; a sparse dictionary uses O(number of non-empty zones) space but needs a default value for absent zones.
