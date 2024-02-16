import numpy as np

class Instance:
    
    def __init__(self, njobs: int, nmachines: int, nworkers: int, time_horizon: int) -> None:
        self._njobs = njobs
        self._nmachines = nmachines
        self._nworkers = nworkers
        self._time_horizon = time_horizon
    
    @property
    def njobs(self) -> int:
        return self.njobs
    
    @property
    def nmachines(self) -> int:
        return self.nmachines
    
    @property
    def nworkers(self) -> int:
        return self.nworkers
    
    @property
    def time_horizon(self) -> int:
        return self.time_horizon
    
    @property
    def machines_used_per_job(self) -> np.ndarray:
        return self._machines_used_per_job
    
    @machines_used_per_job.setter
    def machines_used_per_job(self, value: np.ndarray) -> None:
        self._machines_used_per_job = value
    
    @property
    def workers_used_per_job(self) -> np.ndarray:
        return self._workers_used_per_job
    
    @workers_used_per_job.setter
    def workers_used_per_job(self, value: np.ndarray) -> None:
        self._workers_used_per_job = value
    
    @property
    def workers_used_per_machine(self) -> np.ndarray:
        return self._workers_used_per_machine
    
    @workers_used_per_machine.setter
    def workers_used_per_machine(self, value: np.ndarray) -> None:
        self._workers_used_per_machine = value
    
    @property
    def due_dates(self) -> np.ndarray:
        return self._due_dates
    
    @due_dates.setter
    def due_dates(self, value: np.ndarray) -> None:
        self._due_dates = value
    
    @property
    def due_dates_processed(self) -> np.ndarray:
        return self._due_dates_processed
    
    @due_dates_processed.setter
    def due_dates_processed(self, value: np.ndarray) -> None:
        self._due_dates_processed = value
    
    @property
    def daily_resource_consumption(self) -> np.ndarray:
        return self._daily_resource_consumption 
    
    @daily_resource_consumption.setter
    def daily_resource_consumption(self, value) -> None:
        self._daily_resource_consumption = value
    
    @property
    def jobs_weight(self) -> np.ndarray:
        return self._jobs_weight
    
    @jobs_weight.setter
    def jobs_weight(self, value: np.ndarray) -> None:
        self._jobs_weight = value
    
    @property
    def processing_time(self) -> np.ndarray:
        return self._processing_time  
    
    @processing_time.setter
    def processing_time(self, value: np.ndarray) -> None:
        self._processing_time = value
        
    @property
    def workers_working_hours(self) -> np.ndarray:
        return self._workers_working_hours
    
    @workers_working_hours.setter
    def workers_working_hours(self, value: np.ndarray) -> None:
        self._workers_working_hours = value
    
    def __str__(self) -> str:
        return "[" + str(self._njobs) + ", " + str(self._nmachines) + ", " + str(self._nworkers) + ", " + str(self._time_horizon) +  "]"