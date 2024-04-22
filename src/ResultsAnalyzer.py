from statistics import mean
from typing import Tuple, List

import pandas as pd


class ResultsAnalyzer:
    MILP_RESULTS_PATH = "output\\results_milp.csv"
    MILP_ADVANCED_RESULTS_PATH = "output\\results_milp_advanced.csv"

    def __init__(self) -> None:
        self.data_milp = pd.read_csv(self.MILP_RESULTS_PATH)
        self.data_milp_advanced = pd.read_csv(self.MILP_ADVANCED_RESULTS_PATH)

    def get_vars_mean(self, J_M_K: Tuple[int, int, int]) -> Tuple[float, float]:
        J, M, K = J_M_K
        optimum_versions = self.__get_optimum_instances(J_M_K)
        results_milp = self.data_milp.loc[(self.data_milp["version"].isin(optimum_versions["version"])) &
                                          (self.data_milp["number_of_jobs"] == J) & (
                                                  self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                    "number_of_workers"] == K)]
        results_milp_advanced = self.data_milp_advanced.loc[
            (self.data_milp_advanced["version"].isin(optimum_versions["version"])) &
            (self.data_milp_advanced["number_of_jobs"] == J) & (
                    self.data_milp_advanced["number_of_machines"] == M) & (self.data_milp_advanced[
                                                                               "number_of_workers"] == K)]
        return mean(results_milp["number_of_variables"]), mean(results_milp_advanced["number_of_variables"])

    def __get_optimum_instances(self, J_M_K: Tuple[int, int, int]) -> pd.DataFrame:
        J, M, K = J_M_K
        milp_versions = self.data_milp.loc[
            (self.data_milp["optimum_reached"] == True) & (self.data_milp["number_of_jobs"] == J) & (
                    self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                      "number_of_workers"] == K)]["version"]
        milp_advanced_versions = self.data_milp_advanced.loc[
            (self.data_milp_advanced["optimum_reached"] == True) & (self.data_milp_advanced["number_of_jobs"] == J) & (
                    self.data_milp_advanced["number_of_machines"] == M) & (self.data_milp_advanced[
                                                                               "number_of_workers"] == K)]["version"]
        versions = pd.merge(milp_versions, milp_advanced_versions)
        return versions

    def get_constrs_mean(self, J_M_K: Tuple[int, int, int]) -> Tuple[float, float]:
        J, M, K = J_M_K
        optimum_versions = self.__get_optimum_instances(J_M_K)
        milp_versions = self.data_milp.loc[(self.data_milp["version"].isin(optimum_versions["version"])) &
                                           (self.data_milp["number_of_jobs"] == J) & (
                                                   self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                     "number_of_workers"] == K)]
        milp_advanced_versions = self.data_milp_advanced.loc[
            (self.data_milp_advanced["version"].isin(optimum_versions["version"])) &
            (self.data_milp_advanced["number_of_jobs"] == J) & (
                    self.data_milp_advanced["number_of_machines"] == M) & (
                    self.data_milp_advanced[
                        "number_of_workers"] == K)]
        return mean(milp_versions["number_of_constraints"]), mean(milp_advanced_versions["number_of_constraints"])

    def get_nzs_mean(self, J_M_K: Tuple[int, int, int]):
        J, M, K = J_M_K
        optimum_versions = self.__get_optimum_instances(J_M_K)
        milp_versions = self.data_milp.loc[(self.data_milp["version"].isin(optimum_versions["version"])) &
                                           (self.data_milp["number_of_jobs"] == J) & (
                                                   self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                     "number_of_workers"] == K)]
        milp_advanced_versions = self.data_milp_advanced.loc[
            (self.data_milp_advanced["version"].isin(optimum_versions["version"])) &
            (self.data_milp_advanced["number_of_jobs"] == J) & (
                    self.data_milp_advanced["number_of_machines"] == M) & (self.data_milp_advanced[
                                                                               "number_of_workers"] == K)]
        return mean(milp_versions["nzs"]), mean(milp_advanced_versions["nzs"])

    def get_LP_mean(self, J_M_K: Tuple[int, int, int]):
        J, M, K = J_M_K
        optimum_versions = self.__get_optimum_instances(J_M_K)
        milp_versions = self.data_milp.loc[(self.data_milp["version"].isin(optimum_versions["version"])) &
                                           (self.data_milp["number_of_jobs"] == J) & (
                                                   self.data_milp["number_of_machines"] == M) & (self.data_milp[
                                                                                                     "number_of_workers"] == K)]
        milp_advanced_versions = self.data_milp_advanced.loc[
            (self.data_milp_advanced["version"].isin(optimum_versions["version"])) &
            (self.data_milp_advanced["number_of_jobs"] == J) & (
                    self.data_milp_advanced["number_of_machines"] == M) & (self.data_milp_advanced[
                                                                               "number_of_workers"] == K)]
        return mean(milp_versions["LP"]), mean(milp_advanced_versions["LP"])

    def get_opt_count(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                      J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    def get_run_time_mean(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                          J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    def get_opt_run_time_mean(self, p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                              J_K_ratio: int = None, M_K_ratio: int = None):
        pass
