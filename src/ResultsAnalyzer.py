class ResultsAnalyzer:

    @staticmethod
    def get_vars_mean():
        pass

    @staticmethod
    def get_constrs_mean():
        pass

    @staticmethod
    def get_nzs_mean():
        pass

    @staticmethod
    def get_LP_mean():
        pass

    @staticmethod
    def get_opt_count(p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                      J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    @staticmethod
    def get_run_time_mean(p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                          J_K_ratio: int = None, M_K_ratio: int = None):
        pass

    @staticmethod
    def get_opt_run_time_mean(p_q: bool = None, r: float = None, J: int = None, J_M_ratio: int = None,
                              J_K_ratio: int = None, M_K_ratio: int = None):
        pass
