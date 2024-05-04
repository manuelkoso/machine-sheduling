import logging

from src.ModelEvaluator import ModelEvaluator
from src.MachineScheduler import MILP, MILPAdvanced
from src.enum.InstanceType import InstanceType


def main():
    logging.basicConfig(filename="log\\log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(module)s %(name)s %(message)s")
    logging.debug("Start main execution")

    ModelEvaluator(scheduler_class=MILP, output_path="output/realistic/milp_real.csv").evaluate_all_instances(
        InstanceType.SYNTHETIC)
    ModelEvaluator(scheduler_class=MILPAdvanced,
                   output_path="output/realistic/milp_plus_real.csv").evaluate_all_instances(InstanceType.SYNTHETIC)


if __name__ == '__main__':
    main()
