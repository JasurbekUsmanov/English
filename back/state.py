from aiogram.fsm.state import StatesGroup,State

class Word(StatesGroup):
    word = State()
    trans = State()
    correct = State()
class Delword(StatesGroup):
    word = State()
    translate = State()

class Game(StatesGroup):

    javob= State()
    repeat = State()
class Audio(StatesGroup):
    audio = State()
    answer = State()
class Audiobook(StatesGroup):
    audiobook = State()
    select = State()
    retry = State()