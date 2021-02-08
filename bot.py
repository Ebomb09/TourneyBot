import discord
from leaderboard import Leaderboard

def main():
    intents = discord.Intents().all()

    client = LadderBot(intents)
    client.run("ODA3NzkzNDM0MTAxMjg0ODY1.YB9KQg.kp5aJC9iaHET9Tf7CvilUArZCpc")


class ReactionRequest:
    """Requests to be input by users
    """

    def __init__(self, _message, _users, _need_votes, _func):
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

        #self.PickLB = Leaderboard("pick.lb");
        #self.RandomLB = Leaderboard("random.lb");
        self.ReactionRequestList = []
        super().__init__(intents = intents)


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

        if(command == "CHALLENGE"):
            await self.command_challenge(source.channel, source.author, await self.get_user(argv[0]))

        if(command == "HELP"):
            await source.channel.send("No help from me you dumbshit")


    async def command_challenge(self, channel, duelist1, duelist2):
        """Command for duel requests
        ___

        *channel*   - Channel to output the duel the request
        *duelist1*  - Requester duelist
        *duelist2*  - Requested duelist
        """

        #Error Checking for failed assignments of the duelists user id's
        if(duelist1 == duelist2 or duelist1 == 0 or duelist2 == 0):
            return

        #Send duel messages
        await channel.send(duelist1.mention + " has challenged " + duelist2.mention + " to a duel!")
        msg = await channel.send(duelist1.mention + " and " + duelist2.mention + " must both react to accept the duel.")

        #Create emoji request
        req = ReactionRequest(msg, [duelist1, duelist2], [2, 1], [self.accept_challenge, self. decline_challenge])
        await req.use_reactions(["✔", "❌"])

        #Add to list and wait for response
        self.ReactionRequestList.append( req )

    async def accept_challenge(self, message, users, current_votes, need_votes):
        """Duel will initiate and request another reaction response for when the duel is over
        """
        await message.channel.send("The challenge was accepted")

    async def decline_challenge(self, message, users, current_votes, need_votes):
        """Duel will initiate and request another reaction response for when the duel is over
        """       
        await message.channel.send("The challenge was cancelled")


if (__name__ == "__main__"):
    main()