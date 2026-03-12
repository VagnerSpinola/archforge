class ArchforgeError(Exception):
    """Base exception for archforge."""


class ValidationError(ArchforgeError):
    """Raised when user input does not satisfy project rules."""


class InvalidProjectError(ArchforgeError):
    """Raised when a command targets an invalid project directory."""


class FileConflictError(ArchforgeError):
    """Raised when a file operation would overwrite an existing file."""


class TemplateError(ArchforgeError):
    """Raised when a Jinja template cannot be resolved or rendered."""


class PluginError(ArchforgeError):
    """Raised when a plugin cannot be loaded or registered."""