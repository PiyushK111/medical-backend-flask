from flask import jsonify

def success_response(data=None, message="Operation successful", status_code=200):
    """
    Standard successful response wrapper.
    """
    response = {
        "success": True,
        "message": message,
        "data": data,
        "error": None
    }
    return jsonify(response), status_code

def error_response(message="An error occurred", errors=None, status_code=400):
    """
    Standard error response wrapper.
    """
    response = {
        "success": False,
        "message": message,
        "data": None,
        "error": errors or message
    }
    return jsonify(response), status_code

def validation_error_handler(err):
    """
    Helper to format marshmallow validation errors.
    """
    return error_response(
        message="Validation Error",
        errors=err.messages,
        status_code=422
    )
