from statistics import mean
from src.InstanceRetriever import InstanceRetriever
from src.MachineScheduler import MachineScheduler
import numpy as np
import gurobipy as gp
import pandas as pd
import os
import time

def main ():

    par = [(100,10,5)]
    modes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    
    models = ["milp+"]
    
    for t_model in models:
        for J,M,K in par:
            print((J,M,K))
            results = pd.DataFrame()
            for mode in modes:
                print(mode)
                retriever = InstanceRetriever(path_file=".\\data\\TEST0-RANDOM\\TEST0-" + str(J) + "-" + str(M) + "-" + str(K) + "-" + str(mode) + ".txt")
                instance = retriever.get_instance()
                
                try:
                    if t_model == "milp":
                        model = MachineScheduler(instance).build_milp_model()
                    elif t_model == "milp+":
                        model = MachineScheduler(instance).build_advanced_milp_model()
                        model.optimize()

                    constrs = model.NumConstrs
                    time = model.Runtime
                    if model.status == gp.GRB.OPTIMAL:
                        time_opt = model.Runtime
                        relax_value = model.getAttr('ObjVal')
                    else:
                        relax_value = None
                        time_opt = 3600
                    vars = model.NumVars
                    constrs = model.NumConstrs
                    A = model.getA()
                    size = A.count_nonzero()
                    
                    result = {"J": [J], "M": [M], "K": [K], "mode": [mode], "#opt": [model.status == gp.GRB.OPTIMAL], "T(s)": [time], "T_opt(s)": [time_opt], "LP": [relax_value], "#vars": [vars], "#constrs": [constrs], "#nzs": [size]}
                    results = pd.concat([results, pd.DataFrame(result, index=[0])])
                
                except (MemoryError, gp.GurobiError):
                    relax_value = None
                    time = 3600
                    time_opt = 3600
                    vars = 0
                    constrs = 0
                    size = 0
                    result = {"J": [J], "M": [M], "K": [K], "mode": [mode], "#opt": [False], "T(s)": [time], "T_opt(s)": [time_opt], "LP": [relax_value], "#vars": [vars], "#constrs": [constrs], "#nzs": [size]}
                    results = pd.concat([results, pd.DataFrame(result, index=[0])])
                    continue
            
            path = str(t_model) + "_" + str(J) + "_" + str(M) + "_" + str(K)
            results.to_csv(path + ".csv", mode='a', header=not os.path.exists(path + ".csv"))
    
if __name__ == '__main__':
	main()
