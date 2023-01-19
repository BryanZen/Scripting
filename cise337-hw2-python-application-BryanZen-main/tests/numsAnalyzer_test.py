import pytest
import sys, os

sys.path.insert(1, os.getcwd())
from src.numsAnalyzer import np, countMissingValues, curve_low_scoring_exams, exams_with_median_gt_K, \
    replaceMissingValues


class TestNumsAnalyzer:

    def setup_method(self):
        self.numpy_arr = np.array([
            [100.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        self.numpy_curve = np.array([
            [100.0, 7.4, 50.9, 7.4, 87.4],
            [98.5, 1.5, 100.0, 1.5, 66.8],
            [82.7, 71.4, 100.0, 0.1, 48.1],
            [100.0, 87.3, 94.5, 99.0, 78.4]])

    def test_replace_missing_values(self):
        out = np.array([np.NaN])
        val = np.array([0])
        assert replaceMissingValues(out) == val

    def test_count_missing_values_invalid_k1(self):
        with pytest.raises(TypeError):
            countMissingValues(self.numpy_arr, 'k')

    def test_count_missing_values_invalid_k2(self):
        with pytest.raises(ValueError):
            countMissingValues(self.numpy_arr, 5)

    def test_count_missing_values_invalid_k3(self):
        with pytest.raises(ValueError):
            countMissingValues(self.numpy_arr, -5)

    def test_count_missing_values_valid(self):
        val = np.array([0, 1, 2, 2])
        assert np.array_equal(countMissingValues(self.numpy_arr, 1), val)

    def test_count_missing_values_valid_negative(self):
        val = np.array([0, 1, 2, 2])
        assert np.array_equal(countMissingValues(self.numpy_arr, -1), val)

    def test_exams_with_median_gt_K_invalid_k1(self):
        with pytest.raises(ValueError):
            exams_with_median_gt_K(self.numpy_arr, -1)

    def test_exams_with_median_gt_K_invalid_k2(self):
        with pytest.raises(ValueError):
            exams_with_median_gt_K(self.numpy_arr, 110)

    def test_exams_with_median_gt_K_invalid_k3(self):
        with pytest.raises(TypeError):
            exams_with_median_gt_K(self.numpy_arr, '1')

    def test_exams_with_median_gt_K_invalid_x1(self):
        out = np.array([
            [101.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        with pytest.raises(ValueError):
            exams_with_median_gt_K(out, 1)

    def test_exams_with_median_gt_K_invalid_x2(self):
        out = np.array([
            [-100.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        with pytest.raises(ValueError):
            exams_with_median_gt_K(out, 1)

    def test_exams_with_median_gt_K_valid(self):
        assert exams_with_median_gt_K(self.numpy_arr, 70) == 2

    def test_curve_low_scoring_exams_invalid_k1(self):
        with pytest.raises(ValueError):
            curve_low_scoring_exams(self.numpy_arr, -1)

    def test_curve_low_scoring_exams_invalid_k2(self):
        with pytest.raises(ValueError):
            curve_low_scoring_exams(self.numpy_arr, 101)

    def test_curve_low_scoring_exams_invalid_k3(self):
        with pytest.raises(TypeError):
            curve_low_scoring_exams(self.numpy_arr, '-1')

    def test_curve_low_scoring_exams_invalid_x1(self):
        out = np.array([
            [101.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        with pytest.raises(ValueError):
            curve_low_scoring_exams(out, 1)

    def test_curve_low_scoring_exams_invalid_x2(self):
        out = np.array([
            [-100.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        with pytest.raises(ValueError):
            curve_low_scoring_exams(out, 1)

    def test_curve_low_scoring_exams_invalid_x3(self):
        out = np.array([
            [100.0, 87.3, 94.5, 99.0, 78.4],
            [82.6, 71.3, 99.9, np.NaN, 48.0],
            [-92.6, np.NaN, 43.5, np.NaN, 80.0],
            [97.0, np.NaN, 98.5, np.NaN, 65.3]])
        with pytest.raises(ValueError):
            curve_low_scoring_exams(out, 70)

    def test_curve_low_scoring_exams_valid(self):
        assert np.array_equal(curve_low_scoring_exams(
            self.numpy_arr, 95), self.numpy_curve)
