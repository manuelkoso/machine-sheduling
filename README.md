# Mathematical optimisation - Project 

This repository contains the implementation of the integer linear programming models (MILP and MILP+) described in the following article: [Exact algorithms for a parallel machine scheduling problem with workforce and contiguity constraints](https://doi.org/10.1016/j.cor.2023.106484).

## Folder structure

- `src`: code source folder
- `data`: instances [shared](https://github.com/regor-unimore/Parallel-Machine-Scheduling-with-Contiguity) by the authors 
  - `random`: synthetic instances
  - `real`: real instances
- `output`: results obtained by the optimization process

## Setup and Execution

In order to install all the dependencies, run:

```commandline
pip install -r requirements.txt
```

In the `src/config` folder there is a `evaluator.json` file, where to specify
which instances will be included in the optimization process.

It follows a code snippet on how to run the optimization for
synthetic instances (placed in the `data/random` folder) for both models. In order to 
optimize real instance, replace the `evaluate_all_instances` argument with 
`RealInstanceMeta`

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

Notice that the execution will also produce a `log` folder containing a log
file of the execution.