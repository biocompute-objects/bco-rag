"""Handles the custom types for the App backend.

Type Aliases
------------
- ```ScoreEvalLiteral = Literal["Lower", "About right", "Higher"]```
- ```RunStateKey = Literal["paper",
        "domain",
        "generated_domain",
        "score",
        "score_version",
        "generated_file_path",
        "human_curated_domain",
        "param_set",
        "reference_nodes",
        "run_index",
        "total_runs",
        "already_evaluated",
        "logger",
        "eval_data"]```
- ```AppStateKey = Literal["logger",
        "results_dir_path",
        "bco_results_file_name",
        "bco_results_data",
        "user_results_file_name",
        "user_results_data",
        "users_file_name",
        "users_data",
        "generated_directory_paths",
        "padding",
        "font",
        "user_hash"]```
"""

from typing import Optional, TypedDict, Literal, cast
from logging import Logger
from bcorag import misc_functions as misc_fns
import json
from deepdiff import DeepDiff  # type: ignore


def cast_checkbox(val: str) -> bool:
    """Cast checkbox string to boolean (assuming checkbox values are `on`, `off`).

    Parameters
    ----------
    val : str
        The value to cast.

    Returns
    -------
    bool
        The casted checkbox value.
    """
    val = val.strip().lower()
    if val == "on":
        return True
    elif val == "off":
        return False
    raise ValueError(f"Error casting `{val}` to bool.")


def reverse_cast_checkbox(err: bool) -> str:
    """Reverse cast checkbox bool to string (assuming checkbox values are `on`, `off`).

    Parameters
    ----------
    err : bool
        The value to revserse cast.

    Returns
    -------
    str
        The reverse casted value.
    """
    if err:
        return "on"
    else:
        return "off"


### JSON configuration schema


class ConfigData(TypedDict):
    """Defines the schema for the JSON config data.

    Attributes
    ----------
    logger_path : str
        The path to the logger.
    logger_name : str
        The name of the logger.
    generated_output_dir_path : str
        The filepath to the generated domains directory to evaluate.
    glob_pattern : str
        The glob patterns to traverse the generated output directory.
    results_dir_path : str
        The path to the directory to dump the evaluation results.
    ignore_files : list[str]
        Identifiers to ignore certain files (used like `if ignore_files[x] in filename`).
    bco_results_file_name : str
        The file name for the BCO results file.
    user_results_file_name : str
        The file name for the user evaluations results file.
    users_file_name : str
        The file name for the users file.
    padding : int
        The default root padding used throughout the frontend components.
    font : str
        The default font used throughout the frontend components.
    """

    logger_path: str
    logger_name: str
    generated_output_dir_path: str
    glob_pattern: str
    results_dir_path: str
    ignore_files: list[str]
    bco_results_file_name: str
    user_results_file_name: str
    users_file_name: str
    padding: int
    font: str


### Evaluation Schemas


## Score evaluation schemas

ScoreEvalLiteral = Literal["Lower", "About right", "Higher"]


class ScoreEval(TypedDict):
    """Score evaluation results.

    Attributes
    ----------
    eval : ScoreEvalLiteral
        The score eval literal.
    eval_code : int
        The casted score eval literal.
    notes : str
        Any additional notes from the evaluator regarding the score evaluation.
    """

    eval: ScoreEvalLiteral
    eval_code: int
    notes: str


def create_score_eval(eval: ScoreEvalLiteral, notes: str) -> ScoreEval:
    """Constructor for the ScoreEval TypedDict. The score eval literal
    will be automatically casted to the eval code.

    Parameters
    ----------
    eval : ScoreEvalLiteral
        The score eval literal.
    notes : str
        Any additional notes from the evaluator regarding the score evaluation.

    Returns
    -------
    ScoreEval
    """
    eval_str = str(eval.strip().lower())

    eval_code = 0
    match eval_str:
        case "lower":
            eval_code = -1
        case "higher":
            eval_code = 1

    return_data: ScoreEval = {
        "eval": eval,
        "eval_code": eval_code,
        "notes": notes.strip(),
    }

    return return_data


def cast_score_eval(score_eval_str: str) -> ScoreEvalLiteral:
    """Cast a string to ScoreEvalLiteral (if possible).

    Parameters
    ----------
    score_eval_str : str
        The string to cast.

    Returns
    -------
    ScoreEvalLiteral
    """
    score_eval_str = score_eval_str.strip().lower()
    match score_eval_str:
        case "lower":
            return "Lower"
        case "about right":
            return "About right"
        case "higher":
            return "Higher"
    raise ValueError(f"Error casting `{score_eval_str}` to ScoreEvalLiteral.")


## Error evaluation schemas


class ErrorEval(TypedDict):
    """Error evaluation data.

    Attributes
    ----------
    inferred_knowledge_error: bool
        Whether there was an inferred knowledge error.
    external_knowledge_error: bool
        Whether there was an external knowledge error.
    json_format_error: bool
        Whether there was a JSON formatting error.
    other_error: bool
        Whether there was any other error.
    notes: str
        Any additional notes from the evaluator regarding the error evaluation.
    """

    inferred_knowledge_error: bool
    external_knowledge_error: bool
    json_format_error: bool
    other_error: bool
    notes: str


def create_error_val(
    inf_err: bool | str,
    ext_err: bool | str,
    json_err: bool | str,
    other_err: bool | str,
    notes: str,
) -> ErrorEval:
    """Constructor for the ErrorEval TypedDict.

    Parameters
    ----------
    inf_err : bool | str
        The inferred knowledge error indicator.
    ext_err : bool | str
        The external knowledge error indicator.
    json_err : bool | str
        The JSON formattign error indicator.
    notes : str
        Any additional notes from the evaluator regarding the error evaluation.
    """
    if isinstance(inf_err, str):
        inf_err = cast_checkbox(inf_err)
    if isinstance(ext_err, str):
        ext_err = cast_checkbox(ext_err)
    if isinstance(json_err, str):
        json_err = cast_checkbox(json_err)
    if isinstance(other_err, str):
        other_err = cast_checkbox(other_err)

    return_data: ErrorEval = {
        "inferred_knowledge_error": inf_err,
        "external_knowledge_error": ext_err,
        "json_format_error": json_err,
        "other_error": other_err,
        "notes": notes.strip(),
    }
    return return_data


## Reference node evaluation schemas


class RefereceEval(TypedDict):
    """Reference evaluation data.

    Attributes
    ----------
    reference_relevancy : int
        Indicates how relevant the reference nodes were to the domain.
    top_reference_retrieval : bool
        Whether the top node retrieved was the most relevant.
    notes : str
        Any additional notes from the evaluator regarding the reference evaluation.
    """

    reference_relevancy: int
    top_reference_retrieval: bool
    notes: str


def create_reference_eval(
    reference_relevancy: int, top_reference_retrieval: bool | str, notes: str
) -> RefereceEval:
    """Constructor for the RefereceEval TypedDict.

    Parameters
    ----------
    reference_relevancy : int
        Indicates how relevant the reference nodes were to the domain.
    top_reference_retrieval : bool
        Whether the top node retrieved was the most relevant.
    notes : str
        Any additional notes from the evaluator regarding the reference evaluation.

    Returns
    -------
    ReferenceEval
    """
    if isinstance(top_reference_retrieval, str):
        top_reference_retrieval = cast_checkbox(top_reference_retrieval)

    return_data: RefereceEval = {
        "reference_relevancy": reference_relevancy,
        "top_reference_retrieval": top_reference_retrieval,
        "notes": notes.strip(),
    }

    return return_data


## General evaluation schemas


class GeneralEval(TypedDict):
    """General evaluation data.

    Attributes
    ----------
    relevancy : int
        Indicates how relevant the generated domain was.
    readability : int
        Indicates how readable the generated domain was.
    reproducibility : int
        Indicates how reproduceable the domain steps are.
    confidence_rating : int
        Indicates how confident the evaluator was in their evaluation.
    notes : str
        Any additional notes from the evaluator regarding the general evaluation.
    """

    relevancy: int
    readability: int
    reproducibility: int
    confidence_rating: int
    notes: str


def create_general_eval(
    relevancy: int,
    readability: int,
    reproducibility: int,
    confidence_rating: int,
    notes: str,
) -> GeneralEval:
    """Constructor for the GeneralEval TypedDict.

    Parameters
    ----------
    relevancy : int
        Indicates how relevant the generated domain was.
    readability : int
        Indicates how readable the generated domain was.
    reproducibility : int
        Indicates how reproduceable the domain steps are.
    confidence_rating : int
        Indicates how confident the evaluator is in the generated domain.
    notes : str
        Any additional notes from the evaluator regarding the general evaluation.

    Returns
    -------
    GeneralEval
    """
    return_data: GeneralEval = {
        "relevancy": relevancy,
        "readability": readability,
        "reproducibility": reproducibility,
        "confidence_rating": confidence_rating,
        "notes": notes.strip(),
    }
    return return_data


## Miscellaneous evaluation data schemas


class MiscEval(TypedDict):
    """Miscellaneous evaluation data.

    Attributes
    ----------
    human_domain_rating : int
        The high level human domain rating for the generated domain.
    evaluator_confidence_rating : int
        Indicates how confident the evaluator is in their evaluation.
    evaluator_familiarity_level: int
        Indicates how familiar the evaluator is with the paper content.
    notes : str
        Any additional notes from the evaluator regarding the miscellaneous evaluation.
    """

    human_domain_rating: int
    evaluator_confidence_rating: int
    evaluator_familiarity_level: int
    notes: str


def create_misc_eval(
    human_domain_rating: int,
    evaluator_confidence_rating: int,
    evaluator_familiarity_level: int,
    notes: str,
) -> MiscEval:
    """Constructor for the MiscEval TypedDict.

    Parameters
    ----------
    human_domain_rating : int
        The high level human domain rating for the generated domain.
    evaluator_confidence_rating : int
        Indicates how confident the evaluator is in their evaluation.
    evaluator_familiarity_level: int
        Indicates how familiar the evaluator is with the paper content.
    notes : str
        Any additional notes from the evaluator regarding the miscellaneous evaluation.

    Returns
    -------
    MiscEval
    """
    return_data: MiscEval = {
        "human_domain_rating": human_domain_rating,
        "evaluator_confidence_rating": evaluator_confidence_rating,
        "evaluator_familiarity_level": evaluator_familiarity_level,
        "notes": notes.strip(),
    }
    return return_data


## Full evaluation data schemas


class EvalData(TypedDict):
    """Full evaluation data.

    Attributes
    ----------
    score_eval: ScoreEval
    error_eval: ErrorEval
    reference_eval: RefereceEval
    general_eval: GeneralEval
    misc_eval: MiscEval
    """

    score_eval: ScoreEval
    error_eval: ErrorEval
    reference_eval: RefereceEval
    general_eval: GeneralEval
    misc_eval: MiscEval


def create_full_eval(
    score_eval: ScoreEval,
    error_eval: ErrorEval,
    reference_eval: RefereceEval,
    general_eval: GeneralEval,
    misc_eval: MiscEval,
) -> EvalData:
    """Constructor for the EvalData TypedDict.

    Parameters
    ----------
    score_eval: ScoreEval
    error_eval: ErrorEval
    reference_eval: RefereceEval
    general_eval: GeneralEval
    misc_eval: MiscEval
    """
    return_data: EvalData = {
        "score_eval": score_eval,
        "error_eval": error_eval,
        "reference_eval": reference_eval,
        "general_eval": general_eval,
        "misc_eval": misc_eval,
    }
    return return_data


def load_score_defaults(
    filepath: str = "./evaluator/backend/score_defaults.json",
) -> Optional[EvalData]:
    """Loads the score defaults JSON file.

    Parameters
    ----------
    filepath : str, optional
        The filepath to the score defaults JSON file.

    Returns
    -------
    EvalData | None
        The evaluation data with the default values or None on error.
    """
    naive_load_data = misc_fns.load_json(filepath)
    if naive_load_data is None:
        return None
    if isinstance(naive_load_data, dict):
        eval_defaults = cast(EvalData, naive_load_data)
        return eval_defaults
    return None


def default_eval() -> EvalData:
    """Get a default EvalData.

    Returns
    -------
    EvalData
    """
    eval_defaults = load_score_defaults()
    if eval_defaults is None:
        misc_fns.graceful_exit(1, "Error loading score defaults.")
    return eval_defaults


def check_default_eval(val: dict | EvalData) -> bool:
    """Checks if the EvalData is still the default. This
    helps to prevent saving erroneous save data.

    Parameters
    ----------
    val : dict | EvalData
        The evaluation data to check.

    Returns
    -------
    bool
        True if still the default, False if different.
    """
    default_eval_dict = default_eval()
    diff = DeepDiff(
        default_eval_dict,
        val,
        ignore_order=True,
        ignore_string_case=True,
        ignore_nan_inequality=True,
    )
    if diff == {}:
        return True
    else:
        return False


### Run state schemas

RunStateKey = Literal[
    "paper",
    "domain",
    "generated_domain",
    "score",
    "score_version",
    "generated_file_path",
    "human_curated_domain",
    "param_set",
    "reference_nodes",
    "run_index",
    "total_runs",
    "already_evaluated",
    "logger",
    "eval_data"
]


class RunState(TypedDict):
    """Holds the data for the current run being evaluated.

    Attributes
    ----------
    paper: str
        The paper for the current run state.
    domain: str
        The domain the current run is for.
    generated_domain: str
        The generated domain string for the current run.
    score: float
        The score for the current run (from the BCO score API).
    score_version: float
        The score version for the score (from the BCO score API).
    generated_file_path: str
        The generated domain file path (points to the JSON file if valid JSON, otherwise points to the raw text file).
    human_curated_domain: str
        The human curated domain string.
    param_set: str
        The parameter set string for the run.
    reference_nodes: str
        The retrieved reference node values.
    run_index: int
        The run index.
    total_runs: int
        The total number of runs to potentially evaluate.
    already_evaluated: bool
        Whether the user has already evaluated this run.
    logger: Logger
        The logger for the App.
    eval_data: EvalData
        The evaluation data for the run.
    """

    paper: str
    domain: str
    generated_domain: str
    score: float
    score_version: float
    generated_file_path: str
    human_curated_domain: str
    param_set: str
    reference_nodes: str
    run_index: int
    total_runs: int
    already_evaluated: bool
    logger: Logger
    eval_data: EvalData


def create_run_state(
    paper: str,
    domain: str,
    generated_domain: str | dict,
    generated_file_path: str,
    human_curated_domain: str,
    param_set: str,
    reference_nodes: str,
    run_index: int,
    total_runs: int,
    already_evaluated: bool,
    logger: Logger,
    eval_data: EvalData,
) -> RunState:
    """Constructor for the RunState TypedDict.

    Parameters
    ----------
    paper: str
        The paper for the current run state.
    domain: str
        The domain the current run is for.
    generated_domain: str | dict
        The generated domain for the current run.
    generated_file_path: str
        The generated domain file path (points to the JSON file if valid JSON, otherwise points to the raw text file).
    human_curated_domain: str
        The human curated domain string.
    param_set: str
        The parameter set string for the run.
    reference_nodes: str
        The retrieved reference node values.
    run_index: int
        The run index.
    total_runs: int
        The total number of runs to potentially evaluate.
    already_evaluated: bool
        Whether the user has already evaluated this run.
    logger: Logger
        The logger for the App.
    eval_data: EvalData
        The evaluation data for the run.
    """
    score = -1.0
    score_version = 0.0
    if isinstance(generated_domain, dict):
        # TODO : whenever the BCO score API endpoint is
        # created hit that here.
        generated_domain = json.dumps(generated_domain, indent=4)

    return_data: RunState = {
        "paper": paper,
        "domain": domain,
        "generated_domain": generated_domain,
        "score": score,
        "score_version": score_version,
        "generated_file_path": generated_file_path,
        "human_curated_domain": human_curated_domain,
        "param_set": param_set,
        "reference_nodes": reference_nodes,
        "run_index": run_index,
        "total_runs": total_runs,
        "already_evaluated": already_evaluated,
        "logger": logger,
        "eval_data": eval_data,
    }
    return return_data


### Application attributes schema


class AppAttributes(TypedDict):
    """Handles the app initialization attributes.

    Attributes
    ----------
    logger : Logger
        The App logger.
    results_dir_path : str
        The path to the directory to dump the evaluation results.
    bco_results_file_name : str
        The file name for the BCO results file.
    bco_results_data: dict
        The aggregates BCO results data.
    user_results_file_name: str
        The file name for the user evaluations results file.
    user_results_data: dict[str, dict[str, EvalData | None] | None]
        The user evaluation results.
    users_file_name: str
        The file name for the users file.
    users_data: dict
        The users data.
    generated_output_dir_root: str
        The root filepath to the generated domains directory to evaluate.
    generated_directory_paths: list[str]
        List of directory paths for all the papers.
    padding: int
        The default root padding to use for all the frontend components.
    font: str
        The default font to use for all the frontend components. 
    """

    logger: Logger
    results_dir_path: str
    bco_results_file_name: str
    bco_results_data: dict
    user_results_file_name: str
    user_results_data: dict[str, dict[str, EvalData | None] | None]
    users_file_name: str
    users_data: dict
    generated_output_dir_root: str
    generated_directory_paths: list[str]
    padding: int
    font: str


def create_app_attributes(
    logger: Logger,
    results_dir_path: str,
    bco_results_file_name: str,
    bco_results_data: dict,
    user_results_file_name: str,
    user_results_data: dict[str, dict[str, EvalData | None] | None],
    users_file_name: str,
    users_data: dict,
    generated_output_dir_root: str,
    generated_directory_paths: list[str],
    padding: int,
    font: str,
) -> AppAttributes:
    """Constructor for the AppAttributes TypedDict.

    Parameters
    ----------
    logger : Logger
        The App logger.
    results_dir_path : str
        The path to the directory to dump the evaluation results.
    bco_results_file_name : str
        The file name for the BCO results file.
    bco_results_data: dict
        The aggregates BCO results data.
    user_results_file_name: str
        The file name for the user evaluations results file.
    user_results_data: dict[str, dict[str, EvalData | None] | None]
        The user evaluation results.
    users_file_name: str
        The file name for the users file.
    users_data: dict
        The users data.
    generated_output_dir_root: str
        The root filepath to the generated domains directory to evaluate.
    generated_directory_paths: list[str]
        List of directory paths for all the papers.
    padding: int
        The default root padding to use for all the frontend components.
    font: str
        The default font to use for all the frontend components. 
    """
    return_data: AppAttributes = {
        "logger": logger,
        "results_dir_path": results_dir_path,
        "bco_results_file_name": bco_results_file_name,
        "bco_results_data": bco_results_data,
        "user_results_file_name": user_results_file_name,
        "user_results_data": user_results_data,
        "users_file_name": users_file_name,
        "users_data": users_data,
        "generated_output_dir_root": generated_output_dir_root,
        "generated_directory_paths": generated_directory_paths,
        "padding": padding,
        "font": font,
    }
    return return_data


### App state schemas

AppStateKey = Literal[
    "logger",
    "results_dir_path",
    "bco_results_file_name",
    "bco_results_data",
    "user_results_file_name",
    "user_results_data",
    "users_file_name",
    "users_data",
    "generated_directory_paths",
    "padding",
    "font",
    "user_hash",
]


class AppState(AppAttributes):
    """Holds the application state information, essentially
    just the attributes plus the current user hash, new user
    flag and start from last session boolean.

    Attributes
    ----------
    user_hash: str
        The user hash.
    new_user: bool
        New user flag.
    resume_session: bool
        Resume session flag.
    """

    user_hash: str
    new_user: bool
    resume_session: bool


def create_app_state(
    attributes: AppAttributes,
    user_hash: str,
    new_user: bool,
    resume_session: bool = False,
) -> AppState:
    """Constructor for the AppState TypedDict.

    Parameters
    ----------
    attributes : AppAttributes
        The app attributes to base the state off of.
    user_hash: str
        The user hash.
    new_user: bool
        New user flag.
    resume_session: bool, optional
        Resume session flag.

    Returns
    -------
    AppState
    """
    return_data: AppState = {
        "logger": attributes["logger"],
        "results_dir_path": attributes["results_dir_path"],
        "bco_results_file_name": attributes["bco_results_file_name"],
        "bco_results_data": attributes["bco_results_data"],
        "user_results_file_name": attributes["user_results_file_name"],
        "user_results_data": attributes["user_results_data"],
        "users_file_name": attributes["users_file_name"],
        "users_data": attributes["users_data"],
        "generated_output_dir_root": attributes["generated_output_dir_root"],
        "generated_directory_paths": attributes["generated_directory_paths"],
        "padding": attributes["padding"],
        "font": attributes["font"],
        "user_hash": user_hash,
        "new_user": new_user,
        "resume_session": resume_session,
    }
    return return_data
