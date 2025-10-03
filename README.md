# MC859-Runner
A wrapper to help running the experiments.

## How to use it
Just simply put the files on the parent directory of your project and create an `instances` folder if there isn't one.

### Solver.py
A dummy Solver class with a `solve` method that returns the solution for a given problem.

### main.py
This is the main function that will read the input from `runner.py`, build the problem instance (currently an SC-QBF instance) and solve this instance using `Solver.py`. As is, `Solver.py` has to be on the same directory as `main.py`, but if you reference the path/package correctly you can change this as needed.

#### Instance format
<n>                       # Instance Size
<s1> <s2> <s3> ... <sn>   # Subsets sizes
<S1>                      # Subset elements
<S2>
<S3>
...
<Sn>
<a11> <a12> ... <a1n>     # Matrix in upper triangular form
<a22> <a23> ... <a2n>
<a33> <a34> ... <a3n>
<ann>

### runner.py

This is a wrapper for `main.py` that runs multiple instances from an `instances` directory in parallel with a *minutes* time limit and output logs on a `logs_dir` directory (*logs* by default), you can change the output directory as needed. The `instances` directory and `main.py` have to be on the same directory as `runner.py`. The `logs_dir` directory will be created on the parent directory. The logs directory will be cleaned at the start of `runner.py` every time.

As is, the log files will only contain the `Finished in [...]` and `Final Solution [solution]` (from `main.py`) or `Execution time out [...]`  messages. For anything else add it in `main.py` or on the solver itself accordingly, but make sure to set flush to True or it won't appear on the log file if the instance times out. 

Note that if the instance exceeds the time limit it will not log anything past `solver.solve()`. Also note that only the outputs from `runner.py`will be shown in terminal, all other outputs will be redirected to the respective log file.