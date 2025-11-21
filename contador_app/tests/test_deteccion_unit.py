import numpy as np
import cv2
from unittest.mock import MagicMock, patch
from django.test import TestCase

from contador_app import views as views_module

class FakeTensor:
    def __init__(self, arr):
        self._arr = np.array(arr, dtype=float)

    def cpu(self):
        return self

    def numpy(self):
        if self._arr.size == 1:
            return float(self._arr.flatten()[0])
        return self._arr

class MockBox:
    def __init__(self, xyxy, conf):
        self.xyxy = [FakeTensor(xyxy)]
        self.conf = [FakeTensor([conf])]

class MockResult:
    def __init__(self, boxes):
        self.boxes = boxes

class DetectUnitTest(TestCase):
    @patch('contador_app.views.load_model')
    def test_detect_people_with_mock_model(self, mock_load_model):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        box1 = MockBox([10, 10, 100, 200], 0.92)
        box2 = MockBox([150, 50, 220, 300], 0.85)
        mock_results = [MockResult([box1, box2])]

        mock_model = MagicMock(return_value=mock_results)
        mock_load_model.return_value = mock_model

        out_frame = views_module.detect_people(frame.copy())

        self.assertIsNotNone(out_frame)
        self.assertGreater(out_frame.sum(), 0)

        cv2.imwrite('test_detect_out.jpg', out_frame)
