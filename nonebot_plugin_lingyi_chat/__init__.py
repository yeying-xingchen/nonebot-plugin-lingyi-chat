import aiohttp
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
import json
from .config import Config
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command

__plugin_meta__ = PluginMetadata(
    name="lingyi_chat",
    description="灵翼系列插件-聊天",
    usage="基于部署在CFWorkers的LLM API在Nonebot2上提供聊天服务。",
    type="application",
    homepage="https://github.com/yeying-xingchen/nonebot-plugin-lingyi-chat",
    config=Config,
    supported_adapters=None,
)

config = get_plugin_config(Config)

async def chat(content):
    async with aiohttp.ClientSession() as session:
        async with session.post(config.api_url, json={'content': content}) as resp:
            resp_json = await resp.json()
            return await resp_json["response"]["response"]

chat_command = on_command("chat", aliases={"聊天"}, priority=10, block=True)

@chat_command.handle()
async def command_handler(args: Message = CommandArg()):
    if content := args.extract_plain_text():
        response_data = await chat(content)
        await chat_command.finish(str(response_data))
    else:
        await chat_command.finish("请输入聊天内容。")