from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
import json
import time

@dataclass
class LoopState:
    session_dir: Path
    step: int = 0
    loop_idx: int = 0

class RDLoop:
    def __init__(self, settings: Any, logger, runner) -> None:
        self.settings = settings
        self.logger = logger
        self.runner = runner

    @staticmethod
    def _ensure_session(path: Optional[str], base_dir: str) -> LoopState:
        if path:
            sd = Path(path)
            sd.mkdir(parents=True, exist_ok=True)
        else:
            sd = Path(base_dir) / "__session__" / str(int(time.time()))
            sd.mkdir(parents=True, exist_ok=True)
        return LoopState(session_dir=sd)

    def run(self, step_n: Optional[int] = None, loop_n: Optional[int] = None, all_duration: Optional[str] = None) -> None:
        st = self._ensure_session(getattr(self, "path", None), self.settings.log_dir)
        self.logger.info(f"Session: {st.session_dir}")
        t_end = None
        if all_duration and all_duration.endswith("h"):
            t_end = time.time() + float(all_duration[:-1]) * 3600

        loops = loop_n if loop_n is not None else 1
        for li in range(loops):
            st.loop_idx = li
            self.logger.info(f"Loop {li+1}/{loops}")
            try:
                self._one_loop(st)
            except Exception as e:
                self.logger.exception(f"Loop {li} failed: {e}")
            if t_end and time.time() > t_end:
                self.logger.info("Time budget reached, stopping.")
                break

    def _one_loop(self, st: LoopState) -> None:
        hyp = self.runner.propose(st)
        code_ws = self.runner.implement(st, hyp)
        result = self.runner.evaluate(st, code_ws)
        self._persist(st, hyp=hyp, result=result)

    def _persist(self, st: LoopState, **kwargs) -> None:
        out = st.session_dir / f"loop_{st.loop_idx}_result.json"
        with out.open("w", encoding="utf-8") as f:
            json.dump(kwargs, f, ensure_ascii=False, indent=2)