import re
from pathlib import Path
from dataclasses import dataclass
from typing import Any
from finance_data_agent.logging.logger import get_logger
from finance_data_agent.llm.api_backend import APIBackend
from finance_data_agent.utils.tpl import load_text
from finance_data_agent.experiment.factor_experiment import FactorExperiment, FactorTask
from finance_data_agent.qlib_integration import run_backtest

@dataclass
class Workspace:
    root: Path
    def inject_files(self, **files: dict[str, str]) -> None:
        for fn, content in files.items():
            p = self.root / fn
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

class FactorRunner:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.logger = get_logger("fda.runner", self.settings.log_dir)
        self.backend = APIBackend()
        self.prompts = load_text("finance_data_agent.prompts/qlib_prompts.yaml")

    def propose(self, st) -> dict[str, Any]:
        # Minimal placeholder: return one example task
        t = FactorTask(
            name="Momentum_5_20",
            description="Short-term momentum using 5 vs 20 day returns with volatility adjustment",
            formulation="R = (close/close.shift(5)-1) - (close/close.shift(20)-1)",
            variables="close",
        )
        return {"tasks": [t]}

    def implement(self, st, hyp: dict[str, Any]) -> Workspace:
        ws = Workspace(st.session_dir / f"loop_{st.loop_idx}" / "factor_impl")
        for t in hyp["tasks"]:
            sys = "Implement a robust, vectorized factor function for Qlib backtesting."
            user = (
                load_text("finance_data_agent.prompts/qlib_prompts.yaml")
                + f"\nTask: {t.name}\nDescription: {t.description}\nFormulation: {t.formulation}\nVariables: {t.variables}\n"
            )
            resp = self.backend.build_messages_and_create_chat_completion(user, sys)
            code = self._extract_code(resp)
            ws.inject_files(**{"model.py": code})
        return ws

    def evaluate(self, st, ws: Workspace) -> dict[str, Any]:
        return run_backtest(self.settings, ws.root)

    @staticmethod
    def _extract_code(resp: str) -> str:
        m = re.search(r"```(?:python)?\n(.*?)```", resp, re.S)
        return m.group(1) if m else resp