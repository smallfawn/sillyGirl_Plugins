r"""
/**
 * @title 魔幻手机语录
 * @author sillyGirl
 * @version v1.0.1
 * @desc 随机回复傻妞和陆小千相关短句
 * @rule raw ^\s*(傻妞语录|傻妞台词|陆小千语录|小千语录|小千台词|魔幻手机语录|魔幻手机台词)\s*$
 * @admin false
 * @priority 10
 * @public true
 * @class 娱乐
 * @depe []
 */
"""

import asyncio
import random
from sillygirl import sender as s


QUOTES = [
    {
        "role": "傻妞",
        "text": "华人牌2060款手机傻妞为您服务。",
    },
    {
        "role": "傻妞",
        "text": "请输入开机密码。",
    },
    {
        "role": "傻妞",
        "text": "密码正确，进入功能选择。",
    },
    {
        "role": "傻妞",
        "text": "小千哥哥，傻妞会一直帮你。",
    },
    {
        "role": "傻妞",
        "text": "傻妞明白。",
    },
    {
        "role": "陆小千",
        "text": "我老千啊我？",
    },
    {
        "role": "陆小千",
        "text": "傻妞，帮我一下。",
    },
    {
        "role": "陆小千",
        "text": "这事儿不能这么办。",
    },
    {
        "role": "陆小千",
        "text": "别闹了，先救人。",
    },
    {
        "role": "游所为",
        "text": "给他来一贵的。",
    },
    {
        "role": "黄眉大王",
        "text": "你脑袋让门挤了吧。",
    },
]


def quote_pool(command):
    if "陆小千" in command or "小千" in command:
        return [item for item in QUOTES if item["role"] == "陆小千"]
    if "傻妞" in command:
        return [item for item in QUOTES if item["role"] == "傻妞"]
    return QUOTES


async def main():
    command = (await s.getContent()).strip()
    pool = quote_pool(command)
    item = random.choice(pool or QUOTES)
    await s.reply(f"{item['role']}：{item['text']}")


asyncio.run(main())
