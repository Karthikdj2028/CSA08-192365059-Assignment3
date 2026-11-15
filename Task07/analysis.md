# Q7 – Contact-merging design from first principles

## Stage 1: Interpret the problem

Inputs are contact records from two phones and a SIM. Each may contain a name, zero or more phone numbers, zero or more email addresses and a source label. The output is one merged record per identifiable person, containing all known name variants, normalised phone numbers, email addresses and source labels.

Measurable rules:

1. Every input record is represented in one output contact.
2. A phone is normalised to ten digits for Indian mobile-number examples (strip spaces/punctuation and an optional `+91` or leading `0`).
3. Contacts sharing a normalised phone number are merged.
4. When no phone match exists, a matching normalised email can be used as a fallback identity key.
5. A matching name alone never merges two contacts; two different people may share a name.
6. Sets prevent repeated phone numbers and emails inside a merged contact.
7. A record with no usable phone or email is retained separately rather than guessed to be someone else.

## Stage 2: Design and pseudocode

```text
START
CREATE empty contacts dictionary
CREATE empty phone_owner dictionary
CREATE empty email_owner dictionary
FOR each input contact
    NORMALISE every phone and email
    FIND existing contact IDs through phone_owner and email_owner
    IF no existing ID is found THEN
        CREATE a new contact ID and empty sets
    ELSE
        CHOOSE one existing ID
        MERGE any other matched contact records into it
    ENDIF
    ADD the name, normalised phones, emails and source to the contact sets
    UPDATE phone_owner and email_owner for every key
ENDFOR
OUTPUT the merged contacts
END
```

The main dictionary stores one contact record per canonical contact ID. Each record keeps original name variants and a set of normalised name forms (lower case, title removed, punctuation removed and spaces collapsed). `phone_owner` is the dictionary keyed by normalised phone number, and `email_owner` supports records with missing phone numbers. Sets store multiple unique original/normalised names, phones, emails and sources. Names are normalised for consistent storage and display, but are not used alone to decide identity.

## Stage 3: Implementation and measurement

The program tests phone formats such as `+91 98400 12345`, `9840012345` and a leading-zero form. The small hand test contains Ravi duplicates across sources, an Anita duplicate, two different people both named Arun, an email-only duplicate and a record with no identifying details. It benchmarks dictionary merging at 1,000 and 100,000 contacts.

The pairwise baseline is measured at 1,000 contacts. A 100,000-contact pairwise check would require 4,999,950,000 comparisons, so the program does not run that impractical test by default. Instead it clearly labels a quadratic extrapolation based on the measured 1,000-contact time. The 100,000-contact dictionary merge is measured directly. Do not describe the extrapolation as an observed time.

## Stage 4: Evaluation

Dictionary indexing is better than comparing every pair because average dictionary lookup is O(1), so building the index and processing n contacts is O(n) average time. Pairwise comparison is O(n²). The dictionary design needs O(n) extra space for contacts and lookup indexes. It is appropriate when contact records have reliable common phone numbers or emails.

Limitations: two records for the same person cannot be confidently linked if they have no shared phone or email. Similar names are not enough to infer identity. The phone normaliser is designed for the Indian mobile-number examples in this assignment; international numbers require country-aware rules and stronger validation. A production app should show uncertain matches to the user before merging.
