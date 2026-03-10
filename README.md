# 🤖 HumanAware — Dynamic Occupancy Mapping for Robot Navigation

Real-time human detection and occupancy grid generation for 
safe robot path planning in dynamic environments.

> Built as part of AI/Robotics portfolio — directly applicable 
> to humanoid robot navigation and collision avoidance systems.

## 🎯 Motivation
Humanoid robots operating in shared human spaces need to know:
- **Where** are people located right now?
- **Which zones** are safe to navigate through?
- **How** are people moving?

HumanAware answers all three in real-time.

## ✨ Features
- 🔍 YOLOv8 real-time person detection
- 🗺️ Dynamic occupancy grid (SAFE / CAUTION / DANGER zones)
- 🔥 Temporal heatmap showing crowd density over time  
- ➡️ Movement direction estimation per person
- 📹 Works with webcam AND video files
- 📊 CSV session report generation

## 🛠️ Tech Stack
- Python 3.11
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy

## 🚀 Run

### Install
pip install ultralytics opencv-python pyyaml

### Webcam (live)
python main.py

### Video file
python main.py path/to/video.mp4

### Video + generate report
python main.py path/to/video.mp4 --report

## ⌨️ Controls
| Key | Action |
|-----|--------|
| M   | Toggle Grid view ↔ Heatmap view |
| Q   | Quit |

## 📁 Project Structure
HumanAware/
├── main.py         # Entry point
├── detector.py     # YOLOv8 detection wrapper  
├── occupancy.py    # Grid builder + risk classifier
├── velocity.py     # Movement direction estimator
├── report.py       # CSV report generator
└── config.yaml     # Tunable parameters

## 🔧 Configuration (config.yaml)
| Parameter | Default | Description |
|-----------|---------|-------------|
| confidence | 0.5 | Detection threshold |
| grid_rows | 8 | Occupancy grid rows |
| grid_cols | 8 | Occupancy grid cols |
| danger_threshold | 2 | People per cell = DANGER |

## 🤖 Robotics Application
This system generates the **occupancy layer** needed by robot 
path planners (like RRT* or A*) to avoid human-occupied zones 
dynamically — a core requirement for safe humanoid navigation.

---
Built by [TechAnjum](https://github.com/TechAnjum)