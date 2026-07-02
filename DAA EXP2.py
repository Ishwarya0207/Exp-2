import random
import string

# Generate random text
def generate_text(length):
    text = ""
    for i in range(length):
        text += random.choice(string.ascii_lowercase)
    return text


# ---------------- NAIVE STRING MATCHING ----------------
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

    return comparisons


# ---------------- KMP STRING MATCHING ----------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        else:
            if length != 0:
                length = lps[length - 1]

            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    i = 0
    j = 0
    comparisons = 0

    while i < n:
        comparisons += 1

        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                j = lps[j - 1]

        else:
            if j != 0:
                j = lps[j - 1]

            else:
                i += 1

    return comparisons


# ---------------- RABIN-KARP STRING MATCHING ----------------
def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)

    d = 256
    q = 101

    comparisons = 0

    h = 1
    for i in range(m - 1):
        h = (h * d) % q

    pattern_hash = 0
    text_hash = 0

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q

    for i in range(n - m + 1):

        if pattern_hash == text_hash:

            for j in range(m):
                comparisons += 1

                if text[i + j] != pattern[j]:
                    break

        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h)
                         + ord(text[i + m])) % q

            if text_hash < 0:
                text_hash += q

    return comparisons


# ---------------- MAIN PROGRAM ----------------

text_length = 15000
pattern_lengths = [8, 15, 30, 75]

text = generate_text(text_length)

print("TEXT LENGTH =", text_length)
print()

print("{:<15}{:<20}{:<20}{:<20}".format(
    "Pattern Length",
    "Naive",
    "KMP",
    "Rabin-Karp"
))

print("-" * 75)

for length in pattern_lengths:

    start = random.randint(0, text_length - length)
    pattern = text[start:start + length]

    naive_comp = naive_search(text, pattern)
    kmp_comp = kmp_search(text, pattern)
    rk_comp = rabin_karp(text, pattern)

    print("{:<15}{:<20}{:<20}{:<20}".format(
        length,
        naive_comp,
        kmp_comp,
        rk_comp
    ))
