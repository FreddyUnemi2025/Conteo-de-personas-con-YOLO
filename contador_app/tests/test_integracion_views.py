import numpy as np
import cv2
from django.test import TestCase, Client
from unittest.mock import patch

from contador_app import views as views_module

def fake_frame_generator():
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    ret, buffer = cv2.imencode('.jpg', img)
    if not ret:
        return
    frame = buffer.tobytes()
    yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class IntegrationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'<img', resp.content.lower())

    def test_get_count_endpoint(self):
        resp = self.client.get('/get_count/')
        self.assertEqual(resp.status_code, 200)
        json_data = resp.json()
        self.assertIn('count', json_data)

    @patch('contador_app.views.generate_frames', side_effect=fake_frame_generator)
    def test_video_feed_with_mocked_frames(self, mock_gen):
        resp = self.client.get('/video_feed/', stream=True)
        self.assertEqual(resp.status_code, 200)
        content_type = resp.get('Content-Type', '')
        self.assertTrue('multipart' in content_type)

        iterator = resp.streaming_content
        first = next(iterator, None)
        self.assertIsNotNone(first)
        self.assertIn(b'Content-Type: image/jpeg', first)
