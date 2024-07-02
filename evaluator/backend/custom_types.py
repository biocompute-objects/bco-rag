"""Handles the custom types for the App backend.
"""

from typing import Optional, TypedDict, Literal, cast
from logging import Logger
from bcorag import misc_functions as misc_fns
import json
from deepdiff import DeepDiff  # type: ignore

### JSON configuration schema


class ConfigData(TypedDict):
    """Defines the schema for the JSON config data."""

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


## Score evaluationa schemas

ScoreEvalLiteral = Literal["Lower", "About right", "Higher"]


class ScoreEval(TypedDict):
    """TypedDict for the score evaluations."""

    eval: ScoreEvalLiteral
    eval_code: int
    notes: str


def create_score_eval(eval: ScoreEvalLiteral, notes: str) -> ScoreEval:
    """Constructor for the ScoreEval TypedDict."""
    eval_str = str(eval.strip().lower())

    eval_code = 0
    match eval_str:
        case "lower":
            eval_code = -1
        case "higher":
            eval_code = 1

    return_data: ScoreEval = {"eval": eval, "eval_code": eval_code, "notes": notes}

    return return_data


def cast_score_eval(score_eval_str: str) -> ScoreEvalLiteral:
    """Cast a string to ScoreEvalLiteral (if possible)."""
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
    """Error evaluation data."""

    inferred_knowledge_error: bool
    external_knowledge_error: bool
    other_error: bool
    notes: str


def create_error_val(
    inf_err: bool | str, ext_err: bool | str, other_err: bool | str, notes: str
) -> ErrorEval:
    """Constructor for the ErrorEval TypedDict."""
    if isinstance(inf_err, str):
        inf_err = cast_error_type(inf_err)
    if isinstance(ext_err, str):
        ext_err = cast_error_type(ext_err)
    if isinstance(other_err, str):
        other_err = cast_error_type(other_err)

    return_data: ErrorEval = {
        "inferred_knowledge_error": inf_err,
        "external_knowledge_error": ext_err,
        "other_error": other_err,
        "notes": notes,
    }
    return return_data


def cast_error_type(err: str) -> bool:
    """Cast checkbox string to boolean."""
    err = err.strip().lower()
    if err == "on":
        return True
    elif err == "off":
        return False
    raise ValueError(f"Error casting `{err}` to bool.")


def reverse_cast_error_type(err: bool) -> str:
    """Reverse cast checkbox bool to string."""
    if err:
        return "on"
    else:
        return "off"


## Full evaluation data schemas


class EvalData(TypedDict):
    """Full evaluation data."""

    score_eval: ScoreEval
    error_eval: ErrorEval


def create_full_eval(score_eval: ScoreEval, error_eval: ErrorEval) -> EvalData:
    """Constructor for the EvalData TypedDict."""
    return_data: EvalData = {"score_eval": score_eval, "error_eval": error_eval}
    return return_data


def load_score_defaults(
    filepath: str = "./evaluator/backend/score_defaults.json",
) -> Optional[EvalData]:
    """Loads the score defaults JSON file."""
    naive_load_data = misc_fns.load_json(filepath)
    if naive_load_data is None:
        return None
    if isinstance(naive_load_data, dict):
        eval_defaults = cast(EvalData, naive_load_data)
        return eval_defaults
    return None


def default_eval() -> EvalData:
    """Get a default EvalData."""
    eval_defaults = load_score_defaults()
    if eval_defaults is None:
        misc_fns.graceful_exit(1, "Error loading score defaults.")
    return eval_defaults


def check_default_eval(val: dict | EvalData) -> bool:
    """Checks if the EvalData is still the default. This
    helps to prevent saving erroneous save data.
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
    "domain",
    "generated_domain",
    "generated_file_path",
    "human_curated_domain",
    "param_set",
    "reference_nodes",
    "run_index",
    "total_runs",
    "already_evaluated",
    "logger",
]


class RunState(TypedDict):
    """Holds the data for the current run being evaluated."""

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
    """Constructor for the RunState TypedDict."""
    score = -1.0
    score_version = 0.0
    if isinstance(generated_domain, dict):
        # TODO : whenever the BCO score API endpoint is
        # created hit that here.
        generated_domain = json.dumps(generated_domain, indent=4)

    return_data: RunState = {
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
    """Handles the app initialization attributes."""

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
    """Constructor for the AppAttributes TypedDict."""
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
    """Constructor for the AppState TypedDict."""
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
