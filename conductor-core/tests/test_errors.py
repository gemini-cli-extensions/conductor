from conductor_core.errors import ConductorError, ErrorCategory, ValidationError


def test_conductor_error_to_dict():
    error = ConductorError("Generic error", ErrorCategory.SYSTEM, {"code": 500})
    data = error.to_dict()
    assert data["error"]["message"] == "Generic error"
    assert data["error"]["category"] == "system"
    assert data["error"]["details"]["code"] == 500


def test_validation_error():
    error = ValidationError("Invalid input", {"field": "username"})
    assert error.category == ErrorCategory.VALIDATION
    assert error.details["field"] == "username"
