import sqlite3
import aiosqlite
import yaml

class sync_handle_prefixes:
    def __init__(self, full_path) -> None:
        self.path = full_path
        with open("config.yml", "r") as file:
            configs = yaml.load(file, Loader=yaml.SafeLoader)
        self.base_prefix = configs["moderation"]["basePrefix"]

    def __enter__(self) -> None:
        self.db = sqlite3.connect(self.path)
        return self

    def __exit__(self, type, value, traceback) -> bool:
        self.db.commit()
        self.db.close()
        if traceback is not None:
            print(f"{type}, {value}, {traceback}")
        else:
            return True

    def get_value(self, table, guild_id):
        query = f"SELECT prefix FROM {table} WHERE guildID = ?"
        val = (guild_id,)
        cursor = self.db.execute(query, val)
        prefix=cursor.fetchone()
        if prefix is not None:
            return prefix[0]
        elif prefix is None:
            self.set_value("prefixes", guild_id)
            return self.base_prefix

    def set_value(self, table, guild_id):
        query = f"INSERT INTO {table}(guildID, prefix) VALUES(?, ?)"
        val = (guild_id, self.base_prefix)
        self.db.execute(query, val)

class DB:
    def __init__(self, full_path) -> None:
        self.path = full_path
        with open("config.yml", "r") as file:
            configs = yaml.load(file, Loader=yaml.SafeLoader)
        self.base_prefix = configs["moderation"]["basePrefix"]

    async def __aenter__(self) -> None:
        self.db = await aiosqlite.connect(self.path)
        return self

    async def __aexit__(self, type, value, traceback) -> bool:
        await self.db.commit()
        await self.db.close()
        if traceback is not None:
            print(f"{type}, {value}, {traceback}")
        else:
            return True

    async def update_value(self, table, scoreboard):
        if not scoreboard:
            return
        query = f"SELECT userID, score FROM {table}"
        async with self.db.execute(query) as cursor:
            latest_scoreboard = await cursor.fetchall() #((userID, score), (userID, score))
        for user_id in scoreboard.keys():
            if user_id in [record[0] for record in latest_scoreboard]:
                query = f"UPDATE {table} SET score = score + {scoreboard[user_id]} WHERE userID = {user_id}"
                await self.db.execute(query)
            else:
                query = f"INSERT INTO {table}(userID, score) VALUES(?, ?)"
                val = (user_id, scoreboard[user_id])
                await self.db.execute(query, val)

    async def delete_value(self, table, param):
        userID = [*dict][0]
        query = f"DELETE FROM {table} WHERE userID = ?"
        await self.db.execute(query, param)

    async def get_value(self, table):
        query = f"SELECT userID, score FROM {table}"
        async with self.db.execute(query) as cursor:
            return await cursor.fetchall()
    
class PrefixHandler:
    def __init__(self, full_path) -> None:
        self.path = full_path
        with open("config.yml", "r") as file:
            configs = yaml.load(file, Loader=yaml.SafeLoader)
        self.base_prefix = configs["moderation"]["basePrefix"]

    async def __aenter__(self) -> None:
        self.db = await aiosqlite.connect(self.path)
        return self

    async def __aexit__(self, type, value, traceback) -> bool:
        await self.db.commit()
        await self.db.close()
        if traceback is not None:
            print(f"{type}, {value}, {traceback}")
        else:
            return True

    async def update_value(self, table, dict):
        query = f"SELECT prefix FROM {table} WHERE guildID = ?"
        guild_id = (*dict,)
        async with self.db.execute(query, guild_id) as cursor:
            value = await cursor.fetchone()
            if value is not None:
                await self.delete_value(table, guild_id[0])
        query = f"INSERT INTO {table}(guildID, prefix) VALUES(?, ?)"    ## MIGHT BE GOOD IF THERE IS A BETTER WAY TO STORE IN CHUNKS
        new_values = (guild_id[0], dict[guild_id[0]])
        await self.db.execute(query, new_values)

    async def delete_value(self, table, guild_id):
        query = f"DELETE FROM {table} WHERE guildID = ?"
        await self.db.execute(query, (guild_id,))

    async def get_value(self, table, guildID):
        query = f"SELECT prefix FROM {table} WHERE guildID = ?"
        val = (guildID,)
        async with self.db.execute(query, val) as cursor:
            prefix = await cursor.fetchone()
            if prefix is None:
                await self.update_value(table, {guildID : self.base_prefix})
                return self.base_prefix
            elif prefix is not None:
                return prefix[0]