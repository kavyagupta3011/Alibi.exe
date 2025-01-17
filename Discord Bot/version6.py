import discord
from discord.ext import commands
import random
import asyncio
from final_lists import questions_list 
from lists import title, description_victim, description_crime_scene, items, autopsy_report, forensic_report, backstories, alibis, description_alibis, witnesses, distance, answer, solution

i=0
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


# Define your questions and answers
questions = questions_list
    # Add more questions, answers, and info here

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command()
async def start(ctx):
    await ctx.send("Welcome to the Murder Mystery Game! I will ask you a series of questions. Answer them correctly to reveal information about the case Type 'exit' anytime to end the game.")
    await ask_question(ctx.channel, ctx.author, ctx)

async def ask_question(channel, author, ctx):
    questions_asked = 1

    shuffled_questions = questions 
    random.shuffle(shuffled_questions)

    for question in shuffled_questions:
        await channel.send("```css\n{}\n```".format(question["question"]))  # Box around the question

        def check(msg):
            return msg.author == author and msg.channel == channel

        try:
            response = await client.wait_for('message', timeout=50, check=check)
        except asyncio.TimeoutError:
            await channel.send("Time's up! You failed to answer the question." )
        else:
            if response.content.lower() == 'exit':
                await channel.send("Game ended.")
                break
            elif response.content.strip().lower() == question["answer"].lower():
                if(questions_asked == 1):
                    info_message = description_victim[i]
                    await channel.send("✅ Correct! Here's some information about the victim  : '{}'".format(description_victim[i]))
                elif(questions_asked == 2):
                    info_message = description_crime_scene[i]
                    await channel.send("✅ Correct! Here's the description of the crime scene: '{}'".format(description_crime_scene[i]))
                elif(questions_asked == 3):
                    info_message = items[i]
                    await channel.send("✅ Correct! The crime scene investigation has drawn attention to these four items  : '{}'".format(items[i]) )
                elif(questions_asked == 4):
                    info_message = autopsy_report[i]
                    await channel.send("✅ Correct! Examination of the body of the victim has given the following results : '{}'".format(autopsy_report[i]))
                elif(questions_asked == 5):
                    info_message = forensic_report[i]
                    await channel.send("✅ Correct! Here's the forensic evidence cololected from the crime scene : '{}'".format(forensic_report[i]))
                elif(questions_asked == 6):
                    info_message = backstories[i]
                    await channel.send("✅ Correct! We have four individuals under scrutiny : '{}'".format(backstories[i]))
                elif(questions_asked == 7):
                    info_message = alibis[i]
                    await channel.send("✅ Correct! However the suspects claim to have the following alibis : '{}'".format(alibis[i]))
                elif(questions_asked == 8):
                    info_message = description_alibis[i]
                    await channel.send("✅ Correct! here is a description of the places mentioned in the alibis '{}'".format(description_alibis[i]))
                elif(questions_asked == 9):
                    info_message = witnesses[i]
                    await channel.send("✅ Correct! Any good detective searches for witnesses here are the witnesses at the places where the suspects told they were at : '{}'".format(witnesses[i]))
                elif(questions_asked == 10):
                    info_message = distance[i]
                    await channel.send("✅ Correct! hmm, there is always a possibily that the killer could have travelled between these places. Here is the distance between those places and the crime scene  : '{}'".format(distance[i]))
                try:
                    await client.wait_for('reaction_add',check=check_reaction_and_author(info_message,author,'✅'))
                except asyncio.TimeoutError:
                    pass
            else:
                await channel.send("❌ Incorrect! moving on to the next question")  # Wrong emoji and text
            questions_asked += 1

        if questions_asked == 11:
            await channel.send("It's now time to put your little grey cells to work and solve the case! Who do u think the murderer is '{}'?".format(suspects[i]))
            await final_answer(ctx.channel, ctx.author, ctx) 
            break

async def final_answer(channel, author, ctx):
    def check(msg):
            return msg.author == author and msg.channel == channel
    try:
        response = await client.wait_for('message', timeout=50, check=check)
    except asyncio.TimeoutError:
        await channel.send("Time's up! You failed to answer the question." )
    else:
        if response.content.strip().lower() == answer[i].lower(): 
            await channel.send("Congratulations")
        else:
            await channel.send("Incorrect")
    await channel.send(solution[i])

def check_reaction_and_author(message, author, emoji):
    def check(reaction,user):
        return user == author and str(reaction.emoji) == emoji
    return check

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run('MTIyNTA1MjA3MDMyODE0NDAxMw.GnGiaA.gSoc_sL_7Jn1BKRj0IwA5IQyrouoBxmQwzWjqA')








