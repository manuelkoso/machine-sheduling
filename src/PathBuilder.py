from . import InstanceMeta
from .InstanceMeta import RealInstanceMeta, SyntheticInstanceMeta


class PathBuilder:
    INITIAL_SYNTHETIC_PATH_FILE_NAME = "data\\TEST0-RANDOM\\TEST0-"
    INITIAL_REAL_PATH_FILE_NAME = "data\\TEST1-REALISTIC\\TEST1-"

    @staticmethod
    def build_file_path(instance_meta: InstanceMeta):
        if isinstance(instance_meta, RealInstanceMeta):
            return PathBuilder.build_real_instance_file_path(instance_meta)
        elif isinstance(instance_meta, SyntheticInstanceMeta):
            return PathBuilder.build_synthetic_instance_file_path(instance_meta)
        raise ValueError("instance_meta must be either a RealInstanceMeta or a SyntheticInstanceMeta object")

    @staticmethod
    def build_synthetic_instance_file_path(instance_meta: SyntheticInstanceMeta):
        return PathBuilder.INITIAL_SYNTHETIC_PATH_FILE_NAME + str(instance_meta.J) + "-" + str(
            instance_meta.M) + "-" + str(
            instance_meta.K) + "-" + instance_meta.instance_version + ".txt"

    @staticmethod
    def build_real_instance_file_path(instance_meta: RealInstanceMeta):
        return PathBuilder.INITIAL_REAL_PATH_FILE_NAME + str(instance_meta.number_of_projects) + "-" + str(
            instance_meta.instance_version) + ".txt"
