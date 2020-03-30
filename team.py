import dictionary
import random

class Team(object):
    def __init__(self, players=[], meme_bool=False):
        self.players = players
        self.pi = 0

        self.remaining = []
        for i in range(1,5):
            for j in range(1,5):
                for k in range(1,5):
                    if i != j and j != k and i != k:
                        self.remaining.append("%d%d%d" % (i,j,k))
        random.shuffle(self.remaining)

        self.draws = []

        self.words = []
        while len(self.words) < 4:
            w = dictionary.get_word(meme_bool)
            w = self.randomplayerify(w)
            if w not in self.words:
                self.words.append(w)

    def randomplayerify(self, word):
        if "<RANDOM_PLAYER_NAME>" in word:
            if len(self.players) < 1:
                return word.replace("<RANDOM_PLAYER_NAME>", self.get_random_fake_name())
            return word.replace("<RANDOM_PLAYER_NAME>", self.get_random_player_name())
        return word

    def add_player(self, player):
        self.players.append(player)

    def get_random_fake_name(self):
        s = random.choice(["Aarav", "John", "Ciaran", "Chase", "Brad", "Bryce", "Zach", "Mercer", "Adam", "Jordan", "Josh", "Ryan", "Parker", "Caleb"])
        return s

    def get_random_player_name(self):
        s = str(random.choice(self.players))
        return s.split("#")[0]

    def get_player_list(self):
        return ", ".join(str(p) for p in self.players)

    def get_words(self):
        ret = ""
        for i in range(4):
            ret += "%d - %s\n" % (i+1, self.words[i])
        return ret.strip()

    async def send_draw(self):
        draw = self.remaining.pop()
        player = self.players[self.pi]
        self.pi += 1
        self.pi %= len(self.players)
        s = "Player %s drew %s" % (str(player), draw)
        self.draws.append(s)
        await player.dm_channel.send("Your draw is %s" % draw)
        return "Player %s drew a card" % str(player)

    async def reveal_draw(self, context):
        if len(self.draws) < 1:
            await context.send("No draws yet")
        else:
            await context.send(self.draws[-1])

    async def send_welcome_messages(self):
        for p in self.players:
            await p.dm_channel.send("Hi! Welcome to decrypto.\n\nYou're playing on a team with members [%s].\n\nYour words are the following:\n%s" % (self.get_player_list(), self.get_words()))
