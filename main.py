from statistics import mean
from src.InstanceRetriever import InstanceRetriever
from src.MachineScheduler import MachineScheduler
import numpy as np
import gurobipy as gp
import pandas as pd
import os
import time

def main ():

    modes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    J = 50
    M = 5
    K = 5
    type_model = "milp+"
    results = pd.DataFrame()
    
    for mode in modes:
        print(mode)
        retriever = InstanceRetriever(path_file=".\\data\\TEST0-RANDOM\\TEST0-" + str(J) + "-" + str(M) + "-" + str(K) + "-" + str(mode) + ".txt")
        instance = retriever.get_instance()
        if type_model == "milp":
            model = MachineScheduler(instance).build_milp_model()
        elif type_model == "milp+":
            model = MachineScheduler(instance).build_advanced_milp_model()
        model.optimize()
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
    
    path = type_model + "_" + str(J) + "_" + str(M) + "_" + str(K)
    results.to_csv(path + ".csv", mode='a', header=not os.path.exists(path + ".csv"))
    
if __name__ == '__main__':
	main()
