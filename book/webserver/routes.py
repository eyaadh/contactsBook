import os
import csv
import aiohttp_jinja2
from aiohttp import web
from aiohttp_auth import auth
from book.database.users import Users
from passlib.hash import pbkdf2_sha256
from book.google.people import GPeople

routes = web.RouteTableDef()


@routes.get("/")
@auth.auth_required
@aiohttp_jinja2.template('index.html')
async def root_route_handler(request):
    username = await auth.get_auth(request)
    user_query = await Users().get_user(username)
    group = user_query[0].get('groups')
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


@routes.post('/import_contacts')
@auth.auth_required
async def import_contacts_handler(request):
    posted_data = await request.post()
    contacts_file = posted_data.get("customFile")

    if contacts_file != b"":
        tmp_file = f"book/working_dir/{contacts_file.filename}"

        with open(tmp_file, "wb") as f:
            f.write(contacts_file.file.read())

        with open(tmp_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                names = [{'givenName': row[0], 'familyName': row[1]}]
                phone_numbers = [{'value': row[2], 'type': 'work'},
                                 {'value': row[3], 'type': 'pager'},
                                 {'value': row[4], 'type': 'mobile'}, {'value': row[5], 'type': 'extension'}]
                emails = [{'value': row[6], 'type': 'work'}, {'value': row[7], 'type': 'other'}]
                organizations = [{'name': 'VAKKARU MALDIVES', 'title': row[8]}]
                contact_dict = {
                    'names': names,
                    'phoneNumbers': phone_numbers,
                    'emailAddresses': emails,
                    'organizations': organizations
                }

                await GPeople().create_contacts(contact_dict)


        try:
            os.remove(f"book/working_dir/{contacts_file.filename}")
        except:
            pass

    raise web.HTTPFound('/')
