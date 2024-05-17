from aiogram import Dispatcher,F,Bot
from aiogram.types import Message,CallbackQuery,ReplyKeyboardMarkup,KeyboardButton,FSInputFile
from aiogram.filters.command import Command
from configurate import tken
from Basedata import *
import logging
import asyncio
from button import *
from aiogram.fsm.context import FSMContext
from state import *
from random import *
from gtts import gTTS
import os
from bs4 import BeautifulSoup
import requests
import lxml
logging.basicConfig(level= logging.INFO)
dp = Dispatcher()
bot = Bot(token = tken)



@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(f"Assalomu aleykum hurmatli {message.from_user.full_name}",reply_markup=button)

@dp.message(F.text == "Add new words")
async def addword(message:Message,state:FSMContext):
    await message.answer("Qiziqib turgan so'zni qiriting(English word)")
    await state.set_state(Word.word)
@dp.message(Word.word)
async def tranword(message:Message,state:FSMContext):
    word = message.text
    await state.update_data(
        {"word":word}
    )
    if word != 'My vocabluary' and word != "Game with words" and word != "Guess word by Audio" and word != "Add new words" and word !="Improve Listening skill with audiobooks":
        await state.set_state(Word.trans)
        await message.answer("Translateni qiriting(Ona tilingiz)")
    else:
        await message.answer("This word we can't add",reply_markup=button)
        await state.clear()
@dp.message(Word.trans)
async def transwo(message:Message,state:FSMContext):
    trans = message.text
    d = await state.get_data()
    word= d.get("word")
    await state.update_data(
        {"trans":trans}
    )
    id = message.from_user.id
    check = []
    a = read_word()
    
    for i in a:
            
            
        if message.from_user.id == i[1]:
            check.append(i[0].lower())
            check.append(i[2].lower())    
    if word.lower() in check and trans.lower() in check:
        await message.answer("You have that words,or this word we can't add",reply_markup=button)
    elif word.lower() in check:
        await message.answer("Are you want add this word",reply_markup=agree)
        await state.set_state(Word.correct)
    
    elif trans.lower() in check:
        await message.answer("Are you want add this word",reply_markup=agree)
        await state.set_state(Word.correct)
    
        
    elif trans != 'My vocabluary' and trans != "Game with words" and trans != "Guess word by Audio" and trans != "Add new words" and trans != "Improve Listening skill with audiobooks":
        add_new_word(word,trans,id)
        await message.answer("Added new word",reply_markup=button)
        await state.clear()
    else:
        await message.answer("This word we can't add",reply_markup=button)
        await state.clear()
@dp.message(Word.correct)
async def correction(message:Message,state:FSMContext):
    repl = message.text
    if repl == "🟩Yes":
        d = await state.get_data()
        word = d.get("word")
        trans = d.get("trans")
        id = message.from_user.id
        add_new_word(word,trans,id)
        await message.answer("Added new word",reply_markup=button)
        await state.clear()
    else:
        await message.answer("Okey",reply_markup=button)
        await state.clear()   



@dp.message(F.text == "My vocabluary")
async def voc(message:Message):
    a = read_word()
    b = ""
    z = 0 
    for i in a:
        if message.from_user.id == i[1]:
            z+=1
    if z >0 : 
        for i in a:
            
            if message.from_user.id == i[1]:

                b+= i[0]+"="+i[2]+"\n"
                
        await message.answer(b,reply_markup=delete_btn)
    else:
        await message.answer("Your vocabluary empty")
@dp.callback_query(F.data == "Delete")
async def deleteword(call:CallbackQuery,state:FSMContext):
    await state.set_state(Delword.word)
    await call.message.answer("Input which word(english) you want delete")

@dp.message(F.text,Delword.word)
async def ochirish(message:Message,state:FSMContext):
    check = []
    check1= []
    word = message.text
    a = read_word()
    
    for i in a:
            
            
        if message.from_user.id == i[1]:
            check.append(i[0].lower())
                 

    if word in check:
        

        await state.update_data(
            {"word":word}
        )
        await message.answer("Tarjima bo'lgan so'zni qiriting(Ona tilingiz)")
        await state.set_state(Delword.translate)
    else:
        await message.answer("That word you are not have\nOr you input translate,retry please.")
        await state.set_state(Delword.word)
        

@dp.message(F.text,Delword.translate)
async def delword(message:Message,state:FSMContext):
    trans = message.text
    check1 =[]
    d = await state.get_data()
    word =d.get("word")
    id = message.from_user.id
    
    a = read_word()
    
    for i in a:
            
            
        if message.from_user.id == i[1]:
            
            check1.append(i[2].lower())     

    if trans in check1:
        delete(word,id,trans)
        await message.answer("Ochirildi",reply_markup=button)
        await state.clear()

        
    else:
        await message.answer("That word you are not have\nOr you input word,retry please.")
        await state.set_state(Delword.translate)
    
    
    
    
    
    
    

@dp.message(F.text == "Game with words")
async def sucgame(message:Message,state:FSMContext):
    z = 0
    
    a = read_word() 
    for i in a:
        if message.from_user.id == i[1]:
            z+=1
    if z >0:
        await message.answer("🏁🏁🏁Let's Start🏁🏁🏁", reply_markup=agree)
        await state.set_state(Game.repeat)
    else:
        await message.answer("You are don't have words",reply_markup=button)    
        
@dp.message(Game.repeat)
async def wordgame(message:Message,state:FSMContext):

    text = message.text
    if text == "🟩Yes":
        s = []
        ch = []
        savol = dict()
        di = {}
        num = 1



        c = read_word()
        for j in range(0,len(c)):
            b = randint(0, len(read_word()) - 1)
            if message.from_user.id == c[b][1]:
                cd = c[b][0]
                cb = c[b][2]
                di.update({cd:cb})



                for key,val in di.items():
                    savol.update({key:val})

                a = dict(read_word_game())
                for i in a.values():
                    s.append(i)
                for i in range(3):
                    ch.append(choice(s))

                for key, val in savol.items():
                    ba = 3
                    ch.append(val)

                    sh = set(ch)
                    ch = list(sh)
                    if len(ch) == 4 :
                        aa = 0
                        
                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                            )

                        await message.answer(f"{key}=?\n", reply_markup=game)
                        await state.update_data(
                            {"javob":val}
                        )
                    
                    elif len(ch) == 3:
                        ch.append(s[b-2])

                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                        )

                        await message.answer(f"{key}=?\n", reply_markup=game)
                        await state.update_data(
                            {"javob": val}
                        )
                        pass
                    elif len(ch) == 2:
                        c = randint(0, len(read_word()) - 1)
                        ch.append(s[b-2])
                        ch.append(s[c-2])
                        
                        
                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                        )

                        await message.answer(f"{key}=?\n", reply_markup=game)
                        await state.update_data(
                            {"javob": val}
                        )
                        pass
                    elif len(ch) == 1:
                        d = randint(0,len(read_word()) - 1)
                        c = randint(0, len(read_word()) - 1)
                        ch.append(s[b-2])
                        ch.append(s[c-2])
                        ch.append(s[d-2])
                        
                        
                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                        )

                        await message.answer(f"{key}=?\n", reply_markup=game)
                        await state.update_data(
                            {"javob": val}
                        )
                        pass            
                await state.set_state(Game.javob)
            else:
                continue    
    elif text == "🟥No":
        await message.answer("UHHHH Okey",reply_markup=button)
        await state.clear()
    else:
        await message.answer("Ok",reply_markup=button)   
        await state.clear()
@dp.message(Game.javob)
async def javob(message: Message,state:FSMContext):
    text = message.text

    d = await state.get_data()
    javobtest = d.get("javob")
    if text == javobtest:
        await message.answer(f"✅Great\nYou want to play? ",reply_markup=agree)

        await state.set_state(Game.repeat)


    elif text != javobtest:
        await message.answer("❌Bad",reply_markup=button)
        await state.clear()

@dp.message(F.text == "Guess word by Audio")
async def guess(message:Message,state:FSMContext):
    z = 0
    a = read_word() 
    for i in a:
        if message.from_user.id == i[1]:
            z+=1
    if z >0:
        await message.answer("🏁🏁🏁Let's Start🏁🏁🏁", reply_markup=agree)
        await state.set_state(Audio.audio)
    else:
        await message.answer("You are don't have words",reply_markup=button) 
    

@dp.message(Audio.audio)
async def gameaudio(message:Message,state:FSMContext):

    text = message.text
    if text == "🟩Yes":
        s = []
        ch = []
        savol = dict()
        di = {}

        c = read_word()
        for j in range(0, len(c)):
            b = randint(0, len(read_word()) - 1)
            if message.from_user.id == c[b][1]:
                cd = c[b][0]
                cb = c[b][2]
                di.update({cd: cb})

                for key,val in di.items():
                    savol.update({key:val})

                a = dict(read_word_game())
                for i in a.values():
                    s.append(i)
                for i in range(3):
                    ch.append(choice(s))

                for key, val in savol.items():

                    ch.append(val)

                    sh = set(ch)
                    ch = list(sh)


                    if len(ch) == 4:

                        audio = gTTS(key, lang="en")
                        audio.save("Question.mp3")

                        audiogame = FSInputFile("Question.mp3")
                        await bot.send_audio(message.chat.id, audiogame)
                        os.remove("Question.mp3")

                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                            )


                        await message.answer("Guess this word", reply_markup=game)


                        await state.update_data(
                            {"javob":val}
                        )
                        break
                    elif len(ch) == 3:
                        ch.append(s[b-2])

                        audio = gTTS(key, lang="en")
                        audio.save("Question.mp3")

                        audiogame = FSInputFile("Question.mp3")
                        await bot.send_audio(message.chat.id, audiogame)
                        os.remove("Question.mp3")

                        game = ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text=ch[0]), KeyboardButton(text=ch[1])],
                                [KeyboardButton(text=ch[2]), KeyboardButton(text=ch[3])]
                            ]
                        )

                        await message.answer("Guess this word", reply_markup=game)

                        await state.update_data(
                            {"javob": val}
                        )
                        break

                await state.set_state(Audio.answer)
    elif text == "🟥No":
        await message.answer("UHHHH Okey",reply_markup=button)
        await state.clear()
    else:
        await message.answer("Ok",reply_markup=button)   
        await state.clear()
@dp.message(Audio.answer)
async def javob(message: Message,state:FSMContext):
    text = message.text

    d = await state.get_data()
    javobtest = d.get("javob")
    if text == javobtest:
        await message.answer(f"✅Great\nYou want to play? ",reply_markup=agree)
        await state.set_state(Audio.audio)

    elif text=="🟥No":
        
        await message.answer("❌Bad",reply_markup=button)
        await state.clear()

@dp.message(F.text == "Improve Listening skill with audiobooks")
async def audiobooks(message:Message):
    http = requests.get("https://www.loyalbooks.com/")
    soup = BeautifulSoup(http.content, "lxml")
    name = soup.find(class_="layout2-blue").find_all("b")
    img = soup.find_all("img")
    name1 = []
    img1 = []
    for i in name:
        name1.append(i.text)
    for i in img:
        img1.append("https://www.loyalbooks.com" + i.get("src"))
    reference = soup.find(class_="layout2-blue").find_all("a")
    tuple1 = list()

    set1 = set()
    list1 = []
    for i in reference:
        tuple1.append(i.get("href"))

    del img1[0]
    gb=[]
    for i in range(0,len(read_word()),3):
        gb.append(tuple1[i])
    for i in range(len(name1)):
        ab = img1[i]
        ac = name1[i]
        ad = gb[i]
        await message.answer_photo(photo=ab, caption=f"Title:{ac}\nDownload Link:https://www.loyalbooks.com{ad}")
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot Faoliayatini to'xtadi")