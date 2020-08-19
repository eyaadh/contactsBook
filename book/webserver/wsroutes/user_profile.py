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
