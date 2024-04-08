from typing import Dict
from typing import List
from .Instance import Instance
from .InstanceMeta import InstanceMeta
from .PathBuilder import PathBuilder
import numpy as np
import logging


class InstanceRetriever:
    JOB_NUMBER_INDEX = 0
    MACHINE_NUMBER_INDEX = 1
    WORKERS_NUMBER_INDEX = 2
    TIME_HORIZON_INDEX = 3

    @staticmethod
    def get_instance(instance_meta: InstanceMeta) -> Instance:
        logging.debug("Instance retrieving")
        file_path = PathBuilder.build_file_path(instance_meta)
        lines = [InstanceRetriever.__line_processing(line) for line in
                 InstanceRetriever.__get_text_file_lines(file_path)]

        number_of_jobs = int(lines[InstanceRetriever.JOB_NUMBER_INDEX][0])
        number_of_machines = int(lines[InstanceRetriever.MACHINE_NUMBER_INDEX][0])
        number_of_workers = int(lines[InstanceRetriever.WORKERS_NUMBER_INDEX][0])
        time_horizon = int(lines[InstanceRetriever.TIME_HORIZON_INDEX][0])

        instance = Instance(number_of_jobs, number_of_machines, number_of_workers, time_horizon)
        InstanceRetriever.__setup_instance_parameters(instance, lines)

        return instance

    @staticmethod
    def __setup_instance_parameters(instance, lines):
        initial_indexes = InstanceRetriever.__get_initial_indexes(len(instance.J), len(instance.M), len(instance.K))
        instance.Mj = InstanceRetriever.__process_lines(
            lines[initial_indexes["Mj"]:initial_indexes["Mj"] + len(instance.J)])
        instance.Kj = InstanceRetriever.__process_lines(
            lines[initial_indexes["Kj"]:initial_indexes["Kj"] + len(instance.J)])
        instance.Ki = InstanceRetriever.__process_lines(
            lines[initial_indexes["Ki"]:initial_indexes["Ki"] + len(instance.M)])
        instance.rj = InstanceRetriever.__process_line(lines[initial_indexes["rj"]])
        instance.dj = InstanceRetriever.__process_line(lines[initial_indexes["dj"]])
        instance.qj = InstanceRetriever.__process_line(lines[initial_indexes["qj"]])
        instance.wj = InstanceRetriever.__process_line(lines[initial_indexes["wj"]])
        instance.pj = InstanceRetriever.__process_line(lines[initial_indexes["pj"]])
        instance.ukt = InstanceRetriever.__process_lines(
            lines[initial_indexes["ukt"]: initial_indexes["ukt"] + len(instance.K)])
        if int(lines[initial_indexes["P"]][0]) != 0:
            instance.P = InstanceRetriever.__process_lines(
                lines[initial_indexes["P"] + 1: initial_indexes["P"] + 1 + int(lines[initial_indexes["P"]][0])])
        else:
            instance.P = np.array([])
        initial_indexes["Q"] = initial_indexes["P"] + 1 + int(lines[initial_indexes["P"]][0])
        if int(lines[initial_indexes["Q"]][0]) != 0:
            instance.Q = InstanceRetriever.__process_lines(
                lines[initial_indexes["Q"] + 1: initial_indexes["Q"] + 1 + int(lines[initial_indexes["Q"]][0])])
        else:
            instance.Q = np.array([])

    @staticmethod
    def __line_processing(line):
        return line.rstrip("\n").split("\t")

    @staticmethod
    def __get_initial_indexes(number_of_jobs: int, number_of_machines: int, number_of_workers: int) -> Dict[
        str, int]:
        initial_indexes = dict()
        initial_indexes["Mj"] = InstanceRetriever.TIME_HORIZON_INDEX + 1
        initial_indexes["Kj"] = initial_indexes["Mj"] + number_of_jobs
        initial_indexes["Ki"] = initial_indexes["Kj"] + number_of_jobs
        initial_indexes["rj"] = initial_indexes["Ki"] + number_of_machines
        initial_indexes["dj"] = initial_indexes["rj"] + 1
        initial_indexes["qj"] = initial_indexes["dj"] + 1
        initial_indexes["wj"] = initial_indexes["qj"] + 1
        initial_indexes["pj"] = initial_indexes["wj"] + 1
        initial_indexes["ukt"] = initial_indexes["pj"] + 1
        initial_indexes["P"] = initial_indexes["ukt"] + number_of_workers
        return initial_indexes

    @staticmethod
    def __get_text_file_lines(path: str) -> List[str]:
        with open(path, mode="r") as f:
            return f.readlines()

    @staticmethod
    def __process_line(line: List[str]) -> np.array:
        return np.array([int(value) for value in line if value != ""])

    @staticmethod
    def __process_lines(lines: List[List[str]]) -> np.ndarray:
        processed_lines = [InstanceRetriever.__process_line(line) for line in lines]
        return np.array(processed_lines)
