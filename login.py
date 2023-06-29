import time
from datetime import datetime, timedelta

import discord

from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:
    username = ""
    password = ""

    async def get_username(self, ctx: discord.ext.commands.Context):
        async for message in ctx.channel.history(limit=100, after=datetime.now() - timedelta(minutes=2000)):
            if message.content.startswith("identifiants:"):
                self.username = message.content.split("||")[1].split()[0]
                self.password = message.content.split("||")[1].split()[1]

    def login(self, driver):
        driver.get("https://myges.fr/login")
        time.sleep(2)
        identifier_box = driver.find_element(By.ID, "username")
        identifier_box.send_keys(self.username)
        password_box = driver.find_element(By.ID, "password")
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)
        time.sleep(2)

    def is_empty(self):
        return self.username == "" or self.password == ""
