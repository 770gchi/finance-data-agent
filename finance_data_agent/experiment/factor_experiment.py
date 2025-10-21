from dataclasses import dataclass

@dataclass
class FactorTask:
    name: str
    description: str
    formulation: str
    variables: str

@dataclass
class FactorExperiment:
    sub_tasks: list[FactorTask]