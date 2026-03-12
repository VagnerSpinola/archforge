# Getting Started

## Install ArchForge

```bash
pip install archforge
```

## Create A Service

```bash
archforge new payment-service
```

Use a specific project template when needed:

```bash
archforge new job-runner --template worker-service
archforge new order-events --template event-driven-service
```

## Run Quality Checks In This Repository

```bash
make install
make lint
make typecheck
make test
```

## Extend A Generated Service

From inside a generated project root:

```bash
archforge add entity payment
archforge add use-case create-payment
archforge add repository payment
archforge add endpoint payments
```

## Observability Flags

Generated services include observability scaffolding that is controlled through environment-backed settings:

```bash
STRUCTURED_LOGGING_ENABLED=true
REQUEST_ID_ENABLED=true
READINESS_ENABLED=true
METRICS_ENABLED=false
OTEL_ENABLED=false
```

The generated HTTP services expose `/api/v1/health` by default, `/api/v1/readiness` when readiness checks are enabled, and `/api/v1/metrics` when metrics are enabled. For OpenTelemetry bootstrap support, install the generated project's optional `observability` extra.