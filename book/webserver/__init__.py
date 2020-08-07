import jinja2
import aiohttp_jinja2
from aiohttp import web
from book.webserver.routes import routes


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('book/webserver/template'))
    web_app['static_root_url'] = '/static'
    web_app.router.add_static("/static", "book/webserver/template/static")

    return web_app
