import cv2
import yaml
import time
from detector import PersonDetector
from occupancy import OccupancyGrid
from velocity import VelocityEstimator
from report import ReportGenerator

def run(source=0, save_report=False):
    with open('config.yaml') as f:
        cfg = yaml.safe_load(f)

    cap = cv2.VideoCapture(source)
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector  = PersonDetector(cfg['model'], cfg['confidence'])
    occ_grid  = OccupancyGrid(W, H, cfg['grid_rows'], cfg['grid_cols'])
    vel_est   = VelocityEstimator()
    reporter  = ReportGenerator() if save_report else None

    mode = 0  # 0=grid view, 1=heatmap view
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret: break

        detections = detector.detect(frame)
        occ_grid.update(detections)

        # Draw chosen view
        if mode == 0:
            vis = occ_grid.draw_grid(frame.copy())
        else:
            vis = occ_grid.draw_heatmap(frame.copy())

        # Draw bounding boxes + count
        for det in detections:
            x1,y1,x2,y2 = det['bbox']
            cv2.rectangle(vis,(x1,y1),(x2,y2),(57,211,83),2)

        # HUD
        fps = frame_count / max(time.time()-start_time, 1)
        danger_cells = (occ_grid.grid >= cfg['danger_threshold']).sum()
        cv2.rectangle(vis, (0,0), (320,70), (10,14,25), -1)
        cv2.putText(vis, f"HUMANAWARE v1.0", (10,20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,212,255), 1)
        cv2.putText(vis, f"People: {len(detections)}  FPS: {fps:.1f}",
                   (10,42), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255,255,255), 1)
        cv2.putText(vis, f"Danger Zones: {danger_cells}  [M]=toggle view",
                   (10,62), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,165,255), 1)

        if reporter: reporter.log_frame(frame_count, len(detections), danger_cells)

        cv2.imshow('HumanAware — Robot Occupancy System', vis)
        frame_count += 1

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if key == ord('m'): mode = 1 - mode  # toggle view

    cap.release()
    cv2.destroyAllWindows()
    if reporter: reporter.save('report.csv')

if __name__ == '__main__':
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else 0
    save = '--report' in sys.argv
    # int convert for webcam
    try: src = int(src)
    except: pass
    run(source=src, save_report=save)