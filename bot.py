import discord
intents = discord.Intents.default()
intents.members = True


TOKEN = "NzM5OTk0MTY5NTE4NTg4MDY1.XyijRg.1K8xP0B2U_gjgsKYu7KaRcaKLi0"

client = discord.Client(intents = intents)

rule_confirm_channel = None
announcement_channel = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    print("A new member has joined the server: " + member.name + ", their ID is " + str(member.id))
    await member.create_dm()
    await member.dm_channel.send("Hello, " + member.mention + "! Welcome to the Free Web Project! Remember to read the rules; you cannot use the server until you have confirmed that you agree to them. This protects us from raiding and inappropriate members.")
    if rule_confirm_channel != None:
        print("Rule Confirming them")
        await rule_confirm_channel.send("Hello, " + member.mention + ", please thoroughly read the rules, then say `I hereby confirm my acceptance of the rules and regulations of The Free Web Project`. You may need to copy/paste as this is an exact match algorithm.")

@client.event
async def on_message(message):
    global rule_confirm_channel
    global announcement_channel
    if message.author == client.user:
        return
    memberRole = discord.utils.get(message.channel.guild.roles, name="Member")
    adminRole = discord.utils.get(message.channel.guild.roles, name="Admin")
    guiltyRole = discord.utils.get(message.channel.guild.roles, name = "guilty")
    moderatorRole = discord.utils.get(message.channel.guild.roles, name="Moderator")
    if message.content == "I hereby confirm my acceptance of the rules and regulations of The Free Web Project":
        await message.author.add_roles(memberRole)
    else:
        await message.delete()
    if adminRole in message.author.roles:
        args = message.content.split(" ")
        print(args)
        if args[0] == "TFWP:":
            if args[1] == "configure":
                rule_confirm_channel = discord.utils.get(message.channel.guild.channels, name = "rule-confirmation")
                announcement_channel = discord.utils.get(message.channel.guild.channels, name = "announcements")
            elif args[1] == "accuse":
                person = discord.utils.get(message.channel.guild.members, id = int(args[2][3:-1]))
                await person.remove_roles(moderatorRole, adminRole, memberRole)
                await person.add_roles(guiltyRole)
            elif args[1] == "deaccuse":
                person = discord.utils.get(message.channel.guild.members, id = int(args[2][3:-1]))
                await person.remove_roles(guiltyRole)
                await person.add_roles(memberRole)
            elif args[1] == "announce":
                await announcement_channel.send(message.content[14:])
            elif args[1] == "superannounce":
                for x in message.channel.guild.members:
                    if x != client.user:
                        await x.create_dm()
                        await x.dm_channel.send(message.content[19:])
            await message.delete()

client.run(TOKEN)
