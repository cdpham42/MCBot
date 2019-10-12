# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:14:26 2019

@author: cdpha
"""

import os
import discord
import asyncio
from mcstatus import MinecraftServer
from dotenv import load_dotenv
from datetime import datetime

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == "__main__":
    
    load_dotenv()
    
    s = '{}"'
    token = os.getenv("DISCORD_TOKEN").replace('{','').replace('}','').replace('\"','')
    server_ip = os.getenv("SERVER_IP").replace('{','').replace('}','').replace('\"','')
    server_port = os.getenv("SERVER_PORT").replace('{','').replace('}','').replace('\"','')
    
    client = discord.Client()

    @client.event
    async def on_ready():
        print("{client.user} has connected to Discord!")
        print("Connecting to " + server_ip + ":" + server_port)
        
    @client.event
    async def update():
        while True:
            await client.wait_until_ready()
            try:
                server = MinecraftServer.lookup(server_ip + ":" + server_port)
                status = server.status()
                desc = status.description['text']
                
                # Check list of known servers
                with open("servers.txt") as f:
                    for line in f:
                        line = line.strip()
                        if line in desc:
                            name = line
                
                name = name + ": {0}".format(status.players.online)
    
                activity = discord.Game(name=name)
                await client.change_presence(status = discord.Status.online,
                                             activity = activity)

                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("Players Online: {0}".format(status.players.online))
                print("Server Ping: {0}\n".format(status.latency))

            except:
                activity = discord.Game(name="Server Offline")
                await client.change_presence(status = discord.Status.dnd,
                                             activity = activity)
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print("Cannot connect to server\n")

            await asyncio.sleep(5)

    client.loop.create_task(update())
    client.run(token)
