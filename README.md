# YOLO-TFJS-Pyzbar-FastAPI

# YOLO Fine-Tuning & Web Deployment with TensorFlow.js & FastAPI

## 📌 Project Overview

This project fine-tunes a YOLO model for object detection, converts it to TensorFlow.js for web usage, and integrates FastAPI for barcode decoding with **pyzbar** via WebSockets.

## 🚀 Features

- **YOLOv8 Fine-Tuning** on a custom dataset
- **Model Conversion**: YOLO → TensorFlow.js
- **Optimized Model Loading** in the browser
- **Web Interface**: Real-time inference with TensorFlow.js
- **FastAPI Backend**: Receives image captures via WebSockets and decodes barcodes with **pyzbar**

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Maelabad/YOLO-TFJS-Pyzbar-FastAPI.git && cd YOLO-TFJS-Pyzbar-FastAPI
```

### 2️⃣ Install dependencies

#### Backend (FastAPI + pyzbar)

```bash
pip install -r requirements.txt
```

#### Frontend (TensorFlow.js)

Ensure you have a working web server (e.g., **XAMPP**).

### 3️⃣ Download YOLO Weights (Optional)

```bash
wget https://path/to/your/yolo/weights.pt -O model.pt
```

## 📦 Fine-Tuning the YOLO Model

```python
from ultralytics import YOLO

# Load and fine-tune the model
model = YOLO("yolov8s.pt")  # Pretrained model
model.train(data="config.yaml", epochs=50, save_period=3, save=True)  # Save every 3 epochs
```

## 🔄 Converting YOLO to TensorFlow.js

1️⃣ Convert **YOLO to TensorFlow SavedModel**:

```bash
onnx2tf -i best.onnx -o saved_model
```

2️⃣ Convert **SavedModel to TensorFlow.js** with quantization:

```bash
tensorflowjs_converter \
    --input_format=tf_saved_model \
    --output_format=tfjs_graph_model \
    --quantization_bytes=1 \
    saved_model \
    web_model
```

## ⚡ Model Optimization & Best Practices

1. **Use Intermediate Checkpoints (`epoch_x.pt`)** to keep training state.
2. **Enable Quantization (`--quantization_bytes=1`)** to reduce model size.
3. **Cache Model in IndexedDB** for fast web loading.
4. **Use WebSockets** to send images from the web to FastAPI for barcode decoding.

## 🚀 Running the Web App

#### 1️⃣ Start FastAPI Backend

```bash
uvicorn app.main:app --reload
```

#### 2️⃣ Serve the Frontend

Use a static web server like **XAMPP** or **Live Server** in VS Code.

## 📡 WebSocket Communication for Barcode Decoding

The frontend captures images and sends them via WebSockets:

```js
const socket = new WebSocket("ws://localhost:8000/ws");
socket.send(imageData);
```

FastAPI backend processes and decodes with **pyzbar**:

```python
from pyzbar.pyzbar import decode
from PIL import Image

def decode_barcode(image_path):
    image = Image.open(image_path)
    barcodes = decode(image)
    return [barcode.data.decode("utf-8") for barcode in barcodes]
```

## 📜 Model Configuration in Frontend

Include TensorFlow.js CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/tensorflow/4.15.0/tf.min.js"></script>
```

Define model configuration:
```js
const modelConfig = {
    modelUrl: 'http://localhost/test_barcode/web_model/model.json', // Path to the trained model
    inputSize: 640,
    scoreThreshold: 0.7,
    iouThreshold: 0.5
};
```

Load the model asynchronously:
```js
async function loadModel() {
    loadingDiv.style.display = 'block'; // Show loading indicator
    try {
        model = await tf.loadGraphModel(modelConfig.modelUrl); // Load the model from the defined URL
        isModelLoaded = true;
        loadingDiv.style.display = 'none'; // Hide loading indicator
        console.log('Model successfully loaded');
    } catch (error) {
        console.error('Error loading the model:', error);
        loadingDiv.textContent = 'Error loading the model';
    }
}
```



