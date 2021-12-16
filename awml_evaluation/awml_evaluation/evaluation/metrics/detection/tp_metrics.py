from abc import ABCMeta
from abc import abstractmethod
from math import pi

from awml_evaluation.evaluation.result.object_result import DynamicObjectWithResult


class TPMetrics(metaclass=ABCMeta):
    @abstractmethod
    def get_value(
        self,
        object_result: DynamicObjectWithResult,
    ) -> float:
        pass


class TPMetricsAp(TPMetrics):
    def get_value(
        self,
        object_result: DynamicObjectWithResult,
    ) -> float:
        """[summary]
        Get TP (True positive) value.
        If TP metrics is AP, return 1.0.

        Args:
            object_result (DynamicObjectWithResult): The object result

        Returns:
            float: TP (True positive) value, 1.0.
        """
        return 1.0


class TPMetricsAph(TPMetrics):
    def get_value(
        self,
        object_result: DynamicObjectWithResult,
    ) -> float:
        """[summary]
        Get TP (True positive) value, the heading similarity rate using for APH.
        APH is used in evaluation for waymo dataset.

        Args:
            object_result (DynamicObjectWithResult): The object result

        Returns:
            float: The heading similarity rate using for APH.
                   Calculate heading accuracy (1.0 - diff_heading / pi), instead of 1.0 for AP.
                   The minimum rate is 0 and maximum rate is 1.
                   0 means the heading difference is pi, and 1 means no heading difference.

        Refference:
                https://github.com/waymo-research/waymo-open-dataset/blob/master/waymo_open_dataset/metrics/metrics_utils.cc#L101-L116
        """

        pd_heading = object_result.predicted_object.get_heading_bev()
        gt_heading = object_result.ground_truth_object.get_heading_bev()
        diff_heading = abs(pd_heading - gt_heading)

        # Normalize heading error to [0, pi] (+pi and -pi are the same).
        if diff_heading > pi:
            diff_heading = 2.0 * pi - diff_heading
        # Clamp the range to avoid numerical errors.
        return min(1.0, max(0.0, 1.0 - diff_heading / pi))