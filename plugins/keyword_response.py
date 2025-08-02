
from .base_plugin import BasePlugin

class KeywordResponsePlugin(BasePlugin):
    def setup(self):
        import os
        import random
        import re
        from datetime import date

        self.botstr = "MarcusBot"
        self.namestr = "marcus"
        self.responses = self.load_responses(os.path.join('txt', 'keyword_response.txt'))
        self.name_lines = self.load_lines(os.path.join('txt', 'name.txt'))
        self.botmention_lines = self.load_lines(os.path.join('txt', 'botmention.txt'))
        self.swotd = self.load_wotd()

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            content = message.content.lower()

            if self.botstr.lower() in content:
                await message.channel.send(self.random_response(self.botmention_lines))
                return

            for keyword, response in self.responses.items():
                if keyword in content:
                    await message.channel.send(response)
                    return

            if self.namestr.lower() in content:
                await message.channel.send(self.random_response(self.name_lines))
                return

            if self.swotd.lower() in content:
                await self.react_to_wotd(message)

            if re.match("nice", content):
                await self.react_to_nice(message)

            await self.bot.process_commands(message)

    def load_responses(self, filepath):
        responses = {}
        with open(filepath, 'r') as f:
            for line in f:
                if "::" in line:
                    keyword, response = line.strip().split("::", 1)
                    responses[keyword.strip()] = response.strip()
        return responses

    def load_lines(self, filepath):
        with open(filepath, 'r') as f:
            return f.read().splitlines()

    def random_response(self, lines):
        import random
        return random.choice(lines)

    def load_wotd(self):
        import os
        from datetime import date
        import random
        path = os.path.join('txt', 'words.txt')
        with open(path, 'r') as f:
            lines = f.readlines()
        seed = date.today().isoformat().replace('-', '')
        random.seed(seed)
        word = lines[random.randrange(len(lines))].strip()
        random.seed()
        return word

    async def react_to_wotd(self, message):
        for emoji in ["👌", "😂", "🔥", "😱"]:
            await message.add_reaction(emoji)

    async def react_to_nice(self, message):
        await message.add_reaction("<:69:844757057437302856>")
