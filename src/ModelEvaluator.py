import json
from typing import Dict, Any

from .MachineScheduler import MachineScheduler
from .InstanceMeta import SyntheticInstanceMeta, InstanceMeta
from .InstanceRetriever import InstanceRetriever

import pandas as pd
import gurobipy as gp
import logging

from src import Instance


class ModelEvaluator:
    CONFIG_PATH = "src\\config\\evaluator.json"
    RESULT_MODEL_COLUMNS = ["number_of_jobs", "number_of_machines", "number_of_workers",
                            "optimum_reached", "T(s)", "T_opt(s)", "LP", "number_of_variables", "number_of_constraints",
                            "nzs"]
    OUT_OF_MEMORY_DEFAULT_TIME = 3600

    def __init__(self, scheduler_class: MachineScheduler.__class__):
        self.scheduler_class = scheduler_class

    def evaluate_all_instances(self, instance_meta_class) -> pd.DataFrame:
        logging.debug("Start evaluation, instance type: " + str(instance_meta_class))
        results = pd.DataFrame()

        instances_params = self.__get_instances_params(instance_meta_class)
        versions = instances_params["versions"]
        for instance_params in instances_params["params"]:
            results = pd.concat(
                [results, self.evaluate_all_instance_version(instance_meta_class, versions, instance_params)],
                ignore_index=True)

        return results

    def evaluate_all_instance_version(self, instance_meta_class, versions, instance_params) -> pd.DataFrame:
        results = pd.DataFrame()

        for version in versions:
            instance_params["version"] = version
            instance_meta: InstanceMeta = instance_meta_class(**instance_params)
            logging.debug("Evaluation instance " + str(instance_meta))

            instance = InstanceRetriever.get_instance(instance_meta)
            instance_results = self.evaluate_instance(instance)
            instance_results["version"] = version
            instance_results["number_of_projects"] = instance_meta.get_params()[
                "number_of_projects"] if instance_meta_class is not SyntheticInstanceMeta else None
            results = pd.concat([results, pd.DataFrame(instance_results, index=[0])], ignore_index=True)

        return results

    def evaluate_instance(self, instance: Instance):
        scheduler: MachineScheduler = self.scheduler_class(instance)
        try:
            scheduler.build_model()
            scheduler.run()
            return self.__get_results_from_model(scheduler)
        except (MemoryError, gp.GurobiError):
            return self.__out_of_memory_results()

    def __get_instances_params(self, instance_meta_class):
        json_field = "synthetic" if instance_meta_class is SyntheticInstanceMeta else "real"
        with open(self.CONFIG_PATH) as fp:
            return json.load(fp)[json_field]

    def __get_results_from_model(self, scheduler: MachineScheduler) -> Dict[str, Any]:
        values = [len(scheduler.instance.J), len(scheduler.instance.M), len(scheduler.instance.K),
                  scheduler.model.getAttr("status") == gp.GRB.OPTIMAL, scheduler.model.getAttr("Runtime"),
                  scheduler.model.getAttr("Runtime") if scheduler.model.getAttr(
                      "status") == gp.GRB.OPTIMAL else self.OUT_OF_MEMORY_DEFAULT_TIME,
                  scheduler.model.getAttr("ObjVal"), scheduler.model.getAttr("NumVars"),
                  scheduler.model.getAttr("NumConstrs"),
                  scheduler.model.getA().count_nonzero()]

        return dict(zip(self.RESULT_MODEL_COLUMNS, values))

    def __out_of_memory_results(self):
        values = [None] * len(self.RESULT_MODEL_COLUMNS)
        result = dict(zip(self.RESULT_MODEL_COLUMNS, values))
        result["T(s)"] = self.OUT_OF_MEMORY_DEFAULT_TIME
        return result
