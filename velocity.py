import cv2
import numpy as np

class VelocityEstimator:
    def __init__(self):
        self.prev_positions = {}  # track_id: (cx, cy)

    def update(self, tracked_persons):
        velocities = {}
        for person in tracked_persons:
            tid = person['id']
            cx, cy = person['center']
            if tid in self.prev_positions:
                px, py = self.prev_positions[tid]
                dx, dy = cx - px, cy - py
                speed = np.sqrt(dx**2 + dy**2)
                velocities[tid] = {'dx': dx, 'dy': dy, 'speed': speed}
            self.prev_positions[tid] = (cx, cy)
        return velocities

    def draw_arrows(self, frame, tracked_persons, velocities):
        for person in tracked_persons:
            tid = person['id']
            if tid in velocities:
                cx, cy = person['center']
                v = velocities[tid]
                if v['speed'] > 3:  # only draw if actually moving
                    end = (cx + v['dx']*4, cy + v['dy']*4)
                    cv2.arrowedLine(frame, (cx,cy),
                                   (int(end[0]), int(end[1])),
                                   (255, 255, 0), 2, tipLength=0.4)
        return frame