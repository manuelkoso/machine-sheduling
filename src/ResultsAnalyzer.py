from statistics import mean
from typing import Tuple, List

import pandas as pd


class ResultsAnalyzer:
    MILP_RESULTS_PATH = "output\\results_milp.csv"
    MILP_ADVANCED_RESULTS_PATH = "output\\results_milp_advanced.csv"

    def __init__(self) -> None:
        self.data_milp = pd.read_csv(self.MILP_RESULTS_PATH)
        self.data_milp_advanced = pd.read_csv(self.MILP_ADVANCED_RESULTS_PATH)

    def get_vars_mean(self, J_M_K: Tuple[int, int, int]) -> float:
        J, M, K = J_M_K
        results = self.data_milp.loc[
            (self.data_milp["number_of_jobs"] == J) & (self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                         "number_of_workers"] == K)]
        return mean(results["number_of_variables"])

    def __get_optimum_instances(self, J_M_K: Tuple[int, int, int]) -> pd.DataFrame:
        J, M, K = J_M_K
        milp_versions = self.data_milp.loc[
            (self.data_milp["optimum_reached"] == True) & (self.data_milp["number_of_jobs"] == J) & (
                        self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                          "number_of_workers"] == K)]["version"]
        milp_advanced_versions = self.data_milp.loc[
            (self.data_milp["optimum_reached"] == True) & (self.data_milp["number_of_jobs"] == J) & (
                    self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                     "number_of_workers"] == K)]["version"]
        versions = pd.merge(milp_versions, milp_advanced_versions)
        return versions

    def get_constrs_mean(self, J_M_K: Tuple[int, int, int]):
        J, M, K = J_M_K
        results = self.data_milp.loc[
            (self.data_milp["number_of_jobs"] == J) & (self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                         "number_of_workers"] == K)]
        return mean(results["number_of_constraints"])

    def get_nzs_mean(self, J_M_K: Tuple[int, int, int]):
        J, M, K = J_M_K
        results = self.data_milp.loc[
            (self.data_milp["number_of_jobs"] == J) & (self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                         "number_of_workers"] == K)]
        return mean(results["nzs"])

    def get_LP_mean(self, J_M_K: Tuple[int, int, int]):
        J, M, K = J_M_K
        results = self.data_milp.loc[
            (self.data_milp["number_of_jobs"] == J) & (self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                         "number_of_workers"] == K)]
        return mean(results["LP"])

    def get_opt_count(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                      J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    def get_run_time_mean(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                          J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    def get_opt_run_time_mean(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                              J_K_ratio: int = None, M_K_ratio: int = None):
        pass
