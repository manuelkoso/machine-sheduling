from src.InstanceRetriever import InstanceRetriever
import gurobipy as gp


def main ():
    retriever = InstanceRetriever(path_file=".\\data\\TEST0-RANDOM\\TEST0-50-2-2-A.txt")
    weights = retriever.get_jobs_weights()
    model = gp.Model("scheduler")
    model.modelSense = gp.GRB.MINIMIZE
    t = model.addVars([i for i in range(50)], vtype=gp.GRB.INTEGER)
    model.setObjective(gp.quicksum(t[j]*weights[j] for j in range(50)))
    model.optimize()
    
if __name__ == '__main__':
	main()
