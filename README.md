# spbu-se2020-formal-languages
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=master)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

This repository consists of assignments of formal languages theory course in SPBU

## Task 01 

The basic tests on automata intersection in ```pyformlang``` and matrix multiplication in ```pygraphblas``` libraries. 

First of all, install package manager [Miniconda](https://docs.conda.io/en/latest/miniconda.html "Miniconda installation"). Then install libraries by following commands:
 ```
  conda create -q -n test-environment python=3.8 pygraphblas pytest
  conda activate test-environment
  pip install pyformlang 
 ```

After installation, run tests by ```python -m pytest``` 

## Task 02

Implementation of automaton intersection via tensor product

To install libraries see instructions in <strong>Task 01</strong> section

```
usage: main.py [-h] [--from_v_path START_VERTICES_PATH] [--to_v_path END_VERTICES_PATH] graph_path regex_path

positional arguments:
  graph_path            Path of file with edge list. Format: <vertice> <label> <vertice>
  regex_path            Path of file with regexp

optional arguments:
  -h, --help            show this help message and exit
  --from_v_path START_VERTICES_PATH
                        Path of file with set of starting vertices.
  --to_v_path END_VERTICES_PATH
                        Path of file with set of ending (final) vertices.
```

## Task 04
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task04)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

Implementation of CYK and Hellings Context-free path querying algorithms.
You can see CYK realisation in `CFGrammar.py` and Hellings realisation in `cfpq.py` both in `src` folder

See installation and tests running instrunctions in <strong>Task 01</strong> section

## Task 05
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task05)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

Implementation of two cfpq algorithms which could be named as matrix and tensor algorithms.
You can see both these realisations in `cfpq.py` in `src`

See installation and tests running instrunctions in <strong>Task 01</strong> section

## Task 06
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task06)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

Report for benchmarking CFPQ algorithms can be found in `results_cfpq_benchmark.ipynb`. Exact numerical results can be found at the end of the file.

Script for benchmarking can be found in `src/benchmark_cfpq`. To run this script use `python3 -m src.benchmark_cfpq` from root directory.

## Task 07
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task07)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

Implemented syntax and syntax analyzer using CYK algorithm. 
Syntax definition can be found in `src/syntax/syntax.txt` with tokens in `src/syntax/tokens.txt`.
Syntax analyzer can be found in `src/SyntaxAnalyzer`.

The information about syntax can be found [here](src/syntax/README.md)

## Task 08
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task08)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

Added ANTLR grammar for database language. Also added visualization of script's AST.
### Install

```
 sudo apt-get update
 sudo apt-get install antlr4
 pip install antlr4-python3-runtime
 cd src/antlr && antlr4 -Dlanguage=Python3 DbQLGrammar.g4 
 cd ../../
```

### Using
To generate DOT file use
```
 usage: dot_visualization.py [-h] -s SCRIPT_FILE -o OUTPUT_FILE

 The script visualize input Database script in DOT format

 optional arguments:
   -h, --help      show this help message and exit
   -s SCRIPT_FILE  path to script file
   -o OUTPUT_FILE  path to output DOT file
```
### Example

Example: `python -m src.dot_visualization -s=src/syntax/example_script.txt -o=antlr_example_res`

Result of this example can be found [here](https://github.com/KanashinDmitry/spbu-se2020-formal-languages/blob/Task08/antlr_example_res.pdf)
