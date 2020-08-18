import aiohttp_jinja2
from aiohttp import web
from aiohttp_auth import auth
from book.database.users import Users
from passlib.hash import pbkdf2_sha256

routes = web.RouteTableDef()


@routes.get("/")
@auth.auth_required
@aiohttp_jinja2.template('index.html')
async def root_route_handler(request):
    username = await auth.get_auth(request)
    user_query = await Users().get_user(username)
    group = user_query[0].get('groups')
    print(group)
    context = {'user': username, 'groups': group}
    return context


@routes.get("/login")
@aiohttp_jinja2.template('login.html')
async def login_get_handler(request):
    context = {}
    return context


@routes.post("/login")
@aiohttp_jinja2.template('login.html')
async def login_post_handler(request):
    posted_data = await request.post()
    username = posted_data.get('inputUsername')
    password = posted_data.get('inputPassword')

    user_query = await Users().get_user(username)
    if len(user_query) > 0:
        if user_query[0].get('user_id') == username:
            if pbkdf2_sha256.verify(password, user_query[0].get('hash')):
                await auth.remember(request, username)
                raise web.HTTPFound('/')
            else:
                raise web.HTTPUnauthorized()
        else:
            raise web.HTTPUnauthorized()


@routes.get('/logout')
async def logout_handler(request):
    await auth.forget(request)
    raise web.HTTPFound('/login')
