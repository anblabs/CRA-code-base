import os
import logging
import pandas as pd
from pathlib import Path
from ninflam.core.exceptions import DataRootError
from ninflam.data.loader_base import BaseLoader

log = logging.getLogger(__name__)

class ExcelLoader(BaseLoader):
    def __init__(self, file_name: str, sheet: int):
        self.file_name = file_name
        self.sheet = sheet

    def load(self) -> pd.DataFrame:
        # Search candidate directories in priority order:
        # 1. Code Ocean standard: ../data/<file>
        # 2. Code Ocean absolute: /data/<file>
        # 3. Local workspace Data dirs
        candidates = [
            Path("../data"),
            Path("/data"),
            Path(__file__).resolve().parents[3] / "Data",
            Path(__file__).resolve().parents[3] / "data",
            Path("Data"),
            Path("data"),
        ]

        path = None
        for cand in candidates:
            p = cand / self.file_name
            if p.exists():
                path = p
                break

        if path is None:
            ROOT = Path(__file__).resolve().parents[3]
            path = ROOT / "Data" / self.file_name

        log.info("Loading Excel: %s (sheet=%s)", path, self.sheet)
        return pd.read_excel(path, sheet_name=self.sheet)
