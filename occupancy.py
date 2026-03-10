import numpy as np
import cv2

class OccupancyGrid:
    def __init__(self, frame_w, frame_h, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.cell_w = frame_w // cols
        self.cell_h = frame_h // rows
        self.grid = np.zeros((rows, cols), dtype=int)
        self.heatmap = np.zeros((frame_h, frame_w), dtype=np.float32)

    def update(self, detections):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for det in detections:
            cx, cy = det['center']
            col = min(cx // self.cell_w, self.cols - 1)
            row = min(cy // self.cell_h, self.rows - 1)
            self.grid[row][col] += 1
            # update heatmap
            self.heatmap[cy-25:cy+25, cx-25:cx+25] += 0.5
        self.heatmap *= 0.93  # temporal decay

    def get_risk(self, row, col, danger_t=2, caution_t=1):
        count = self.grid[row][col]
        if count >= danger_t:   return 'DANGER', (0, 0, 255)
        elif count >= caution_t: return 'CAUTION', (0, 165, 255)
        else:                    return 'SAFE', (0, 255, 0)

    def draw_grid(self, frame):
        overlay = frame.copy()
        for r in range(self.rows):
            for c in range(self.cols):
                risk, color = self.get_risk(r, c)
                x1 = c * self.cell_w
                y1 = r * self.cell_h
                x2 = x1 + self.cell_w
                y2 = y1 + self.cell_h
                alpha = 0.35 if risk != 'SAFE' else 0.1
                cv2.rectangle(overlay, (x1,y1), (x2,y2), color, -1)
                if risk != 'SAFE':
                    cv2.putText(overlay, risk, (x1+4, y1+18),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                               (255,255,255), 1)
        return cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    def draw_heatmap(self, frame):
        h = np.clip(self.heatmap, 0, 255).astype(np.uint8)
        heat_color = cv2.applyColorMap(h, cv2.COLORMAP_JET)
        return cv2.addWeighted(frame, 0.6, heat_color, 0.4, 0)