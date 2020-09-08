# spbu-se2020-formal-languages
This repository consists of assignments of formal languages theory course in SPBU

## Task 01 
[![Build Status](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages.svg?branch=Task01)](https://travis-ci.com/KanashinDmitry/spbu-se2020-formal-languages)

The basic tests on automata intersection in ```pyformlang``` and matrix multiplication in ```pygraphblas``` libraries. 

First of all, install package manager [Miniconda](https://docs.conda.io/en/latest/miniconda.html "Miniconda installation"). Then install libraries by following commands:
 ```
  conda create -q -n test-environment python=3.8 pygraphblas pytest
  conda activate test-environment
  pip install pyformlang 
 ```

After installation, run tests by ```pytest``` 
