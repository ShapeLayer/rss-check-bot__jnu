import requests
import xmltodict
from json import dumps, loads
import discord
from datetime import datetime, timezone, timedelta
import argparse
from os import getenv

parser = argparse.ArgumentParser(description='JNU notice observer')
parser.add_argument('--channel', type=str, default=None, action='append', help='Specific channel to observe. (str)')
parser.add_argument('--nlimit', type=int, default=0, help='Limit datetime to get notice. (int)')
args = parser.parse_args()

CONFIG = loads(open('config.json', encoding='utf-8').read())
client = discord.Client()

def get_rss(target, row = CONFIG['get_notice_limit'], mode='n') -> dict:
    res = requests.get(CONFIG['targets'][target]['rss'].format(row), headers = {'User-Agent': 'Mozilla/5.0'})
    if not res.status_code == 200:
        return
    tree = xmltodict.parse(res.text)
    if mode == 'w':
        with open('{}.json'.format(target), 'w', encoding='utf-8') as f:
            f.write(dumps(tree, indent=2, ensure_ascii=False))
    return tree

def check_update(target: str, limit = CONFIG['get_notice_limit']) -> list:
    now = datetime.now(timezone(timedelta(hours=9)))
    dict_ = get_rss(target, limit)
    if not dict_:
        return
    items = dict_['rss']['channel']['item']
    content = []
    for i in range(min(len(items), limit)): # 하위호환성 대응: 나중에 `legacy` 타입 RSS 들어와야하면 대응수정
        pub_date = datetime.strptime(items[i]['pubDate'], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone(timedelta(hours=9)))
        if (now-pub_date).days <= args.nlimit:
            content += [items[i]]
    return content

async def send_update(boardcode, channelid):
    updates = check_update(boardcode)
    for update in updates:
        embed = discord.Embed(
            title = update['title'],
            type = 'rich',
            description = update['description'],
            url = update['link'] if not CONFIG['targets'][boardcode]['refactor'] else CONFIG['targets'][boardcode]['host'] + update['link']
        )
        await client.get_channel(channelid).send(embed=embed)

@client.event
async def on_ready():
    for board in args.channel if args.channel else CONFIG['targets'].keys():
        await send_update(board, CONFIG['targets'][board]['discord'])
    await client.close()

if __name__ == '__main__':
    client.run(CONFIG['KEY'] if CONFIG['KEY'] else getenv('discord_key'))