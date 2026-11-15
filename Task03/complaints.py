"""Q3: Count complaint words and group complaints by district."""
import csv
import random
import string
import time
from collections import Counter

STOP = {"not", "the", "is", "and", "to", "a", "in", "has"}


def words_in(text):
    """Return lower-case words after removing basic punctuation."""
    clean = text.lower().translate(str.maketrans("", "", string.punctuation))
    return clean.split()


def frequencies(texts, stop=STOP):
    """Count non-stop words with dict.get()."""
    counts = {}
    for text in texts:
        for word in words_in(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def group_by_district(records):
    """Group complaint text by district using setdefault()."""
    groups = {}
    for record in records:
        district = record["district"]
        groups.setdefault(district, []).append(record["text"])
    return groups


def top(counts, k):
    """Sort by highest count, then alphabetical word for ties."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def dictionary_count_tokens(tokens):
    """Count an already-tokenised list with dict.get()."""
    result = {}
    for word in tokens:
        result[word] = result.get(word, 0) + 1
    return result


def list_count_method(tokens):
    """Slow alternative: call list.count once for each distinct word."""
    result = {}
    for word in set(tokens):
        result[word] = tokens.count(word)
    return result


def make_complaints(count, seed=7):
    rng = random.Random(seed + count)
    districts = ["Chennai", "Thiruvallur", "Kanchipuram", "Vellore"]
    samples = [
        "seeds delayed farmer needs seeds",
        "fertiliser price high in district",
        "water supply problem for paddy crop",
        "cotton pest attack and crop loss",
        "subsidy not received by farmer",
        "rice price support needed",
    ]
    records = []
    for index in range(count):
        records.append({"district": rng.choice(districts), "text": rng.choice(samples)})
    return records


def benchmark():
    rows = []
    for count in (1000, 10000, 100000):
        records = make_complaints(count)
        tokens = []
        for record in records:
            tokens.extend(words_in(record["text"]))
        tokens = [word for word in tokens if word not in STOP]
        start = time.perf_counter()
        dict_result = dictionary_count_tokens(tokens)
        dict_time = time.perf_counter() - start
        start = time.perf_counter()
        list_result = list_count_method(tokens)
        list_time = time.perf_counter() - start
        start = time.perf_counter()
        counter_result = dict(Counter(tokens))
        counter_time = time.perf_counter() - start
        same = dict_result == list_result == counter_result
        rows.append((count, len(tokens), len(dict_result), dict_time, list_time, counter_time, same))
    with open("Task03/complaints_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["complaints", "tokens", "distinct_words", "dict_seconds", "list_count_seconds", "counter_seconds", "same_result"])
        writer.writerows(rows)
    print("\nBENCHMARK: DICTIONARY / list.count() / Counter")
    print("Complaints | tokens | distinct | dict s | list.count s | Counter s | same")
    for row in rows:
        print(f"{row[0]:>10} | {row[1]:>6} | {row[2]:>8} | {row[3]:.6f} | {row[4]:.6f} | {row[5]:.6f} | {row[6]}")
    print("Raw measurements saved to Task03/complaints_benchmark.csv")


def main():
    calls = [
        "seeds not received seeds delayed",
        "fertiliser price high",
        "seeds price high subsidy not received",
    ]
    stop = {"not", "high"}
    counts = frequencies(calls, stop)
    print("Q3 - FARMER HELPLINE COMPLAINT ANALYSIS")
    print("Frequencies:", counts)
    print("Top 3:", top(counts, 3))
    print("Price comes before received because both have count 2 and price is alphabetically earlier.")
    records = [
        {"district": "Chennai", "text": "Seeds delayed"},
        {"district": "Chennai", "text": "Water problem"},
        {"district": "Vellore", "text": "Cotton pest"},
    ]
    print("District groups:", group_by_district(records))
    print("Empty text:", frequencies(["", "!!!"], stop))
    print("Case/punctuation:", frequencies(["SEEDS, seeds! Seeds."], set()))
    benchmark()


if __name__ == "__main__":
    main()
