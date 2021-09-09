from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response(f"Hello {request.args.get('name', 'World!')}!")

