from flask import Flask, render_template, request, jsonify
from qreader import QReader
import cv2
import numpy as np
import base64
import logging

app = Flask(__name__)

# Initialize QR code reader
qreader = QReader()


deveui_size = 16
invalid_message = ""
message_end_time = 0

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Handle frame from webcam."""
    try:
        # Get the uploaded frame (base64 string)
        frame_data = request.json.get('frame')
        if not frame_data:
            return jsonify({'error': 'No frame data received'}), 400

        # Verify base64 prefix
        if not frame_data.startswith("data:image/png;base64,"):
            return jsonify({'error': 'Invalid frame data format'}), 400

        # Decode the base64 frame
        encoded_data = frame_data.split(',')[1]
        np_img = np.frombuffer(base64.b64decode(encoded_data), np.uint8)

        if np_img.size == 0:
            return jsonify({'error': 'Decoded buffer is empty'}), 400

        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({'error': 'Failed to decode the image'}), 400

        # Process the frame for QR codes
        height, width, _ = frame.shape
        roi = frame[height // 4:3 * height // 4, width // 4:3 * width // 4]
        rgb_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        decoded_text = qreader.detect_and_decode(image=rgb_frame)

        if decoded_text and decoded_text[0]:
            parts = decoded_text[0].split(",")
            for part in parts:
                if len(part) == deveui_size:
                    return jsonify({'code': part, 'warning': None, 'error': None})
            
            return jsonify({'code': None, 'warning': 'No valid DEVEUI code detected', 'error': None})

        return jsonify({'code': None, 'warning': 'No QR code detected', 'error': None})

    except Exception as e:
        return jsonify({'code': None, 'warning': None, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
