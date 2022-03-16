import asyncio
import discord
from discord.ext import commands
from typing import Callable, Coroutine, Any


class MyBot(commands.Bot):
    async def _run_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as error:
            try:
                await self.on_error(event_name, error, *args, **kwargs) #ive passed error, which is the error so now your on_error takes event_name, error, *args and **kwargs
            except asyncio.CancelledError:
                pass