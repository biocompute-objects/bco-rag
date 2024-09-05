"""Parameter search base class.
"""

import random
import pprint
import time
from logging import Logger
from abc import ABC, abstractmethod
from bcorag.bcorag import BcoRag, supress_stdout
from bcorag.custom_types.core_types import (
    UserSelections,
    DomainKey,
)
from .custom_types import GitDataFileConfig, SearchSpace
from typing import Optional, get_args

STANDARD_BACKOFF = 1


class BcoParameterSearch(ABC):
    """Parent class that lays the foundation for the specific parameter
    search classes. This class shouldn't be instantiated directly.

    Attributes
    ----------
    _files : list[str]
        The files search space.
    _loaders : list[str]
        The data loaders search space.
    _chunking_configs : list[str]
        The chunking strategies search space.
    _embedding_models : list[str]
        The embedding models search space.
    _vector_stores : list[str]
        The vector stores search space.
    _similarity_top_k : list[int]
        The similarity top k search space.
    _llms : list[str]
        The LLM search space.
    _git_data : Optional[list[GitDataFileConfig]]
        The git data to associate with test runs.
    _verbose : bool
        Parameter search verbosity mode.
    _logger : logging.Logger
        The logger to use.
    backoff_time : int | float
        The backoff time between runs. Uses exponential backoff time.
    delay_reset : int
        The amount of runs in between resetting the backoff time. 
    """

    def __init__(
        self,
        search_space: SearchSpace,
        verbose: bool = True,
    ):
        """Constructor.

        Parameters
        ----------
        search_space : SearchSpace
            The parameter search space.
        verbose : bool, optional
            The verbosity level. False for no output, True for running output.
        """

        self._files: list[str] = search_space["filenames"]
        self._loaders: list[str] = search_space["loader"]
        self._chunking_configs: list[str] = search_space["chunking_config"]
        self._embedding_models: list[str] = search_space["embedding_model"]
        self._vector_stores: list[str] = search_space["vector_store"]
        self._similarity_top_k: list[int] = search_space["similarity_top_k"]
        self._llms: list[str] = search_space["llm"]
        self._git_data: Optional[list[GitDataFileConfig]] = search_space["git_data"]
        self._other_docs: Optional[dict[str, list[str]]] = search_space["other_docs"]
        self._verbose: bool = verbose
        self._logger = self._setup_logger()
        self.backoff_time: int | float = STANDARD_BACKOFF
        self.delay_reset = 3

    def train(self):
        """Starts the generation workflow."""

        param_sets = self._create_param_sets()
        for idx, param_set in enumerate(param_sets):

            self._log_output(
                f"------------ Param Set {idx + 1}/{len(param_sets)} ------------"
            )
            self._log_output(param_set)
            t0 = time.time()

            t1 = time.time()
            bco_rag = self._create_bcorag(param_set)
            self._log_output(f"RAG created, elapsed time: {time.time() - t1}")

            t2 = time.time()
            self._generate_domains(bco_rag)
            self._log_output(
                f"Domains generated, total elapsed time: {time.time() - t2}"
            )

            self._log_output(f"Sleeping for {self.backoff_time}...")
            time.sleep(self.backoff_time)
            if idx % self.delay_reset == 0:
                self.backoff_time = STANDARD_BACKOFF
            else:
                self.backoff_time *= 2 + random.uniform(0, 1)

            self._log_output(f"Param set elapsed time: {time.time() - t0}")

    @abstractmethod
    def _setup_logger(self, path: str, name: str) -> Logger:
        """Sets up the logger."""
        pass

    @abstractmethod
    def _create_param_sets(self) -> list[UserSelections]:
        """Creates a list of parameter sets."""
        pass

    def _generate_domains(self, bcorag: BcoRag):
        """Performs the bcorag query on each domain.

        Parameters
        ----------
        bcorag : BcoRag
            The setup BcoRag instance.
        """

        domain: DomainKey
        for domain in get_args(DomainKey):

            t0 = time.time()
            with supress_stdout():
                bcorag.perform_query(domain)
            self._log_output(f"\t{domain.upper()} domain generated, elapsed time: {time.time() - t0}")

    def _create_bcorag(
        self, user_selections: UserSelections
    ) -> BcoRag:
        """Creates the BcoRag instance.

        Parameters
        ----------
        user_selections : UserSelections
            The parameter set.

        Returns
        -------
        BcoRag
            The instantiated BcoRag instance.
        """
        bcorag = BcoRag(user_selections)
        return bcorag

    def _log_output(self, message: str | UserSelections):
        """Handles output. If the logger was passed in handles logging, if
        verbose is `True` handles printing (only info level logging).

        Parameters
        ----------
        message : str | UserSelections
            The message or param set to log and/or print.
        """
        if self._verbose:
            if isinstance(message, str):
                print(message)
            elif isinstance(message, dict):
                pprint.pprint(message)
        if self._logger is not None:
            self._logger.info(message)
