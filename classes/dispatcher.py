import asyncio


class Dispatcher:
    def __init__(self, event_manager, bot, db, parser):
        self.event_manager = event_manager
        self.bot = bot
        self.db = db
        self.parser = parser

        self.bot_task = None
        self.parser_task = None

        # DB operations
        self.event_manager.subscribe('insert_user', self.db.insert_user)
        self.event_manager.subscribe('insert_message', self.db.insert_message)
        self.event_manager.subscribe('fetch_user', self.db.fetch_users)
        self.event_manager.subscribe('fetch_users', self.db.fetch_users)
        self.event_manager.subscribe('fetch_target_words', self.db.fetch_target_words)
        self.event_manager.subscribe('update_target_words', self.db.update_user)
        self.event_manager.subscribe('delete_user', self.db.delete_user)

        # Bot operations
        self.event_manager.subscribe('notify_user', self.bot.bot.send_message)

        # Parser operations
        self.event_manager.subscribe('start_parser', self.parser.start_parser)
        self.event_manager.subscribe('pause_parser', self.parser.pause_parser)

    async def start(self):
        self.bot_task = asyncio.create_task(self.bot.start())
        self.parser_task = asyncio.create_task(self.parser.start())
        await asyncio.gather(self.bot_task, self.parser_task)

    def _bot_task(self):
        self.bot_task = asyncio.create_task(self.bot.start())

    def _parser_task(self):
        self.parser_task = asyncio.create_task(self.parser.start())

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
