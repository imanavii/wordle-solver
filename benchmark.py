
from pathlib import Path
from statistics import median
from time import perf_counter

from algorithms import (
    WordDictionary,
    naive_search,
    trie_search,
    hash_search,
    combined_search,
    matches_constraints,
)
from main import load_dictionary


REPEATS = 5


def benchmark_function(function, repeats=REPEATS):
    """Run a search repeatedly and report its median execution time."""

    times = []
    results = None
    operations = None

    for _ in range(repeats):
        start = perf_counter()
        current_results, current_operations = function()
        elapsed = perf_counter() - start

        times.append(elapsed)
        results = current_results
        operations = current_operations

    return {
        "results": sorted(results),
        "time": median(times),
        "operations": operations,
    }


def naive_combined_search(dictionary, pattern, required, excluded):
    """Reference implementation that applies all three clues."""

    results = []
    examined = 0

    for word in dictionary.words:
        examined += 1

        if pattern and not matches_constraints(
            word, "position", pattern=pattern
        ):
            continue

        if required and not matches_constraints(
            word, "required", required_letters=required
        ):
            continue

        if excluded and not matches_constraints(
            word, "excluded", excluded_letters=excluded
        ):
            continue

        results.append(word)

    return results, examined


def show_comparison(title, first_name, first, second_name, second):
    """Print timing and correctness for two equivalent searches."""

    print(f"\n{'-' * 65}")
    print(title)
    print("-" * 65)

    print(
        f"{first_name:<24} "
        f"{first['time'] * 1000:10.3f} ms"
        f" | Operations: {first['operations']:,}"
    )

    print(
        f"{second_name:<24} "
        f"{second['time'] * 1000:10.3f} ms"
        f" | Operations: {second['operations']:,}"
    )

    same_results = first["results"] == second["results"]

    print(f"Matching result sets: {'PASS' if same_results else 'FAIL'}")

    if same_results and second["time"] > 0:
        speedup = first["time"] / second["time"]
        print(f"Relative speed: {speedup:.2f}x")

    return same_results


def main():
    dictionary_path = Path(__file__).parent / "data" / "words.txt"

    if not dictionary_path.exists():
        print(f"Dictionary not found: {dictionary_path}")
        return

    words = load_dictionary(dictionary_path)
    dictionary = WordDictionary(words)

    print("=" * 65)
    print("             WORDLE SOLVER - ALGORITHM BENCHMARK")
    print("=" * 65)
    print(f"Dictionary size: {len(dictionary.words):,} words")
    print(f"Timing repetitions: {REPEATS}")
    print("Times shown are median execution times.")

    all_passed = True

    # TEST 1: Known positions — Naive vs Trie
    pattern = "_a_e_"

    naive_position = benchmark_function(
        lambda: naive_search(
            dictionary, "position", pattern=pattern
        )
    )

    trie_position = benchmark_function(
        lambda: trie_search(dictionary, pattern)
    )

    all_passed &= show_comparison(
        f"1. KNOWN POSITIONS | Pattern: {pattern}",
        "Naive search",
        naive_position,
        "Trie search",
        trie_position,
    )

    # TEST 2: Required letters — Naive vs Hash
    required = "ae"

    naive_required = benchmark_function(
        lambda: naive_search(
            dictionary, "required", required_letters=required
        )
    )

    hash_required = benchmark_function(
        lambda: hash_search(
            dictionary, "required", required_letters=required
        )
    )

    all_passed &= show_comparison(
        f"2. REQUIRED LETTERS | Letters: {required}",
        "Naive search",
        naive_required,
        "Hash search",
        hash_required,
    )

    # TEST 3: Excluded letters — Naive vs Hash
    excluded = "xyz"

    naive_excluded = benchmark_function(
        lambda: naive_search(
            dictionary, "excluded", excluded_letters=excluded
        )
    )

    hash_excluded = benchmark_function(
        lambda: hash_search(
            dictionary, "excluded", excluded_letters=excluded
        )
    )

    all_passed &= show_comparison(
        f"3. EXCLUDED LETTERS | Letters: {excluded}",
        "Naive search",
        naive_excluded,
        "Hash search",
        hash_excluded,
    )

    # TEST 4: All clues together — Reference vs Combined search
    pattern = "_a_e_"
    required = "r"
    excluded = "st"

    reference_combined = benchmark_function(
        lambda: naive_combined_search(
            dictionary, pattern, required, excluded
        )
    )

    actual_combined = benchmark_function(
        lambda: combined_search(
            dictionary, pattern, required, excluded
        )
    )

    all_passed &= show_comparison(
        "4. COMBINED SEARCH | Pattern: _a_e_, "
        "Required: r, Excluded: st",
        "Reference scan",
        reference_combined,
        "Combined search",
        actual_combined,
    )

    print(f"\n{'=' * 65}")
    print("FINAL RESULT")
    print("=" * 65)

    if all_passed:
        print("PASS: All algorithms returned matching result sets.")
    else:
        print("FAIL: At least one algorithm returned different results.")
        print("Check algorithms.py before trusting the benchmarks.")

    print("\nBenchmark complete.")


if __name__ == "__main__":
    main()
