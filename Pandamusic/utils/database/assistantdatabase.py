from Pandamusic.core.userbot import assistants


async def get_assistant(client_id: int):
    for client in assistants:
        if client_id == (await client.get_me()).id:
            return client
    return None


async def get_assistant_by_username(username: str):
    username = (username or "").lstrip("@").lower()
    for client in assistants:
        me = await client.get_me()
        if (me.username or "").lower() == username:
            return client
    return None


async def list_assistants():
    data = []
    for client in assistants:
        me = await client.get_me()
        data.append(
            {
                "id": me.id,
                "username": me.username,
                "name": f"{me.first_name or ''} {me.last_name or ''}".strip(),
            }
        )
    return data
