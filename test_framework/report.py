from __future__ import annotations
from typing import Dict, Any, List, Optional
import csv, json, time, pathlib, os

class Report:
    """In-memory log of test steps.
    - log_result(): append a step
    - export_artifacts(): write JSON + CSV
    - attach_live_log(): stream a line of JSON per step to live.log
    """

    def __init__(self, uut_id: Optional[str] = None, session_id: Optional[str] = None):
        self.records: List[Dict[str, Any]] = []
        self.uut_id = uut_id
        self.session_id = session_id or time.strftime("%Y%m%d-%H%M%S")
        self._live_log_path: Optional[str] = None

    def set_meta(self, *, uut_id: Optional[str] = None, session_id: Optional[str] = None):
        if uut_id is not None:
            self.uut_id = uut_id
        if session_id is not None:
            self.session_id = session_id

    # --- live log streaming ---
    def attach_live_log(self, path: str, header: bool = True):
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._live_log_path = path
        if header:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"# live log session={self.session_id} uut={self.uut_id}\n")

    def _append_live_line(self, rec: Dict[str, Any]):
        if not self._live_log_path:
            return
        with open(self._live_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    # --- step logging ---
    def log_result(
        self,
        name: str,
        status: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        rec = {
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "session_id": self.session_id,
            "uut_id": self.uut_id,
            "name": name,
            "status": status,
            "output": output,
            "error": error,
        }
        if meta:
            rec.update({f"meta_{k}": v for k, v in meta.items()})
        self.records.append(rec)
        self._append_live_line(rec)

    # --- exports ---
    def _ensure_dir(self, path: str):
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)

    def to_csv(self, path: str):
        if not self.records:
            return
        self._ensure_dir(path)
        fields = list(self.records[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in self.records:
                w.writerow(r)

    def to_json(self, path: str, indent: int = 2):
        self._ensure_dir(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=indent)

    def export_artifacts(self, directory: str, basename: str = "report"):
        os.makedirs(directory, exist_ok=True)
        self.to_json(os.path.join(directory, f"{basename}.json"))
        self.to_csv(os.path.join(directory, f"{basename}.csv"))