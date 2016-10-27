from json import dumps
from aiohttp.web_exceptions import HTTPBadRequest
from jsonschema.exceptions import ValidationError

async def jsonParseMiddleware(app, handler):
    async def jsonMiddlewareHandler(request):
        if request.method == "POST":
            try:
                body = None
                if request.has_body:
                    # get json data from post requests and pass it on to handler
                    body = await request.json()
                response = await handler(request, body)
                return response
            except ValidationError as ex:
                error = dumps({"error": ex.message})
                raise HTTPBadRequest(text=error,
                                     content_type="application/json")

        response = await handler(request)
        return response

    return jsonMiddlewareHandler
