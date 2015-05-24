import traceback
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import unauthenticated_userid


def generic(context, request):
    request.response.status_int = 500
    try:
        response = {'message': context.args[0]}
    except IndexError:
        response = {'message': 'Unknown error'}
    if request.registry.settings.get('pyramid_raml.debug'):
        response['traceback'] = ''.join(
                traceback.format_exception(*request.exc_info))
    return response


def http_error(context, request):
    request.response.status = context.status
    for (header, value) in context.headers.items():
        if header in {'Content-Type', 'Content-Length'}:
            continue
        request.response.headers[header] = value
    if context.message:
        return {'message': context.message}
    else:
        return {'message': context.status}


def notfound(context, request):
    message = 'Resource not found'
    if isinstance(context, HTTPNotFound):
        if context.content_type == 'application/json':
            return context
        elif context.detail:
            message = context.detail
    request.response.status_int = 404
    return {
        'success': False,
        'message': message
    }


def forbidden(request):
    if unauthenticated_userid(request):
        request.response.status_int = 403
        return {
            'success': False,
            'message': 'You are not allowed to perform this action.'
        }
    else:
        request.response.status_int = 401
        return {
            'success': False,
            'message': 'You must login to perform this action.'
        }
