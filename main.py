from src.ModelEvaluator import ModelEvaluator
from src.MachineScheduler import MILPAdvanced
from src.InstanceMeta import SyntheticInstanceMeta
from src.ResultsAnalyzer import ResultsAnalyzer

import os
import logging

OUTPUT_PATH = "output/results_milp_advanced.csv"


def main():
    logging.basicConfig(filename="log\\log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(module)s %(name)s %(message)s")
    logging.debug("Start main execution")
    # evaluator = ModelEvaluator(MILPAdvanced, OUTPUT_PATH)
    # evaluator.evaluate_all_instances(SyntheticInstanceMeta)
    J_M_K = (50, 5, 3)
    analyzer = ResultsAnalyzer()
    print(analyzer.get_vars_mean(J_M_K))
    print(analyzer.get_LP_mean(J_M_K))
    print(analyzer.get_nzs_mean(J_M_K))
    print(analyzer.get_constrs_mean(J_M_K))


if __name__ == '__main__':
    main()
