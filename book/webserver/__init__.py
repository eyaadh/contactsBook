import jinja2
import aiohttp_jinja2
import aiohttp_session
from os import urandom
from aiohttp import web
from aiohttp_auth import auth
from book.webserver.routes import routes
import book.webserver.wsroutes as ws_routes
from wsrpc_aiohttp import STATIC_DIR, WebSocketAsync
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 401:
                raise web.HTTPFound('/login')
            return response
        except web.HTTPException as ex:
            if ex.status == 401:
                raise web.HTTPFound('/login')
            raise

    return middleware_handler


async def web_server():
    web_app = web.Application(client_max_size=30000000, middlewares=[error_middleware])

    storage = EncryptedCookieStorage(urandom(32))
    aiohttp_session.setup(web_app, storage)
    policy = auth.SessionTktAuthentication(urandom(32), 86400000,
                                           include_ip=True)
    auth.setup(web_app, policy)

    web_app.add_routes(routes)
    aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('book/webserver/template'))
    web_app['static_root_url'] = '/static'
    web_app.router.add_static("/static", "book/webserver/template/static")

    web_app.router.add_route("*", "/ws/", WebSocketAsync)
    web_app.router.add_static("/js", STATIC_DIR)
    web_app.router.add_static("/", ".")

    WebSocketAsync.add_route("list_people", ws_routes.list_people.list_people)
    WebSocketAsync.add_route("get_people", ws_routes.get_people.get_people)
    WebSocketAsync.add_route("delete_people", ws_routes.delete_people.delete_people)
    WebSocketAsync.add_route("create_people", ws_routes.create_people.create_people)
    WebSocketAsync.add_route("update_people", ws_routes.update_people.update_people)

    return web_app
