from typing import Dict
from typing import List
from src.Instance import Instance
import numpy as np


class InstanceRetriever():
    
    JOB_NUMBER_INDEX = 0
    MACHINE_NUMBER_INDEX = 1
    WORKERS_NUMBER_INDEX = 2
    TIME_HORIZON_INDEX = 3
    
    def __init__(self, path_file: str) -> None:
        self.path = path_file
    
    def get_instance(self) -> Instance:
        lines = [line.rstrip("\n").split("\t") for line in self.__get_text_file_lines()]
        
        self.njobs = int(lines[self.JOB_NUMBER_INDEX][0])
        self.nmachines = int(lines[self.MACHINE_NUMBER_INDEX][0]) 
        self.nworkers = int(lines[self.WORKERS_NUMBER_INDEX][0])
        self.max_days = int(lines[self.TIME_HORIZON_INDEX][0])  
        
        instance = Instance(self.njobs, self.nmachines, self.nworkers, self.max_days)
        
        initial_indexes = self.__get_initial_indexes()
        instance.Mj = InstanceRetriever.__process_lines(lines[initial_indexes["Mj"]:initial_indexes["Mj"] + self.njobs])
        instance.Kj = InstanceRetriever.__process_lines(lines[initial_indexes["Kj"]:initial_indexes["Kj"] + self.njobs])
        instance.Ki = InstanceRetriever.__process_lines(lines[initial_indexes["Ki"]:initial_indexes["Ki"] + self.nmachines])
        instance.rj = InstanceRetriever.__process_line(lines[initial_indexes["rj"]])
        instance.dj = InstanceRetriever.__process_line(lines[initial_indexes["dj"]])
        instance.qj = InstanceRetriever.__process_line(lines[initial_indexes["qj"]])
        instance.wj = InstanceRetriever.__process_line(lines[initial_indexes["wj"]])
        instance.pj = InstanceRetriever.__process_line(lines[initial_indexes["pj"]])
        instance.ukt = InstanceRetriever.__process_lines(lines[initial_indexes["ukt"]: initial_indexes["ukt"] + self.nworkers])
        
        if int(lines[initial_indexes["P"]][0]) != 0:
            instance.P = InstanceRetriever.__process_lines(lines[initial_indexes["P"] + 1 : initial_indexes["P"] + 1 + int(lines[initial_indexes["P"]][0])])
        else:
            instance.P = np.array([])
        initial_indexes["Q"] = initial_indexes["P"] + 1 + int(lines[initial_indexes["P"]][0]) 
        if int(lines[initial_indexes["Q"]][0]) != 0:
            instance.Q = InstanceRetriever.__process_lines(lines[initial_indexes["Q"] + 1 : initial_indexes["Q"] + 1 + int(lines[initial_indexes["Q"]][0])])
        else:
            instance.Q = np.array([])
        return instance

    def __get_initial_indexes(self) -> Dict[str, int]:
        initial_indexes = dict()
        initial_indexes["Mj"] = self.TIME_HORIZON_INDEX + 1
        initial_indexes["Kj"] = initial_indexes["Mj"] + self.njobs
        initial_indexes["Ki"] = initial_indexes["Kj"] + self.njobs
        initial_indexes["rj"] = initial_indexes["Ki"] + self.nmachines
        initial_indexes["dj"] = initial_indexes["rj"] + 1
        initial_indexes["qj"] = initial_indexes["dj"] + 1
        initial_indexes["wj"] = initial_indexes["qj"] + 1
        initial_indexes["pj"] = initial_indexes["wj"] + 1
        initial_indexes["ukt"] = initial_indexes["pj"] + 1
        initial_indexes["P"] = initial_indexes["ukt"] + self.nworkers
        return initial_indexes
    
    def __get_text_file_lines(self) -> List[str]:
        with open(self.path, mode="r") as f:
            return f.readlines()
    
    def __process_line(line: List[str]) -> np.array:
        return np.array([int(value) for value in line if value != ""])
    
    def __process_lines(lines: List[List[str]]) -> np.ndarray:
        processed_lines = [InstanceRetriever.__process_line(line) for line in lines]
        return np.array(processed_lines)
    
