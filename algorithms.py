
from collections import defaultdict
from time import perf_counter
import string


WORD_LENGTH = 5

# 1. TRIE DATA STRUCTURE

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Trie for efficient positional-pattern searches."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search_pattern(self, pattern):
        """
        Search a five-letter pattern.
        '_' represents an unknown position.

        Returns:
            Matching words and the number of trie nodes visited.
        """
        results = []
        nodes_visited = 0

        def dfs(node, position, prefix):
            nonlocal nodes_visited
            nodes_visited += 1

            if position == WORD_LENGTH:
                if node.is_end:
                    results.append(prefix)
                return

            char = pattern[position]

            if char == "_":
                for next_char, child in node.children.items():
                    dfs(child, position + 1, prefix + next_char)
            else:
                child = node.children.get(char)

                if child is not None:
                    dfs(child, position + 1, prefix + char)

        dfs(self.root, 0, "")
        return sorted(results), nodes_visited


# 2. DICTIONARY INDEX

class WordDictionary:
    """Stores five-letter words and builds search indexes."""

    def __init__(self, words):
        self.words = sorted({
            word.strip().lower()
            for word in words
            if len(word.strip()) == WORD_LENGTH
            and all(
                char in string.ascii_lowercase
                for char in word.strip().lower()
            )
        })

        self.letter_index = defaultdict(set)
        self.signature_index = defaultdict(set)
        self.trie = Trie()

        for word in self.words:
            for letter in set(word):
                self.letter_index[letter].add(word)

            signature = "".join(sorted(set(word)))
            self.signature_index[signature].add(word)

            self.trie.insert(word)


# 3. CONSTRAINT MATCHING

def matches_constraints(
    word,
    mode,
    pattern=None,
    required_letters=None,
    excluded_letters=None
):
    """Check whether a word satisfies a search constraint."""

    if len(word) != WORD_LENGTH:
        return False

    if mode == "position":
        if pattern is None or len(pattern) != WORD_LENGTH:
            raise ValueError("Pattern must contain exactly five characters.")

        pattern = pattern.lower()

        if any(
            char != "_" and char not in string.ascii_lowercase
            for char in pattern
        ):
            raise ValueError("Use letters and underscores only.")

        return all(
            expected == "_" or word[i] == expected
            for i, expected in enumerate(pattern)
        )

    if mode == "required":
        required = set((required_letters or "").lower())

        if not required.issubset(set(string.ascii_lowercase)):
            raise ValueError("Required letters must be A-Z.")

        return required.issubset(set(word))

    if mode == "excluded":
        excluded = set((excluded_letters or "").lower())

        if not excluded.issubset(set(string.ascii_lowercase)):
            raise ValueError("Excluded letters must be A-Z.")

        return not bool(set(word) & excluded)

    raise ValueError(f"Unknown search mode: {mode}")


#  ALGORITHM A: NAIVE SEARCH

def naive_search(
    dictionary,
    mode,
    pattern=None,
    required_letters=None,
    excluded_letters=None
):
    """
    Baseline: examine every word and check its constraints.

    Returns:
        (matching_words, words_examined)
    """
    results = []
    words_examined = 0

    for word in dictionary.words:
        words_examined += 1

        if matches_constraints(
            word,
            mode,
            pattern,
            required_letters,
            excluded_letters
        ):
            results.append(word)

    return results, words_examined


#  ALGORITHM B: TRIE SEARCH

def trie_search(dictionary, pattern):
    """Use Trie traversal for known-position searches."""

    pattern = pattern.lower()

    if len(pattern) != WORD_LENGTH:
        raise ValueError("Pattern must contain exactly five characters.")

    if any(
        char != "_" and char not in string.ascii_lowercase
        for char in pattern
    ):
        raise ValueError("Use letters and underscores only.")

    return dictionary.trie.search_pattern(pattern)


# ALGORITHM C: HASH-BASED SEARCH

def hash_search(
    dictionary,
    mode,
    required_letters=None,
    excluded_letters=None
):
    """Use precomputed letter indexes to filter candidates."""

    candidates = set(dictionary.words)

    if mode == "required":
        required = set((required_letters or "").lower())

        if not required.issubset(set(string.ascii_lowercase)):
            raise ValueError("Required letters must be A-Z.")

        for letter in required:
            candidates.intersection_update(
                dictionary.letter_index.get(letter, set())
            )

    elif mode == "excluded":
        excluded = set((excluded_letters or "").lower())

        if not excluded.issubset(set(string.ascii_lowercase)):
            raise ValueError("Excluded letters must be A-Z.")

        for letter in excluded:
            candidates.difference_update(
                dictionary.letter_index.get(letter, set())
            )

    else:
        raise ValueError(
            "Hash search supports required and excluded modes."
        )

    return sorted(candidates), len(candidates)



# ALGORITHM D: SORTED-LETTER SIGNATURE

def signature_search(dictionary, required_letters):
    """
    Auxiliary experiment: find words whose distinct-letter
    set exactly matches the supplied letters.
    """

    required = set(required_letters.lower())

    if not required.issubset(set(string.ascii_lowercase)):
        raise ValueError("Letters must be A-Z.")

    signature = "".join(sorted(required))

    results = sorted(dictionary.signature_index.get(signature, set()))

    return results, len(results)


# BENCHMARK TIMING HELPER


def timed_search(search_function, *args, **kwargs):
    """Measure search execution time."""

    start = perf_counter()
    results, operations = search_function(*args, **kwargs)
    elapsed = perf_counter() - start

    return {
        "results": results,
        "count": len(results),
        "operations": operations,
        "time_seconds": elapsed,
    }


def combined_search(
    dictionary,
    pattern,
    required_letters,
    excluded_letters
):
    """Find words satisfying all three constraints."""

    results = []
    candidates_examined = 0

    for word in dictionary.words:
        candidates_examined += 1

        if matches_constraints(
            word,
            "position",
            pattern=pattern
        ) and matches_constraints(
            word,
            "required",
            required_letters=required_letters
        ) and matches_constraints(
            word,
            "excluded",
            excluded_letters=excluded_letters
        ):
            results.append(word)

    return results, candidates_examined
