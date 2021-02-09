import discord
from leaderboard import Leaderboard

def main():
    intents = discord.Intents().all()

    client = LadderBot(intents)
    client.run("KEY")


class ReactionRequest:
    """Requests to be input by users
    """

    def __init__(self, _message, _users, _need_votes, _func, _args = []):
        self.message = _message
        self.users = _users
        self.need_votes = _need_votes
        self.current_votes = []

        for x in range(len(self.need_votes)):
            self.current_votes.append(0)

        self.func = _func

    async def use_reactions(self, _options):

        self.options = _options

        for x in self.options:
            await self.message.add_reaction(x)

    async def do(self, index):
        await self.func[index](self.message, self.users, self.current_votes, self.need_votes)


class LadderBot(discord.Client):
    """Main worker class of bot project
    """

    def __init__(self, intents):
        """Load command variables
        """

        self.PickLeaderboard = Leaderboard("pick.lb");
        self.RandomLeaderboard = Leaderboard("random.lb");
        self.ReactionRequestList = []
        super().__init__(intents = intents)


    """
    |
    |   Event handling interface
    |
    """

    async def on_ready(self):
        """On bot startup
        """

        print('We are in as ', self.user)


    async def on_reaction_add(self, reaction, user):
        """Discord reaction add override visible to the bot
        """    

        if user == self.user:
            return

        #Check inside the request list for vote addition
        for x in self.ReactionRequestList:

            if reaction.message == x.message:

                #In reactors subgroup
                if user in x.users:

                    #Used vote group emoji
                    if reaction.emoji in x.options:
                        opt = x.options.index(reaction.emoji)

                        print(user, " added vote ", reaction.emoji)
                        x.current_votes[opt] = x.current_votes[opt] + 1

                        if x.current_votes[opt] >= x.need_votes[opt]:
                            await x.do(opt)
                            self.ReactionRequestList.remove(x)


    async def on_reaction_remove(self, reaction, user):
        """Discord reaction remove override visible to the bot
        """    

        if user == self.user:
            return

        #Check inside the request for vote removal
        for x in self.ReactionRequestList:

            if reaction.message == x.message:

                #In reactors subgroup
                if user in x.users:

                    #Used vote group emoji
                    if reaction.emoji in x.options:
                        opt = x.options.index(reaction.emoji)

                        print(user, " removed vote ", reaction.emoji)
                        x.current_votes[opt] = x.current_votes[opt] - 1        


    async def on_message(self, message):
        """Discord messages override visible to the bot
        """    

        if message.author == self.user:
            return

        #Check if message contains command prefix then run the handler
        if message.content[0] == '$':
            coms = message.content.upper()[1:].split(' ')
            await self.handle_command(coms[0], len(coms) - 1, coms[1 : len(coms)], message)


    """
    |
    |   Helper methods
    |
    """
    
    async def get_user(self, string_name):
        """Simplified getter method to retrieve discord.User
        ___

        *string_name* - The string of an @ message to convert
        """
        print(string_name[3: (len(string_name) - 1)])
        return await self.fetch_user( int(string_name[3: (len(string_name) - 1)]) )


    async def handle_command(self, command, argc, argv, source):
        """Command handler to sort arguments and call specific commands
        ___

        *command* - String of the base command
        *argc*    - Argument count
        *argv*    - Argument vector
        *source*  - discord.Message where the command originated from
        """

        #Debug command line options
        print(command, ":", argc, ":", argv)

        if(command == "PICKCHALLENGE"):
            await self.command_challenge(source.channel, source.author, await self.get_user(argv[0]), self.PickLeaderboard)

        if(command == "RANDOMCHALLENGE"):
            await self.command_challenge(source.channel, source.author, await self.get_user(argv[0]), self.RandomLeaderboard)

        if(command == "HELP"):
            await source.channel.send("No help from me you dumbshit")

    """
    |
    |   Challenge commands interfacing
    |
    """
    async def command_challenge(self, channel, duelist1, duelist2, leaderboard):
        """Command for duel requests
        ___

        *channel*   - Channel to output the duel the request
        *duelist1*  - Requester duelist
        *duelist2*  - Requested duelist
        """

        #Error Checking for failed assignments of the duelists user id's
        if(duelist1 == duelist2 or duelist1 == 0 or duelist2 == 0):
            return

        #Check for profile usage
        profiles = [leaderboard.get_profile(duelist1.id), leaderboard.get_profile(duelist2.id)]

        if(profiles[0] == None):
            leaderboard.create_profile(duelist1.name, duelist1.id)

        if(profiles[1] == None):
            leaderboard.create_profile(duelist2.name, duelist2.id)

        if(!leaderboard.within_range(profiles[0], profiles[1])):
            await channel.send("Challenging users are out of range on the ladder board")
            return


        #Send duel messages
        await channel.send("⚔ " + duelist1.mention + " has challenged " + duelist2.mention + " to a duel!")
        msg = await channel.send(duelist1.mention + " and " + duelist2.mention + " must both react to accept the duel.")

        #Create emoji request
        req = ReactionRequest(msg, [duelist1, duelist2], [2, 1], [self.accept_challenge, self.decline_challenge])
        await req.use_reactions(["✔", "❌"])

        #Add to list and wait for response
        self.ReactionRequestList.append( req )

    async def accept_challenge(self, message, users, current_votes, need_votes):
        """Callback function, duel will initiate and request another reaction response for when the duel is over
        """
        await message.channel.send("The challenge was accepted!")
        msg = await message.channel.send("🏳" + users[0].mention + " and 🏴" + users[1].mention + " must agree upon the winner by reacting with the following")

        req = ReactionRequest(msg, users, [2, 2], [self.winner_challenge, self.winner_challenge])

        self.ReactionRequestList.append( req )


    async def decline_challenge(self, message, users, current_votes, need_votes):
        """Callback function, duel will initiate and request another reaction response for when the duel is over
        """       
        await message.channel.send("The challenge was cancelled.")


    async def winner_challenge(self, message, users, current_votes, need_votes):
        """Callback function, called when the winner of the duel is agreed upon
        """
        winner = None

        if(current_votes[0] > current_votes[1]):
            winner = users[0]

        if(current_votes[1] > current_votes[0]):
            winner = users[1]

        message.channel.send("The winner of the duel was " + winner.mention + "!")




if (__name__ == "__main__"):
    main()