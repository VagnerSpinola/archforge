from pathlib import Path

GENERATED_SOURCE_DIRECTORIES = (
    Path("src/domain/entities"),
    Path("src/domain/repositories"),
    Path("src/domain/services"),
    Path("src/application/dto"),
    Path("src/application/interfaces"),
    Path("src/application/use_cases"),
    Path("src/infrastructure/config"),
    Path("src/infrastructure/logging"),
    Path("src/infrastructure/persistence"),
    Path("src/infrastructure/repositories"),
    Path("src/presentation/api"),
    Path("src/presentation/dependencies"),
    Path("src/presentation/schemas"),
)

REQUIRED_PROJECT_MARKERS = (
    Path("src/domain"),
    Path("src/application"),
    Path("src/infrastructure"),
    Path("src/presentation"),
    Path("pyproject.toml"),
)