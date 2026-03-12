# Architecture

ArchForge is structured as a small platform rather than a single-purpose script. The CLI delegates orchestration to generators, generators depend on services and builders, and the template catalog is separated from the runtime logic.

## Internal Layers

- `cli`: command surface and user feedback
- `core`: domain-neutral models, contracts, constants, and exceptions
- `builders`: construction of template manifests
- `factories`: resolution of framework and persistence strategies
- `generators`: lifecycle orchestration for projects and modules
- `services`: filesystem, validation, and template rendering concerns
- `strategies`: framework and database variability points
- `templates`: generated service assets and reusable module templates

## Generated Service Boundaries

Generated services follow Clean Architecture boundaries:

- `domain`: entities, repository interfaces, and domain services
- `application`: use cases, DTOs, and interface contracts
- `infrastructure`: configuration, logging, persistence, and repository implementations
- `presentation`: FastAPI routes, dependency providers, and request or response schemas