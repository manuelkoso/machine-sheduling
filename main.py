from src.ModelEvaluator import ModelEvaluator
from src.MachineScheduler import MILP
from src.InstanceMeta import SyntheticInstanceMeta
import os
import logging

OUTPUT_PATH = "results/results.csv"


def main():
    logging.basicConfig(filename="log\\log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(module)s %(name)s %(message)s")
    logging.debug("Start main execution")
    evaluator = ModelEvaluator(MILP)
    results = evaluator.evaluate_all_instances(SyntheticInstanceMeta)

    if os.path.isfile(OUTPUT_PATH):
        results.to_csv(OUTPUT_PATH, mode='a', header=False)
    else:
        results.to_csv(OUTPUT_PATH)


if __name__ == '__main__':
    main()
