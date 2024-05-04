# Mathematical optimisation - Project 

This repository contains the implementation of the two methods that use integer linear programming (MILP and MILP+) described in the following article: [Exact algorithms for a parallel machine scheduling problem with workforce and contiguity constraints](https://doi.org/10.1016/j.cor.2023.106484).

<!-- TOC -->
* [Mathematical optimisation - Project](#mathematical-optimisation---project-)
  * [Folder structure](#folder-structure)
  * [Data](#data)
  * [Configuration](#configuration)
  * [Setup and Execution](#setup-and-execution)
<!-- TOC -->

## Folder structure

- `src`: code source folder
- `data`: instances [shared](https://github.com/regor-unimore/Parallel-Machine-Scheduling-with-Contiguity) by the authors 
- `output`: results obtained by the optimization process

## Setup and Execution

In order to install all the dependencies, run:

```commandline
pip install -r requirements.txt
```

In the `src/config` folder there is `evaluator.json`, a config file where to specify
which instances (see `data` folder) will be included in the optimization process.

It follows a code snippet on how to run the optimization for
synthetic instances (placed in the `data/random` folder) for both models.

```python
from src.ModelEvaluator import ModelEvaluator
from src.MachineScheduler import MILP, MILPAdvanced
from src.InstanceMeta import SyntheticInstanceMeta

ModelEvaluator(scheduler_class=MILP, output_path="milp.csv").evaluate_all_instances(
        SyntheticInstanceMeta)

ModelEvaluator(scheduler_class=MILPAdvanced,
                   output_path="milp_plus.csv").evaluate_all_instances(SyntheticInstanceMeta)
```

This code snippet is also in the `main.py` file. In order to execute it, run the following command line:

```commandline
python main.py
```

Notice that the execution will produce also a `log` folder containing a log
file of the execution.