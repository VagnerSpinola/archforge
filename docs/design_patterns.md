# Design Patterns

## Factory Pattern

`FrameworkFactory` selects the framework and database strategies for project generation.

## Builder Pattern

`ProjectBuilder` assembles the template manifest for a project using the selected strategies.

## Strategy Pattern

Framework and database choices are modeled as strategies so project generation can evolve without branching logic spreading across the codebase.

## Template Method

`BaseGenerator` defines the generation lifecycle and `ProjectGenerator` implements the concrete steps.

## Repository Pattern And Unit Of Work

Generated services model persistence boundaries through repository interfaces and unit of work contracts, keeping application logic insulated from infrastructure choices.

## Dependency Injection

Generated services isolate composition in the presentation dependency layer so use cases depend on contracts rather than concrete framework state.