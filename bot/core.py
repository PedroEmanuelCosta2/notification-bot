"""Bot de notifications."""

import asyncio
import json
import zlib
import shlex
import time
import param

import aiohttp

from datetime import datetime
from main import new, store, load, update, listTask, detail, helpTask, delete, user_dict

TOKEN = param.TOKEN

URL = "https://discordapp.com/api"
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
}

listeRappel = []
load()

async def api_call(path, method="GET", **kwargs):
     """Effectue une  requête sur l'API REST de Discord."""
     default = {"headers": HEADERS}
     kwargs = dict(default, **kwargs)
     with aiohttp.ClientSession() as session:
         async with session.request(method, f"{URL}{path}", **kwargs) as response:
             if 200 == response.status:
                 return await response.json()
             elif 204 == response.status:
                 return {}
             else:
                 body = await response.text()
                 raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")

async def send_message(recipient_id, content):
     """Envoie un message à l'utilisateur donné."""
     channel = await api_call("/users/@me/channels", "POST", json={"recipient_id": recipient_id})
     return await api_call(f"/channels/{channel['id']}/messages", "POST", json={"content": content})

# Pas très joli, mais ça le fait.
last_sequence = None

async def heartbeat(ws, interval):
    """Tâche qui informe Discord de notre présence."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await ws.send_json({'op': 1,  # Heartbeat
                            'd': last_sequence})


async def identify(ws):
    """Tâche qui identifie le bot à la Web Socket (indispensable)."""
    await ws.send_json({'op': 2,  # Identify
                        'd': {'token': TOKEN,
                              'properties': {},
                              'compress': True,  # implique le bout de code lié à zlib, pas nécessaire.
                              'large_threshold': 250}})

async def start(ws):
    """Lance le bot sur l'adresse Web Socket donnée."""
    global last_sequence  # global est nécessaire pour modifier la variable
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{ws}?v=5&encoding=json") as ws:
            async for msg in ws:
                if msg.tp == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.tp == aiohttp.WSMsgType.BINARY:
                    data = json.loads(zlib.decompress(msg.data))
                else:
                    print("?", msg.tp)

                # https://discordapp.com/developers/docs/topics/gateway#gateway-op-codes
                if data['op'] == 10:  # Hello
                    asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval']))
                    await identify(ws)
                elif data['op'] == 11:  # Heartbeat ACK
                    print("< Heartbeat ACK")
                elif data['op'] == 0:  # Dispatch
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE":

                        print(data['d'])

                        if data['d']['content'] == '?help':
                            helpMsg = helpTask()
                            await send_message(data['d']['author']['id'],helpMsg)

                        if '?new' in data['d']['content']:
                            arguments = shlex.split(data['d']['content'])

                            if len(arguments) != 4:
                                await send_message(data['d']['author']['id'],'Veuillez entrez un titre, une description et une date')
                            else:
                                newMsg = new(data['d']['author']['id'], arguments[1], arguments[2], arguments[3])
                                await send_message(data['d']['author']['id'],newMsg)
                                task = rappel(data['d']['author']['id'], arguments[1],arguments[3])
                                await task
                                listeRappel.append(task)

                        if '?update' in data['d']['content']:
                            arguments = shlex.split(data['d']['content'])

                            if len(arguments) != 4:
                                await send_message(data['d']['author']['id'],f"Veuillez entrez l'id de votre tâche, le champ que vous souhaitez changer et la nouvelle valeur.")
                                await send_message(data['d']['author']['id'],f"Exemple : update 0 name NewName")
                            else:
                                updateMsg = update(data['d']['author']['id'], arguments[1], arguments[2], arguments[3])
                                await send_message(data['d']['author']['id'],updateMsg)

                        if '?delete' in data['d']['content']:
                            arguments = shlex.split(data['d']['content'])
                            deleteMsg = delete(data['d']['author']['id'], arguments[1])
                            await send_message(data['d']['author']['id'],deleteMsg)
                            #listeRappel[int(arguments[1])].cancel()

                        if '?list' in data['d']['content']:
                            tacheList=listTask(data['d']['author']['id'])
                            await send_message(data['d']['author']['id'],tacheList)

                        if '?detail' in data['d']['content']:
                            arguments = shlex.split(data['d']['content'])
                            details = detail(data['d']['author']['id'], arguments[1])
                            await send_message(data['d']['author']['id'],details)

                        if data['d']['content'] == '?quit':
                            store()
                            await send_message(data['d']['author']['id'],'Bye Bye !')
                            break

                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)

async def loadTask():
    for id_o in user_dict:
        for tache in user_dict[id_o]:
            task = rappel(tache.owner, tache.name, tache.time)
            await task
            listeRappel.append(task)

def callback(owner, name, date):
    asyncio.ensure_future(send_message(owner,f"RAPPEL ! Il est temps ({date}) de faire votre tâche : {name}"))

async def rappel(owner, name, date):
    nowLoop = loop.time()
    nowTime = time.time()

    try:
      dateTask = datetime.strptime(date,"%d/%m/%Y %H:%M")
    except:
      print("Error converting time into timestamp")

    delta = dateTask.timestamp() - nowTime

    loop.call_at( nowLoop+delta, callback, owner, name, date)

async def main():
    response = await api_call('/gateway')
    await loadTask()
    await start(response['url'])

# Lancer le programme.
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()
