# -*- coding: utf-8 -*-

import logging
from os import environ
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Gotify import Gotify
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import StreamerSettings

envVariables = [
    "TWITCH_USERNAME",
    "TWITCH_PASSWORD",
    "DISCORD_WEBHOOK_URL",
    "GOTIFY_URL",
    "STREAMER_LIST"
]

for envVar in envVariables:
    if envVar not in environ:
        raise Exception(f"Environment variable {envVar} not found")

twitch_miner = TwitchChannelPointsMiner(
    username=environ.get("TWITCH_USERNAME", "none"),
    password=environ.get("TWITCH_PASSWORD", "none"),
    claim_drops_startup=True,
    priority=[
        Priority.STREAK,
        Priority.DROPS,
        Priority.ORDER
    ],
    enable_analytics=True,
    disable_ssl_cert_verification=False,
    disable_at_in_nickname=False,
    logger_settings=LoggerSettings(
        save=True,
        console_level=logging.INFO,
        console_username=False,
        auto_clear=True,
        time_zone="",
        file_level=logging.DEBUG,
        emoji=True,
        less=False,
        colored=True,
        color_palette=ColorPalette(
            STREAMER_online="GREEN",
            streamer_offline="red",
            BET_wiN=Fore.MAGENTA
        ),
        discord=Discord(
            webhook_api=environ.get("DISCORD_WEBHOOK_URL", "none"),
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION],
        ),
        gotify=Gotify(
            endpoint=environ.get("GOTIFY_URL", "none"),
            priority=8,
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE, Events.CHAT_MENTION], 
        )
    ),
    streamer_settings=StreamerSettings(
        make_predictions=False,
        follow_raid=True,
        claim_drops=True,
        claim_moments=True,
        watch_streak=True,

        community_goals=False,
        chat=ChatPresence.ONLINE,
        bet=BetSettings(
            strategy=Strategy.SMART,
            percentage=5,
            percentage_gap=20,
            max_points=50000,
            stealth_mode=True,
            delay_mode=DelayMode.FROM_END,
            delay=6,
            minimum_points=20000,
            filter_condition=FilterCondition(
                by=OutcomeKeys.TOTAL_USERS,
                where=Condition.LTE,
                value=800
            )
        )
    )
)

streamers = environ.get("STREAMER_LIST", "").split(",")

twitch_miner.analytics(host="0.0.0.0", port=5000, refresh=5, days_ago=7)   # Start the Analytics web-server

twitch_miner.mine(streamers,
    followers=False,
    followers_order=FollowersOrder.ASC
)
