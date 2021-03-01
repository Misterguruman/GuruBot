# bot.py
import os
import random

from bs4 import BeautifulSoup
import requests
import difflib

from discord.ext import commands
from dotenv import load_dotenv

def create_url(query):
    base_url = "https://escapefromtarkov.gamepedia.com/Special:Search?search="
    url_prefix = "&go=Go"

    return(base_url + query.replace(" ", "+") + url_prefix)

def search_wiki(input):
    print("Search triggered for %s" % input)
    url = create_url(input)
    page = requests.get(url)

    #Log if the site throws an error
    if (page.status_code != 200):
        return("Your search returned with an error. Try again, if it fails again this may be on our side. I'm going to leave a note for the devs, we'll see what we can do to fix it")
    
    #If a user types in an item/quest in perfectly. The site will redirect to the page of the item. No need to go through results.
    elif (page.url != url):
        return(page.url)

    #Get list of search results
    soup = BeautifulSoup(page.text, 'html.parser')  
    results = soup.find_all("a", class_="unified-search__result__title")

    #Generate a dictionary of titles and links in results
    r = [ x.text.strip() for x in results ]
    l = [ x['href'] for x in results ]

    match = difflib.get_close_matches(input, r)

    if match:
        for i, result in enumerate(results):
            if result.text.strip() == match[0]:
                return(result['href'])

    else:
        try:
            return(results[0]['href'])
        except IndexError:
            return("No matching results. Try a better Keyword")

if __name__ == '__main__':

    # Change only the no_category default string
    help_command = commands.DefaultHelpCommand(
        no_category = 'Commands'
    )

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.command(name="tarkovwiki", help="Searches the tarkov wiki and provides the top result")
    async def tarkov_wiki(ctx, query: str):
        await ctx.send(search_wiki(query))


    bot.run(TOKEN)