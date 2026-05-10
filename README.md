# 🎨 AI Finger Painter

An interactive AI-powered drawing application that allows you to paint in the air using your fingers and a webcam.

## 🚀 Features
- **Real-time Finger Tracking**: Uses MediaPipe for high-performance hand landmark detection.
- **Dynamic Palette**: Select colors (Red, Green, Blue, Yellow, Purple, White) or use the Eraser.
- **Gesture Controls**: 
  - ☝️ **Index Finger Up**: Draw on the canvas.
  - ✌️ **Index + Middle Fingers Up**: Hover over the top palette to select colors.
  - ✊ **Fist**: Pause drawing.
- **Brush Controls**: Use `+` and `-` keys to adjust brush size.
- **Canvas Management**: Press `C` to clear the screen and `Q` to quit.

## 🛠️ Setup & Installation

Due to specific version requirements for MediaPipe and TensorFlow, it is recommended to run this in a virtual environment.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ADARSH685-BOT/-finger-tracking-AI-painter.git
   cd -finger-tracking-AI-painter
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install mediapipe==0.10.11 opencv-python numpy
   ```

4. **Run the application**:
   ```bash
   python finger_painter.py
   ```

## 📜 Requirements
- Python 3.10+
- Webcam
- Dependencies: `mediapipe`, `opencv-python`, `numpy`

---
Built with ❤️ by Adarsh Kumar
