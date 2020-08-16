import jinja2
import aiohttp_jinja2
import book.webserver.wsroutes as ws_routes
from aiohttp import web
from book.webserver.routes import routes
from wsrpc_aiohttp import STATIC_DIR, WebSocketAsync


async def web_server():
    web_app = web.Application(client_max_size=30000000)
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

    return web_app
