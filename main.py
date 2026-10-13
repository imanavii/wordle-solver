from pathlib import Path

from algorithms import (
    WORD_LENGTH,
    WordDictionary,
    combined_search,
)

# LOAD DICTIONARY

def load_dictionary(file_path):
    """Load unique, valid five-letter words from a local file."""

    words = set()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip().lower()

            if (
                len(word) == WORD_LENGTH
                and word.isascii()
                and word.isalpha()
            ):
                words.add(word)

    if not words:
        raise ValueError(
            "No valid five-letter words found in data/words.txt."
        )

    return sorted(words)


def initialize():
    """Load the dictionary and build indexes once."""

    dictionary_path = Path(__file__).parent / "data" / "words.txt"

    if not dictionary_path.exists() or dictionary_path.stat().st_size == 0:
        raise FileNotFoundError(
            f"Dictionary not found or empty: {dictionary_path}\n"
            "Add a word list to data/words.txt before running the solver."
        )

    words = load_dictionary(dictionary_path)
    dictionary = WordDictionary(words)

    print(f"\nDictionary loaded: {len(dictionary.words)} five-letter words")
    return dictionary


# INPUT VALIDATION

def read_input(prompt):
    """Read input and allow EXIT at every prompt."""

    value = input(prompt).strip().lower()

    if value == "exit":
        raise SystemExit

    return value


def get_pattern():
    """Read an optional five-character pattern."""

    while True:
        pattern = read_input(
            "1. Known positions (e.g. _a_e_): "
        )

        if not pattern:
            return ""

        if (
            len(pattern) == WORD_LENGTH
            and all(char == "_" or "a" <= char <= "z"
                    for char in pattern)
        ):
            return pattern

        print("Invalid pattern. Use exactly five letters/underscores, "
              "e.g. _a_e_. Try again.")


def get_letters(prompt, required=False):
    """Read an optional comma-separated list of letters."""

    while True:
        letters = read_input(prompt)
        letters = letters.replace(",", "").replace(" ", "")

        if not letters:
            if required:
                print("This field is required. Please enter at least "
                      "one letter.")
                continue
            return ""

        if letters.isascii() and letters.isalpha():
            return letters

        print("Invalid input. Enter English letters A-Z only.")


# DISPLAY RESULTS

def display_results(results):
    print(f"\nMatching words: {len(results)}")

    if not results:
        print("No matching words found.")
        return

    for start in range(0, len(results), 10):
        print("  ".join(results[start:start + 10]))


# SOLVER

def run_solver(dictionary):
    while True:
        print("\n" + "=" * 42)
        print("              WORDLE SOLVER")
        print("=" * 42)
        print("Enter your clues in sequence.")
        print("Press Enter to skip an optional field.")
        print("Type EXIT at any prompt to quit.\n")

        try:
            # 1. Known positions
            pattern = get_pattern()

            # 2. Known letters
            required = get_letters(
                "2. Known letters (e.g. a, r, e): "
            )

            # 3. Excluded letters
            # Mandatory only when both earlier fields were skipped.
            excluded = get_letters(
                "3. Excluded letters (e.g. s, t, o): ",
                required=not pattern and not required,
            )

            # Search with every supplied constraint simultaneously.
            print("\nSearching with all supplied clues...")

            results, candidates_examined = combined_search(
                dictionary,
                pattern,
                required,
                excluded,
            )

            print(f"Candidates: {candidates_examined}")
            display_results(results)

            # Ask what to do after every search.
            while True:
                again = read_input(
                    "\nSolve again? (Y/N): "
                )

                if again in ("y", "yes"):
                    break

                if again in ("n", "no"):
                    print("Goodbye!")
                    return

                print("Please enter Y or N.")

        except SystemExit:
            print("\nGoodbye!")
            return

        except KeyboardInterrupt:
            print("\nGoodbye!")
            return


def main():
    try:
        dictionary = initialize()
        run_solver(dictionary)

    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
