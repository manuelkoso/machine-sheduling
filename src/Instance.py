import numpy as np


class Instance:
    JOB_WEIGHTS = [1, 2, 3, 4]
    MAX_NUMBER_OF_WORKING_HOURS = 8
    RESOURCE_CONSUMPTION_VALUES = [1, 8]
    BINARY_VALUES = [0, 1]

    def __init__(self, njobs: int, nmachines: int, nworkers: int, time_horizon: int) -> None:
        self.J = range(njobs)
        self.M = range(nmachines)
        self.K = range(nworkers)
        self.T = range(time_horizon + 1)
        self.t_max = time_horizon

    @property
    def Mj(self) -> np.ndarray:
        return self._Mj

    @Mj.setter
    def Mj(self, value: np.ndarray) -> None:
        if value.shape[0] != len(self.J):
            raise ValueError("The number of rows must be equal to the number of jobs")
        if value.shape[1] != len(self.M):
            raise ValueError("The number of columns must be equal to the number of machines")
        if not np.all(np.isin(value, self.BINARY_VALUES)):
            raise ValueError("The Mj must contain only binary values 0 and 1")
        self._Mj = value

    @property
    def Kj(self) -> np.ndarray:
        return self._Kj

    @Kj.setter
    def Kj(self, value: np.ndarray) -> None:
        if value.shape[0] != len(self.J):
            raise ValueError("The number of rows must be equal to the number of jobs")
        if value.shape[1] != len(self.K):
            raise ValueError("The number of columns must be equal to the number of workers")
        if not np.all(np.isin(value, self.BINARY_VALUES)):
            raise ValueError("The Kj must contain only binary values 0 and 1")
        self._Kj = value

    @property
    def Ki(self) -> np.ndarray:
        return self._Ki

    @Ki.setter
    def Ki(self, value: np.ndarray) -> None:
        if value.shape[0] != len(self.M):
            raise ValueError("The number of rows must be equal to the number of machines")
        if value.shape[1] != len(self.K):
            raise ValueError("The number of columns must be equal to the number of workers")
        if not np.all(np.isin(value, self.BINARY_VALUES)):
            raise ValueError("The Ki must contain only binary values 0 and 1")
        self._Ki = value

    @property
    def rj(self) -> np.ndarray:
        return self._rj

    @rj.setter
    def rj(self, value: np.ndarray) -> None:
        if len(value) != len(self.J):
            raise ValueError("The number of elements must be equal to the number of jobs")
        if not np.all(np.isin(value, self.T)):
            raise ValueError("The value of elements must be an integer in the interval [0," + str(self.t_max) + "]")
        self._rj = value

    @property
    def dj(self) -> np.ndarray:
        return self._dj

    @dj.setter
    def dj(self, value: np.ndarray) -> None:
        if len(value) != len(self.J):
            raise ValueError("The number of elements must be equal to the number of jobs")
        if not np.all(np.isin(value, self.T)):
            raise ValueError("The value of elements must be an integer in the interval [0," + str(self.t_max) + "]")
        self._dj = value

    @property
    def qj(self) -> np.ndarray:
        return self._qj

    @qj.setter
    def qj(self, value) -> None:
        if len(value) != len(self.J):
            raise ValueError("The number of elements must be equal to the number of jobs")
        if not np.all(np.isin(value, self.RESOURCE_CONSUMPTION_VALUES)):
            raise ValueError("The value of elements must be either 1 or 8")
        self._qj = value

    @property
    def wj(self) -> np.ndarray:
        return self._wj

    @wj.setter
    def wj(self, value: np.ndarray) -> None:
        if len(value) != len(self.J):
            raise ValueError("The number of elements must be equal to the number of jobs")
        if not np.all(np.isin(value, self.JOB_WEIGHTS)):
            raise ValueError("The value of elements be an integer in the interval " + self.JOB_WEIGHTS)
        self._wj = value

    @property
    def pj(self) -> np.ndarray:
        return self._pj

    @pj.setter
    def pj(self, value: np.ndarray) -> None:
        if len(value) != len(self.J):
            raise ValueError("The number of elements must be equal to the number of jobs")
        if not np.all(np.isin(value, self.T)):
            raise ValueError("The value of elements must be an integer in the interval [0," + str(self.t_max) + "]")
        self._pj = value

    @property
    def ukt(self) -> np.ndarray:
        return self._ukt

    @ukt.setter
    def ukt(self, value: np.ndarray) -> None:
        if value.shape[0] != len(self.K):
            raise ValueError("The number of rows must be equal to the number of workers")
        if value.shape[1] != len(self.T) - 1:
            raise ValueError("The number of columns must be equal to the time horizon")
        if not np.all((value >= 0) & (value <= self.MAX_NUMBER_OF_WORKING_HOURS)):
            raise ValueError("The value of elements must be an integer in the interval [0," + str(
                self.MAX_NUMBER_OF_WORKING_HOURS) + "]")
        self._ukt = value

    @property
    def P(self) -> np.ndarray:
        return self._P

    @P.setter
    def P(self, value: np.ndarray) -> None:
        if len(value) != 0 and value.shape[1] != 2:
            raise ValueError("The number of columns must be 2")
        if len(value) != 0 and not np.all(np.isin(value, self.J)):
            raise ValueError("The values must be a job, an integer in the interval [0," + str(len(self.J) - 1) + "]")
        self._P = value

    @property
    def Q(self) -> np.ndarray:
        return self._Q

    @Q.setter
    def Q(self, value: np.ndarray) -> None:
        if len(value) != 0 and value.shape[1] != 2:
            raise ValueError("The number of columns must be 2")
        if len(value) != 0 and not np.all(np.isin(value, self.J)):
            raise ValueError("The values must be a job, an integer in the interval [0," + str(len(self.J) - 1) + "]")
        self._Q = value

    def get_P_union_Q(self) -> np.ndarray:
        if len(self._Q) == 0:
            return self._P
        elif len(self._P) == 0:
            return self._Q
        else:
            return np.concatenate((self._Q, self._P))

    def get_Kij(self, i: int, j: int) -> np.array:
        if i not in self.M:
            raise ValueError(
                "The parameter i must be a machine, integer in the interval [0," + str(len(self.M) - 1) + "]")
        if j not in self.J:
            raise ValueError(
                "The parameter j must be a job, an integer in the inetrval [0," + str(len(self.J) - 1) + "]")
        return np.where(self._Ki[i] + self._Kj[j] > 1)[0]

    def get_Kj(self, j: int) -> np.array:
        if j not in self.J:
            raise ValueError(
                "The parameter j must be a job, an integer in the inetrval [0," + str(len(self.J) - 1) + "]")
        return np.where(self._Kj[j] == 1)[0]

    def get_Mj(self, j: int) -> np.array:
        if j not in self.J:
            raise ValueError(
                "The parameter j must be a job, an integer in the inetrval [0," + str(len(self.J) - 1) + "]")
        return np.where(self._Mj[j] == 1)[0]

    def get_Sjt(self, j: int, t: int) -> np.array:
        if t not in self.T:
            raise ValueError("The parameter t must be an integer in the interval [0," + str(self.t_max) + "]")
        if j not in self.J:
            raise ValueError(
                "The parameter j must be a job, an integer in the inetrval [0," + str(len(self.J) - 1) + "]")
        if (self._rj[j] > t):
            return np.array([])
        if t >= self._rj[j] and self._rj[j] >= t - self._pj[j] + 1:
            return np.arange(self._rj[j], t + 1)
        return np.arange(t - self._pj[j] + 1, t + 1)

    def __str__(self) -> str:
        return "[" + str(len(self.J)) + ", " + str(len(self.M)) + ", " + str(len(self.K)) + ", " + str(self.t_max) + "]"
