import pandas as pd
from statistics import mean
import os

milp_results = pd.read_csv("milp_50_5_3.csv")
# milp_plus_results = pd.read_csv("milp+_50_5_5.csv")

mode_opt_milp = milp_results.loc[milp_results["#opt"] == True]["mode"]
# mode_opt_milp_plus = milp_plus_results.loc[milp_plus_results["#opt"] == True]["mode"]

# opt_modes = pd.merge(mode_opt_milp, mode_opt_milp_plus)
opt_modes = {}
opt_modes["mode"] = mode_opt_milp
print("************* milp *************")
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["#vars"]))
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["#constrs"]))
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["#nzs"]))
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["LP"]))
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["T(s)"]))
print(mean(milp_results.loc[milp_results["mode"].isin(opt_modes["mode"])]["T_opt(s)"]))

print("************* milp plus *************")
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["#vars"]))
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["#constrs"]))
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["#nzs"]))
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["LP"]))
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["T(s)"]))
# print(mean(milp_plus_results.loc[milp_plus_results["mode"].isin(opt_modes["mode"])]["T_opt(s)"]))