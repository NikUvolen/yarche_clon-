import asyncio
from telethon import TelegramClient, events
from tools.funcs import split_string, find_suitable_vacancy
from config import (API_ID, API_HASH, SESSION_STRING, BOT_ID)


client = TelegramClient(SESSION_STRING, API_ID, API_HASH)
user_id = 0
is_running = False
gathering_requests = False
requests = ''


async def answer():
    global gathering_requests, requests

    while is_running:
        await client.send_message(BOT_ID, 'Все заявки')
        gathering_requests = True
        await asyncio.sleep(20)

        result = split_string(requests)
        result = find_suitable_vacancy(result)
        gathering_requests = False

        if result:
            await client.send_message(BOT_ID, f'/{result}')

        requests = ''

        await asyncio.sleep(10)


async def all_orders():
    await client.send_message(BOT_ID, 'привет')


@client.on(events.NewMessage(chats=(BOT_ID,), func=lambda is_run: is_running))
async def main(event):
    global requests

    if event.message.peer_id.user_id != user_id:
        if gathering_requests:
            requests += event.message.message
        elif event.message.message.split('\n')[0] == 'Заявка:':
            await client.send_message(BOT_ID, 'Забрать себе')
        elif event.message.message == 'Укажите комментарий:':
            await client.send_message(BOT_ID, 'Пропустить')
            await asyncio.sleep(1.5)
            await client.send_message(BOT_ID, 'Назад')


@client.on(events.NewMessage(chats=('me',)))
async def start(event):
    global is_running, user_id

    if event.message.message.lower() == 'on':
        user_id = event.message.peer_id.user_id

        is_running = True
        await event.reply('Бот запущен')
        await asyncio.create_task(answer())
        asyncio.get_running_loop().run_forever()
    elif event.message.message.lower() == 'off':
        await event.reply('Бот выключен')
        is_running = False

        try:
            asyncio.get_running_loop().close()
        except RuntimeError:
            pass


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
