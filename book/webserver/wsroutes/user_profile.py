import json
from book.database.users import Users
from passlib.hash import pbkdf2_sha256
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def update_password(socket: WebSocketAsync, *, username, old, new):
    user_details = await Users().get_user(username)
    if len(user_details) > 0:
        if pbkdf2_sha256.verify(old, user_details[0].get('hash')):
            await Users().update_user_pass(username, new)
            return "The password has been updated"
        else:
            return "The old password does not match the password as on the Server."
    else:
        return "There was an error updating this profile. Contact the administrator"


async def list_all_users(socket: WebSocketAsync):
    users = await Users().get_users()
    return json.dumps(users)


async def create_user(socket: WebSocketAsync, *, username, password, group):
    return await Users().create_new_user(username, password, group)


async def edit_user(socket: WebSocketAsync, *, data):
    if data["type"] == "nPassword":
        await Users().update_user_group(data['username'], data['groups'])
        return f"<strong>{data['username']}</strong> has been assigned to <strong>{data['groups']}</strong> group!."
    elif data["type"] == "wPassword":
        await Users().update_user_pass(data['username'], data['password'])
        await Users().update_user_group(data['username'], data['groups'])
        return f"<strong>{data['username']}</strong> has been assigned to <strong>{data['groups']}</strong> " \
               f"group and password for the user is updated!"


async def remove_user(socket: WebSocketAsync, *, username):
    return await Users().remove_user(username)
