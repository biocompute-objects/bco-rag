"""Base evaluation frame, enforces the update state and get results methods.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from evaluator.backend.custom_types import AppState, RunState

T = TypeVar("T")


class EvaluationBaseFrame(ABC, Generic[T]):

    @abstractmethod
    def __init__(self, master, app_state: AppState, run_state: RunState, **kwargs):
        pass

    @abstractmethod
    def update_state(self, app_state: AppState, run_state: RunState) -> None:
        """Upate the component state.

        Parameters
        ----------
        app_state : AppState
            The updated app state.
        run_state : RunState
            The updated run state.
        """
        pass

    @abstractmethod
    def get_results(self) -> T:
        """Gets the results for the current state of the evaluation frame.

        Returns
        -------
        T
            The specific evaluation TypedDict for the frame.
        """
        pass
