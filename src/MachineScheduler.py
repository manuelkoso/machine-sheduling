from typing import Tuple

import gurobipy as gp
import numpy as np
import logging
from abc import ABC, abstractmethod

from .Instance import Instance


class MachineScheduler(ABC):
    TIME_LIMIT = 3600

    def __init__(self, instance: Instance) -> None:
        self._instance = instance
        self._model = gp.Model(str(self.__class__))
        self.model.setParam("TimeLimit", self.TIME_LIMIT)

    @property
    def instance(self) -> Instance:
        return self._instance

    @property
    def model(self) -> gp.Model:
        return self._model

    @abstractmethod
    def build_model(self) -> None:
        pass

    def run(self) -> None:
        logging.debug("Start model optimization")
        self.model.optimize()


class MILP(MachineScheduler):
    def build_model(self) -> None:
        logging.debug("MILP model building")
        T, C, x_ijkt = self.__get_variables()
        self.__set_constraints(T, C, x_ijkt)
        self.__set_objective(T)

    def __get_variables(self) -> Tuple:
        T = self.model.addVars([j for j in self.instance.J], vtype=gp.GRB.CONTINUOUS)
        C = self.model.addVars([j for j in self.instance.J], vtype=gp.GRB.CONTINUOUS)
        x_ijkt = self.model.addVars([(i, j, k, t) for j in self.instance.J
                                     for i in self.instance.get_Mj(j)
                                     for k in self.instance.get_Kij(i, j)
                                     for t in self.instance.T
                                     if t in np.arange(self.instance.rj[j],
                                                       self.instance.t_max - self.instance.pj[j] + 1)],
                                    vtype=gp.GRB.BINARY)
        return T, C, x_ijkt

    def __set_constraints(self, T, C, x_ijkt) -> None:
        self.model.addConstrs(gp.quicksum(x_ijkt[i, j, k, t]
                                          for i in self.instance.get_Mj(j)
                                          for k in self.instance.get_Kij(i, j)
                                          for t in self.instance.T if (i, j, k, t) in x_ijkt.keys()) == 1
                              for j in self.instance.J)

        self.model.addConstrs(gp.quicksum(x_ijkt[i, j, k, tau]
                                          for j in self.instance.J
                                          for k in self.instance.get_Kij(i, j)
                                          for tau in self.instance.get_Sjt(j, t)
                                          if (i, j, k, tau) in x_ijkt.keys()) <= 1
                              for i in self.instance.M
                              for t in self.instance.T)

        self.model.addConstrs(gp.quicksum(self.instance.qj[j] * x_ijkt[i, j, k, tau]
                                          for j in self.instance.J
                                          for i in self.instance.get_Mj(j) if k in self.instance.get_Kij(i, j)
                                          for tau in self.instance.get_Sjt(j, t)
                                          if (i, j, k, tau) in x_ijkt.keys()) <= self.instance.ukt[k, t]
                              for k in self.instance.K
                              for t in self.instance.T
                              if t != self.instance.t_max)

        self.model.addConstrs(C[j] == gp.quicksum(x_ijkt[i, j, k, t] * (t + self.instance.pj[j])
                                                  for i in self.instance.get_Mj(j)
                                                  for k in self.instance.get_Kij(i, j)
                                                  for t in self.instance.T
                                                  if (i, j, k, t) in x_ijkt.keys())
                              for j in self.instance.J)

        self.model.addConstrs(C[l] - self.instance.pj[l] >= C[j]
                              for j, l in self.instance.get_P_union_Q())

        self.model.addConstrs(gp.quicksum(x_ijkt[i, j, k, t]
                                          for k in self.instance.get_Kij(i, j)
                                          for t in self.instance.T
                                          if (i, j, k, t) in x_ijkt.keys()) ==
                              gp.quicksum(x_ijkt[i, l, k, t]
                                          for k in self.instance.get_Kij(i, l)
                                          for t in self.instance.T
                                          if (i, l, k, t) in x_ijkt.keys())
                              for j, l in self.instance.Q
                              for i in self.instance.get_Mj(j))

        self.model.addConstrs(gp.quicksum(x_ijkt[i, jp, k, t]
                                          for jp in self.instance.J if jp not in (j, l)
                                          for k in self.instance.get_Kij(i, jp)
                                          if (i, jp, k, t) in x_ijkt.keys()) <= 1 -
                              gp.quicksum(x_ijkt[i, j, k, tau]
                                          for k in self.instance.get_Kij(i, j)
                                          for tau in np.arange(self.instance.rj[j], t + 1)
                                          if (i, j, k, tau) in x_ijkt.keys()) +
                              gp.quicksum(x_ijkt[i, l, k, tau]
                                          for k in self.instance.get_Kij(i, l)
                                          for tau in np.arange(self.instance.rj[l], t + 1)
                                          if (i, l, k, tau) in x_ijkt.keys())
                              for j, l in self.instance.Q
                              for i in self.instance.get_Mj(j)
                              for t in self.instance.T)

        self.model.addConstrs(T[j] >= C[j] - self.instance.dj[j]
                              for j in self.instance.J)

    def __set_objective(self, T) -> None:
        self.model.setObjective(gp.quicksum(T[j] * self.instance.wj[j]
                                            for j in self.instance.J), gp.GRB.MINIMIZE)


class MilpAdvanced(MachineScheduler):
    def build_model(self) -> None:
        logging.debug("MILP Advanced model building")
        T, C, xm_ijt, xw_jkt = self.__get_variables()
        self.__set_constraints(T, C, xm_ijt, xw_jkt)
        self.__set_objective(T)

    def __get_variables(self) -> Tuple:
        T = self.model.addVars([j for j in self.instance.J], vtype=gp.GRB.CONTINUOUS)
        C = self.model.addVars([j for j in self.instance.J], vtype=gp.GRB.CONTINUOUS)
        xm_ijt = self.model.addVars([(i, j, t) for j in self.instance.J
                                     for i in self.instance.get_Mj(j)
                                     for t in self.instance.T
                                     if t in np.arange(self.instance.rj[j],
                                                       self.instance.t_max - self.instance.pj[j] + 1)],
                                    vtype=gp.GRB.BINARY)
        xw_jkt = self.model.addVars([(j, k, t) for j in self.instance.J
                                     for k in self.instance.get_Kj(j)
                                     for t in self.instance.T
                                     if t in np.arange(self.instance.rj[j],
                                                       self.instance.t_max - self.instance.pj[j] + 1)],
                                    vtype=gp.GRB.BINARY)

        return T, C, xm_ijt, xw_jkt

    def __set_constraints(self, T, C, xm_ijt, xw_jkt):
        self.model.addConstrs(gp.quicksum(xm_ijt[i, j, t]
                                          for i in self.instance.get_Mj(j)
                                          for t in self.instance.T
                                          if (i, j, t) in xm_ijt.keys()) == 1
                              for j in self.instance.J)

        self.model.addConstrs(gp.quicksum(xw_jkt[j, k, t]
                                          for k in self.instance.get_Kj(j)
                                          for t in self.instance.T
                                          if (j, k, t) in xw_jkt.keys()) == 1
                              for j in self.instance.J)

        self.model.addConstrs(gp.quicksum(xm_ijt[i, j, tau]
                                          for j in self.instance.J
                                          for tau in self.instance.get_Sjt(j, t)
                                          if (i, j, tau) in xm_ijt.keys()) <= 1
                              for i in self.instance.M
                              for t in self.instance.T)

        self.model.addConstrs(gp.quicksum(self.instance.qj[j] * xw_jkt[j, k, tau]
                                          for j in self.instance.J
                                          for tau in self.instance.get_Sjt(j, t)
                                          if (j, k, tau) in xw_jkt.keys()) <= self.instance.ukt[k, t]
                              for k in self.instance.K
                              for t in self.instance.T if t != self.instance.t_max)

        self.model.addConstrs(C[j] == gp.quicksum(xm_ijt[i, j, t] * (t + self.instance.pj[j])
                                                  for i in self.instance.get_Mj(j)
                                                  for t in self.instance.T
                                                  if (i, j, t) in xm_ijt.keys())
                              for j in self.instance.J)

        self.model.addConstrs(C[l] - self.instance.pj[l] >= C[j]
                              for j, l in self.instance.get_P_union_Q())

        self.model.addConstrs(gp.quicksum(xm_ijt[i, j, t]
                                          for t in self.instance.T
                                          if (i, j, t) in xm_ijt.keys()) ==
                              gp.quicksum(xm_ijt[i, l, t]
                                          for t in self.instance.T
                                          if (i, l, t) in xm_ijt.keys())
                              for i in self.instance.M
                              for j, l in self.instance.Q)

        self.model.addConstrs(gp.quicksum(xm_ijt[i, jp, t]
                                          for jp in self.instance.J if jp not in (j, l)
                                          if (i, jp, t) in xm_ijt.keys()) <= 1 -
                              gp.quicksum(xm_ijt[i, j, tau]
                                          for tau in np.arange(self.instance.rj[j], t + 1)
                                          if (i, j, tau) in xm_ijt.keys()) +
                              gp.quicksum(xm_ijt[i, l, tau]
                                          for tau in np.arange(self.instance.rj[l], t + 1)
                                          if (i, l, tau) in xm_ijt.keys())
                              for i in self.instance.M
                              for t in self.instance.T
                              for j, l in self.instance.Q)

        self.model.addConstrs(T[j] >= C[j] - self.instance.dj[j]
                              for j in self.instance.J)

        self.model.addConstrs(gp.quicksum(xm_ijt[i, j, t]
                                          for t in self.instance.T
                                          if (i, j, t) in xm_ijt.keys()) <=
                              gp.quicksum(xw_jkt[j, k, t]
                                          for t in self.instance.T
                                          for k in self.instance.get_Kij(i, j)
                                          if (j, k, t) in xw_jkt.keys())
                              for j in self.instance.J
                              for i in self.instance.get_Mj(j))

        self.model.addConstrs(gp.quicksum(xm_ijt[i, j, t]
                                          for i in self.instance.get_Mj(j)
                                          if (i, j, t) in xm_ijt.keys()) ==
                              gp.quicksum(xw_jkt[j, k, t]
                                          for k in self.instance.get_Kj(j)
                                          if (j, k, t) in xw_jkt.keys())
                              for j in self.instance.J
                              for t in self.instance.T)

    def __set_objective(self, T):
        self.model.setObjective(gp.quicksum(T[j] * self.instance.wj[j]
                                            for j in self.instance.J), gp.GRB.MINIMIZE)
