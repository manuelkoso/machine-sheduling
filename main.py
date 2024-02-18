from src.InstanceRetriever import InstanceRetriever
import gurobipy as gp


def main ():
    retriever = InstanceRetriever(path_file=".\\data\\TEST0-RANDOM\\TEST0-50-5-3-E.txt")
    instance = retriever.get_instance()
    print(instance.get_Sjt(20,101))
    print(instance.get_Kij(4,6))
    # weights = retriever.__get_jobs_weights()
    # model = gp.Model("scheduler")
    # model.modelSense = gp.GRB.MINIMIZE
    # T = model.addVars([i for i in range(50)], vtype=gp.GRB.INTEGER)
    # model.setObjective(gp.quicksum(T[j]*weights[j] for j in range(50)))
    # model.optimize()
    
if __name__ == '__main__':
	main()
