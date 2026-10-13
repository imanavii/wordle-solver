# Wordle Solver — Algorithm Analysis

A Python-based command-line Wordle Solver that finds five-letter words matching positional clues, required letters, and excluded letters. The project demonstrates and compares multiple data structures and search algorithms, with a focus on correctness and execution-time optimization.

## Features

- **Known-position search:** Finds words matching a five-character pattern, such as `_a_e_`.
- **Required-letter search:** Finds words containing all specified letters.
- **Excluded-letter search:** Filters out words containing specified letters.
- **Combined search:** Applies multiple clues simultaneously.
- **Interactive CLI:** Accepts user input, supports repeated searches, and allows exiting at any prompt.
- **Performance benchmarking:** Compares search algorithms using execution time and result-equivalence checks.

## Project Structure

```text
wordle-solver/
├── data/
│   └── words.txt
├── results/
│   └── benchmark_results.csv
├── main.py
├── algorithms.py
├── benchmark.py
├── README.md
```

| File | Purpose |
|---|---|
| `main.py` | Loads the dictionary and handles the interactive CLI |
| `algorithms.py` | Implements the Trie, letter indexes, and search algorithms |
| `benchmark.py` | Benchmarks algorithms and checks result correctness |
| `data/words.txt` | Local five-letter word dictionary |
| `results.csv` | Saved benchmark measurements |

## Requirements

- Python 3.10 or later recommended
- A local dictionary at `data/words.txt`
- No external Python packages are required by the current implementation, assuming all modules use only the standard library.

## Setup and Execution

Clone or download the repository, then open a terminal in the project directory.


### Dictionary Setup

The dictionary file is not included in this repository. Download it before running the application.

**Windows (PowerShell)**

From the project root directory, run:

```powershell
New-Item -ItemType Directory -Force data
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words" `
  -OutFile "data/words.txt"
```

**macOS / Linux**

From the project root directory, run:

```bash
mkdir -p data
curl -L "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words" \
  -o data/words.txt
```

After downloading the dictionary, run the solver:

```bash
python main.py
```

Run the benchmark suite:

```bash
python benchmark.py
```
The application loads the local dictionary and filters it to unique, valid five-letter English-letter entries.


The dictionary must be available at `data/words.txt`. If it is missing, the application will report an error.

## How to Use

The solver requests clues in sequence:

1. **Known positions:** Enter a five-character pattern, such as `_a_e_`.
2. **Known letters:** Enter letters that must appear in the word, such as `r, t`.
3. **Excluded letters:** Enter letters that must not appear, such as `s, o`.

Press Enter to skip optional fields. If both known positions and known letters are skipped, at least one excluded letter must be entered.

The solver applies all supplied constraints simultaneously and displays matching words. After each search, choose whether to solve again or exit.

Type `EXIT` at any input prompt to quit.

## Algorithms and Data Structures

### 1. Naive Search

Examines every word in the dictionary and checks whether it satisfies the requested constraint.

- Simple baseline implementation
- Useful for verifying optimized algorithms
- Time complexity: \(O(NL)\) per search, where \(N\) is the number of words and \(L\) is the word length

### 2. Trie-Based Search

Stores words in a prefix tree. Each level represents a character position, and known letters restrict which branches are explored.

- Effective for positional patterns
- Avoids examining every dictionary word individually
- Performance depends on the pattern and number of Trie nodes visited

### 3. Hash-Index Search

Maintains indexes mapping letters to the words containing them.

- Required-letter searches intersect the relevant indexed sets
- Excluded-letter searches remove words containing unwanted letters
- Performance depends on the sizes of the relevant sets and their filtering costs

### 4. Combined Search

Combines positional and letter-based constraints:

1. Retrieves positional matches from the Trie when a pattern is supplied.
2. Intersects candidate sets for required letters.
3. Removes words containing excluded letters.
4. Sorts and returns the final candidates.

This reduces unnecessary dictionary-wide scanning for the tested combination of clues.

## Benchmark Results

The following results were recorded during development using a dictionary of 14,855 words and five timing repetitions per search. Times are median execution times.

| Search | Reference Time | Optimized Time | Speedup |
|---|---:|---:|---:|
| Known positions | 15.285 ms | 0.246 ms | 62.26× |
| Required letters | 13.086 ms | 1.147 ms | 11.41× |
| Excluded letters | 14.201 ms | 2.626 ms | 5.41× |
| Combined search | 17.906 ms | 0.298 ms | 60.07× |

All four benchmark comparisons passed their result-equivalence checks.

**Combined-search optimization:** The recorded runtime decreased from 16.975 ms before optimization to 0.298 ms after optimization, approximately a 98.24% reduction for the tested input.

These are development measurements, not guaranteed performance figures. Results can vary with the machine, Python version, dictionary, and input constraints. The individual search comparisons and combined-search before/after comparison were recorded in different runs.

The benchmark's reported count for the optimized combined search represents final candidates, whereas the reference count represents words examined. These counts are not directly comparable as operation counts.

## Correctness and Limitations

- Optimized searches are checked against reference implementations.
- Benchmark inputs cover selected examples rather than every possible clue combination.
- The dictionary may contain uncommon words that are not accepted as guesses in the official Wordle game.
- Execution-time measurements do not include every possible cost, such as initial dictionary loading and index construction, unless explicitly measured.

## Future Improvements

- Automatically export each benchmark run to CSV.
- Test multiple clue combinations and dictionary sizes.
- Measure memory usage and preprocessing time.
- Add automated unit tests for edge cases and invalid inputs.
- Separate common Wordle answers from the broader dictionary.
- Add visualizations of algorithm runtime comparisons.

## Conclusion

The Wordle Solver demonstrates how appropriate data structures can improve search efficiency. Trie-based positional matching and hash-index filtering reduce search time compared with naive scanning, while combined search applies multiple clues efficiently. Benchmarking and correctness checks provide a foundation for analyzing the trade-offs between the implemented approaches.

---

**Project:** Wordle Solver  
**Language:** Python  
**Focus:** Data Structures and Algorithms, search optimization, and benchmarking
