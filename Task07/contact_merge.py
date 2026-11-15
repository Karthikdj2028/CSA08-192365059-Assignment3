"""Q7: Merge contacts using normalised phone and email dictionaries."""
import csv
import random
import string
import time


def normalise_phone(raw):
    """Return a 10-digit Indian number, or None when no valid number is present."""
    digits = "".join(character for character in str(raw) if character.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[-10:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[-10:]
    if len(digits) == 10:
        return digits
    return None


def normalise_email(raw):
    return str(raw).strip().lower() if raw and str(raw).strip() else None


def normalise_name(raw):
    clean = str(raw or "").strip().lower()
    clean = clean.replace("dr.", "").replace("dr ", "")
    clean = clean.translate(str.maketrans("", "", string.punctuation))
    return " ".join(clean.split())


def merge_contacts(records):
    """Merge records when a normalised phone matches, or email matches as fallback."""
    contacts = {}
    phone_owner = {}
    email_owner = {}
    next_id = 1

    for record in records:
        raw_phones = record.get("phones", []) or []
        raw_emails = record.get("emails", []) or []
        phones = {number for number in (normalise_phone(p) for p in raw_phones) if number}
        emails = {email for email in (normalise_email(e) for e in raw_emails) if email}
        names = {str(record.get("name", "")).strip()} if str(record.get("name", "")).strip() else set()
        normalised_names = {normalise_name(name) for name in names if normalise_name(name)}
        sources = {str(record.get("source", "unknown"))}

        matched_ids = set()
        for number in phones:
            if number in phone_owner:
                matched_ids.add(phone_owner[number])
        for email in emails:
            if email in email_owner:
                matched_ids.add(email_owner[email])

        if not matched_ids:
            contact_id = f"C{next_id:05d}"
            next_id += 1
            contacts[contact_id] = {"names": set(), "normalised_names": set(), "phones": set(), "emails": set(), "sources": set()}
        else:
            contact_id = sorted(matched_ids)[0]
            # If this record connects two previously separate groups, combine them.
            for other_id in sorted(matched_ids - {contact_id}):
                for number in contacts[other_id]["phones"]:
                    phone_owner[number] = contact_id
                for email in contacts[other_id]["emails"]:
                    email_owner[email] = contact_id
                for field in ("names", "normalised_names", "phones", "emails", "sources"):
                    contacts[contact_id][field].update(contacts[other_id][field])
                del contacts[other_id]

        contacts[contact_id]["names"].update(names)
        contacts[contact_id]["normalised_names"].update(normalised_names)
        contacts[contact_id]["phones"].update(phones)
        contacts[contact_id]["emails"].update(emails)
        contacts[contact_id]["sources"].update(sources)
        for number in phones:
            phone_owner[number] = contact_id
        for email in emails:
            email_owner[email] = contact_id

    return contacts


def hand_test_records():
    return [
        {"source": "Phone 1", "name": "Dr. Ravi", "phones": ["+91 98400 12345"], "emails": ["RAVI@MAIL.COM"]},
        {"source": "Phone 2", "name": "Ravi Kumar", "phones": ["9840012345", "9884011111"], "emails": ["ravi@mail.com", "ravi.k@example.com"]},
        {"source": "SIM", "name": "Dr Ravi K", "phones": ["09884011111"], "emails": []},
        {"source": "Phone 1", "name": "Anita", "phones": ["9000011111"], "emails": ["anita@example.com"]},
        {"source": "SIM", "name": "Anita", "phones": ["+91-90000-11111"], "emails": []},
        {"source": "Phone 2", "name": "Arun", "phones": ["9111122222"], "emails": []},
        {"source": "SIM", "name": "Arun", "phones": ["9222233333"], "emails": []},
        {"source": "Phone 1", "name": "Email only", "phones": [], "emails": ["solo@example.com"]},
        {"source": "SIM", "name": "Email Only", "phones": [], "emails": ["SOLO@example.com"]},
        {"source": "Phone 2", "name": "No details", "phones": [], "emails": []},
    ]


def make_contacts(count, seed=27):
    rng = random.Random(seed + count)
    records = []
    # Every tenth record repeats the prior contact's number in another format.
    for index in range(count):
        if index > 0 and index % 10 == 0:
            number = f"+91 {9000000000 + index - 1:010d}"[-15:]
            records.append({"source": "generated duplicate", "name": f"Person {index-1}",
                            "phones": [number], "emails": [f"person{index-1}@example.com"]})
        else:
            phone = str(9000000000 + index)
            records.append({"source": "generated", "name": f"Person {index}",
                            "phones": [phone], "emails": [f"person{index}@example.com"]})
    rng.shuffle(records)
    return records


def naive_pairwise_duplicate_checks(records):
    """Compare every pair; used only for the 1,000-record baseline."""
    phones = []
    for record in records:
        phones.append({p for p in (normalise_phone(x) for x in record.get("phones", [])) if p})
    matches = 0
    for left in range(len(phones)):
        for right in range(left + 1, len(phones)):
            if phones[left] and phones[right] and phones[left].intersection(phones[right]):
                matches += 1
    return matches


def benchmark():
    rows = []
    naive_1000_seconds = None
    for count in (1000, 100000):
        records = make_contacts(count)
        start = time.perf_counter()
        merged = merge_contacts(records)
        dict_time = time.perf_counter() - start
        expected_comparisons = count * (count - 1) // 2
        if count == 1000:
            start = time.perf_counter()
            pair_matches = naive_pairwise_duplicate_checks(records)
            naive_time = time.perf_counter() - start
            naive_1000_seconds = naive_time
            naive_status = "measured"
        else:
            # 100,000 contacts require almost five billion pair checks; do not run
            # a deliberately quadratic baseline for an impractical length of time.
            pair_matches = "not run"
            naive_time = naive_1000_seconds * (expected_comparisons / (1000 * 999 / 2))
            naive_status = "estimated from measured 1,000-contact baseline"
        rows.append((count, len(merged), dict_time, pair_matches, naive_time,
                     expected_comparisons, naive_status))
    with open("Task07/contact_benchmark.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["input_contacts", "merged_contacts", "dictionary_merge_seconds", "pairwise_matches_or_status", "pairwise_seconds_measured_or_estimated", "pair_comparisons", "pairwise_timing_status"])
        writer.writerows(rows)
    print("\nCONTACT MERGE BENCHMARK")
    print("Contacts | merged | dictionary seconds | pair comparisons | pairwise seconds | status")
    for row in rows:
        print(f"{row[0]:>8} | {row[1]:>6} | {row[2]:.6f} | {row[5]:>15,} | {row[4]:.6f} | {row[6]}")
    print("100,000-contact pairwise time is an extrapolation, not a measured run.")
    print("Raw measurements saved to Task07/contact_benchmark.csv")


def main():
    records = hand_test_records()
    merged = merge_contacts(records)
    print("Q7 - CONTACT MERGING")
    print("Normalisation examples:")
    for raw in ["+91 98400 12345", "9840012345", "09884011111"]:
        print(raw, "->", normalise_phone(raw))
    print("\nMerged contacts:")
    for contact_id, details in sorted(merged.items()):
        print(contact_id)
        print("  names:", sorted(details["names"]))
        print("  normalised names:", sorted(details["normalised_names"]))
        print("  phones:", sorted(details["phones"]))
        print("  emails:", sorted(details["emails"]))
        print("  sources:", sorted(details["sources"]))
    print("Unique merged records:", len(merged))
    print("Two people named Arun remain separate:", sum("Arun" in c["names"] for c in merged.values()) == 2)
    print("Missing-information record retained:", any("No details" in c["names"] for c in merged.values()))
    print("Normalised name example:", normalise_name("Dr. Ravi Kumar"))
    benchmark()


if __name__ == "__main__":
    main()
