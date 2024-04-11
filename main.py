from src.ModelEvaluator import ModelEvaluator
from src.MachineScheduler import MILPAdvanced
from src.InstanceMeta import SyntheticInstanceMeta

import os
import logging

OUTPUT_PATH = "results/results_milp_advanced.csv"


def main():
    logging.basicConfig(filename="log\\log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(module)s %(name)s %(message)s")
    logging.debug("Start main execution")
    evaluator = ModelEvaluator(MILPAdvanced, OUTPUT_PATH)
    evaluator.evaluate_all_instances(SyntheticInstanceMeta)


if __name__ == '__main__':
    main()
