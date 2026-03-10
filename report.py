import csv, datetime

class ReportGenerator:
    def __init__(self):
        self.logs = []

    def log_frame(self, frame_num, people_count, danger_zones):
        self.logs.append({
            'frame': frame_num,
            'people': people_count,
            'danger_zones': danger_zones,
            'timestamp': datetime.datetime.now().isoformat()
        })

    def save(self, path='report.csv'):
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.logs[0].keys())
            writer.writeheader()
            writer.writerows(self.logs)
        print(f"[HumanAware] Report saved → {path}")