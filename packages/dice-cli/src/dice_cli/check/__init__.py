from typing import Any, Callable, Dict, List

import typer

from ..logger import user_logger
from ._environment import EnvironmentScope, get_env_for_scope, prepare_table

app = typer.Typer(help="DICE commands for various checks")


def add_enum_as_options(enum_class: Any) -> Callable[..., Any]:
    import inspect

    def change_params(func: Callable[..., Any]) -> Callable[..., Any]:
        params = []
        annotations = {}
        for e in enum_class:
            param = inspect.Parameter(
                e.name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=bool,
                default=typer.Option(
                    False, "--" + e.value, help=f"Show environment for {e.value}"
                ),
            )
            params.append(param)
            annotations[e.value] = bool
        func.__signature__ = inspect.Signature(params)  # type: ignore[attr-defined]
        func.__annotations__ = annotations
        return func

    return change_params


@app.command()
@add_enum_as_options(enum_class=EnvironmentScope)
def environment(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
    """
    Check environment
    """
    for name, value in kwargs.items():
        if not value:
            continue
        scope = EnvironmentScope[name]
        user_logger.debug(f"Checking environment with scope={scope.value}:")
        env_vars = get_env_for_scope(scope)
        if not env_vars:
            user_logger.warning(
                f"No environment variables found in scope={scope.value}"
            )
            continue

        table = prepare_table(env_vars)

        user_logger.info(table)
