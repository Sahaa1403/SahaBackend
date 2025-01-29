from rest_framework.response import Response



class CustomResponse(Response):
    __result = None

    def __init__(self, success: bool, status_code: int, errors=None, 
data=None, headers=None,
                 meta=None, content_type='application/json'):
        if errors is None:
            if meta is None:
                self.__result = {
                    "success": success,
                    "data": data
                }
            else:
                self.__result = {
                    "success": success,
                    "meta": meta,
                    "data": data
                }

        else:
            self.__result = {
                "success": success,
                "errors": errors
            }

        # headers = {
        #     'Access-Control-Allow-Headers': '*',
        #     'Access-Control-Allow-Origin': '*',
        #     'Access-Control-Allow-Methods': '*'
        # }
        super(CustomResponse, self).__init__(
            data=self.__result,
            status=status_code,
            headers=headers,
            content_type=content_type
        )


class SuccessResponse(CustomResponse):

    def __init__(self, data=None, meta=None, status_code: int = 200, 
headers=None, content_type='application/json'):
        super(SuccessResponse, self).__init__(
            success=True,
            data=data,
            meta=meta,
            status_code=status_code,
            headers=headers,
            content_type=content_type
        )


class UnsuccessfulResponse(CustomResponse):
    def __init__(self, status_code: int, errors=None, headers=None, 
content_type='application/json'):
        super(UnsuccessfulResponse, self).__init__(
            success=False,
            status_code=status_code,
            errors=errors,
            data=None,
            headers=headers,
            content_type=content_type
        )


def bad_request(errors, headers=None, content_type='application/json') -> UnsuccessfulResponse :
    return UnsuccessfulResponse(
        status_code=400,
        errors=errors,
        headers=headers,
        content_type=content_type
    )


def ok(data, meta=None, headers=None, content_type='application/json') -> SuccessResponse:
    return SuccessResponse(
        data=data,
        status_code=200,
        meta=meta,
        headers=headers,
        content_type=content_type
    )

def no_content(data, meta=None, headers=None, 
content_type='application/json') -> SuccessResponse:
    return SuccessResponse(
        data=data,
        status_code=204,
        meta=meta,
        headers=headers,
        content_type=content_type
    )


def created(data, meta=None, headers=None, 
content_type='application/json') -> SuccessResponse:
    return SuccessResponse(
        data=data,
        status_code=201,
        meta=meta,
        headers=headers,
        content_type=content_type
    )


def conflict(errors, headers=None, content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=409,
        errors=errors,
        headers=headers,
        content_type=content_type
    )


def internal_server_error(errors, headers=None, 
content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=500,
        errors=errors,
        headers=headers,
        content_type=content_type
    )


def forbidden(errors, headers=None, content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=403,
        errors=errors,
        headers=headers,
        content_type=content_type
    )


def unauthorized(errors, headers=None, content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=401,
        errors=errors,
        headers=headers,
        content_type=content_type
    )


def not_found(errors, headers=None, content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=404,
        errors=errors,
        headers=headers,
        content_type=content_type
    )

def not_implemented() -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=501,
        errors={},
        headers=None,
        content_type='application/json'
    )


def generic_unsuccessful(status_code: int, errors, headers=None,
                         content_type='application/json') -> UnsuccessfulResponse:
    return UnsuccessfulResponse(
        status_code=status_code,
        errors=errors,
        headers=headers,
        content_type=content_type
    )

#ss