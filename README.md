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
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task02)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

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
