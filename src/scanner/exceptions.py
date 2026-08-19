class ScannerError(Exception):
    """Base exception class for all scanner-related errors."""
    pass


class DependencyError(ScannerError):
    """Raised when a required system dependency or tool is missing."""
    pass


class GitOperationError(ScannerError):
    """Raised when a Git command fails or cloned repository processing fails."""
    pass
