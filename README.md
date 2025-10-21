# Finance Data Agent (VER 0.1)
## 🚧 Project Status: Under Development 🚧  


A lightweight, standalone version of the "Finance Data Agent" from RD-Agent.
It proposes factor hypotheses, implements factor code via LLM, and backtests via Qlib(UNDER DISCUSSION) in an iterative loop.

## **Research Acknowledgments**
We are grateful for the foundational research papers that inspired and guided this project:
- [Alpha-GPT: Human-AI Interactive Alpha Mining for Quantitative Investment](https://arxiv.org/pdf/2308.00016)
- [https://arxiv.org/abs/2505.15155]

## Install

```bash
pip install -e .
```

## Quickstart

```bash
# Prepare env vars for your LLM backend
export LLM_API_BASE="https://api.your-llm.com/v1"
export LLM_API_KEY="sk-..."
export LLM_MODEL="gpt-4o-mini"

# Ensure Qlib data exists (default: ~/.qlib/qlib_data/cn_data)
fda run --loop-n 1 --timeout 2h
```

## Config (env)

You can override Factor settings via env (prefix `FACTOR_COSTEER_`):

- `FACTOR_COSTEER_DATA_FOLDER`
- `FACTOR_COSTEER_DATA_FOLDER_DEBUG`
- `FACTOR_COSTEER_PYTHON_BIN`
- `FACTOR_COSTEER_FILE_BASED_EXECUTION_TIMEOUT`
- `FACTOR_COSTEER_SELECT_METHOD`
- `FACTOR_COSTEER_QLIB_PROVIDER_URI`
- `FACTOR_COSTEER_QLIB_MARKET`
- `FACTOR_COSTEER_QLIB_BENCHMARK`
- `FACTOR_COSTEER_LOG_DIR`

## Status

- v0.1: Minimal loop wired; Qlib backtest is a placeholder. Replace with full pipeline in `qlib_integration.py`.
