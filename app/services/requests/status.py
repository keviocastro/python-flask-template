def code_message(message_or_code):
    if message_or_code == 1:
        message = "Registered successfully"
    elif message_or_code == 2:
        message = "Query made successfully"
    elif message_or_code == 3:
        message = "Updated successfully"
    elif message_or_code == 4:
        message = "Deleted successfully"
    elif message_or_code == 5:
        message = "Missing field"
    elif message_or_code == 6:
        message = "Not Found"
    elif message_or_code == 7:
        message = "Already registered"
    elif message_or_code == 8:
        message = "Already Deleted"
    elif message_or_code == 9:
        message = "Status change not permitted. The data was not updated"
    else:
        message = message_or_code

    return message


def code_http(code):
    if code == 200:
        status = "OK"
    if code == 201:
        status = "Created"
    if code == 206:
        status = "Partial Content"
    if code == 302:
        status = "Found"
    if code == 400:
        status = "Bad Request"
    if code == 401:
        status = "Unauthorized"
    if code == 402:
        status = "Payment Unauthorized"
    if code == 403:
        status = "Forbidden"
    if code == 404:
        status = "Not Found"
    if code == 405:
        status = "Method Not Allowed"
    if code == 406:
        status = "Not Acceptable"
    if code == 409:
        status = "Conflict"
    if code == 415:
        status = "Unsupported Media Type"
    if code == 429:
        status = "Too Many Request"
    if code == 500:
        status = "Internal Server Error"
    if code == 503:
        status = "Service Unavailable"

    return status
