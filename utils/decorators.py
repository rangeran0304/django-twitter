from rest_framework.response import Response
from rest_framework import  status
from functools import  wraps

def required_params( request_attr='query_params',params = None):
    if params is None:
        params = []
    def decorator(func):
        @wraps(func)
        def wrapped_view (instance,request,*args,**kargs):
            data = getattr(request,request_attr)
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                missed_params = ','.join(missing_params)
                return Response(
                    {
                        'message': 'missing the required_param {}'.format(missed_params),
                        'success': 'False'
                    }
                    ,status = status.HTTP_400_BAD_REQUEST
                )
            return func(instance,request,*args,**kargs)
        return wrapped_view
    return decorator