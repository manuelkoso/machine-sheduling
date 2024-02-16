from itertools import islice
from src.Instance import Instance
import numpy as np


class InstanceRetriever():
    
    JOB_NUMBER_FILE_ROW_INDEX = 0
    MACHINE_NUMBER_FILE_ROW_INDEX = 1
    WORKERS_NUMBER_FILE_ROW_INDEX = 2
    TIME_HORIZON_FILE_ROW_INDEX = 3
    
    def __init__(self, path_file: str) -> None:
        self.path = path_file
    
    def get_instance(self) -> Instance:
        instance = Instance(self.__get_njobs(), self.__get_nmachines(), self.__get_nworkers(), self.__get_time_horizon())
        
    def __get_njobs(self) -> int:
        with open(self.path, mode="r") as f:
            for line in islice(f, self.JOB_NUMBER_FILE_ROW_INDEX, self.JOB_NUMBER_FILE_ROW_INDEX + 1):
                return int(line)
        
    def __get_nmachines(self) -> int:
        with open(self.path, mode="r") as f:
            for line in islice(f, self.MACHINE_NUMBER_FILE_ROW_INDEX, self.MACHINE_NUMBER_FILE_ROW_INDEX + 1):
                return int(line)
    
    def __get_nworkers(self) -> int:
        with open(self.path, mode="r") as f:
            for line in islice(f, self.WORKERS_NUMBER_FILE_ROW_INDEX, self.WORKERS_NUMBER_FILE_ROW_INDEX + 1):
                return int(line)
            
    def __get_time_horizon(self) -> int:
        with open(self.path, mode="r") as f:
            for line in islice(f, self.TIME_HORIZON_FILE_ROW_INDEX, self.TIME_HORIZON_FILE_ROW_INDEX + 1):
                return int(line)
    
    def get_jobs_weights(self) -> np.array:
        with open(self.path, mode="r") as f:
            for line in islice(f, 109, 110):
                weights = np.array(line.split("\t"))
                weights = weights[:len(weights)-1]
                return weights.astype(int)
            
    def get_due_dates(self) -> np.array:
        with open(self.path, mode="r") as f:
            for line in islice(f, 107, 108):
                dates = np.array(line.split("\t"))
                dates = dates[:len(dates)-1]
                return dates.astype(int)