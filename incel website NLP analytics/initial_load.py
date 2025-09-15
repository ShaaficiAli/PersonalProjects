import asyncio
import requests
import re
import httpx
from bs4 import BeautifulSoup
async def get_all_posts_urls():
    pass



def add_to_database():
    pass
'''
async def main():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(post) for post in get_all_posts_url()]
        for response_future in asyncio.as_completed(tasks):
            response = await response_future
            
'''

    
async def test():
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        example = await client.get("https://incels.is/threads/no-nut-november-tomorrow.674915/")
        print(await example)
def process_urls(urls):
    pass   
if __name__ =="__main__":
    asyncio.run(test()) 
