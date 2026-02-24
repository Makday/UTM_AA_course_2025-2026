### Requirements

You need to install necessary dependencies from requirements.txt, located a level above this folder
```pip install requirements.txt```

### Description

This folder contains source codes, here's what they do:
- benchmark.cpp - the main program, it produces 3 sets of 30 arrays with sizes equally distributed in range(100_000, 1_000_000). 
One set has arrays with random elements, one has them all sorted and the last one has them sorted in reverse. 
They are all saved in "/inputs". The program then benchmarks algorithms from "/algorithms" on these sets and outputs the execution time in "outputs/benchmark.txt".
- graph.py - parses "outputs/benchmark.txt" and generates graphs based on the data. These graphs are saved in "/outputs".
- generate_animated.cpp - prompts the user to introduce an array of elements. Then, it performs the algorithms on the input array and  logs every step they did on the array, the results are saved in "outputs/animations.txt".
- animate.py - parses "outputs/animations.txt" and produces an animation with every algorithm in the file. The animation is only interpreting the taken steps, it does not perform any sorting algorithms inside itself.

### Useful commands

To compile all .cpp files, run:
```
mingw32-make
```

To compile benchmark.cpp only, run:
```
mingw32-make benchmark
```

To compile generate_animated.cpp only, run:
```
mingw32-make benchmark
```

To delete all executables, run:
```
mingw32-make clean
```