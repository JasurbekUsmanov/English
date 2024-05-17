import sqlite3
def add_new_table():
    try:
        connection = sqlite3.connect("telegram.db")
        cursor = connection.cursor()
        new_table= """CREATE TABLE englishbot(
        WORD VARCHAR(50) NOT NULL,
        ID BIGINT NOT NULL,
        TRANSLATE VARCHAR(50) NOT NULL
        );"""
        cursor.execute(new_table)
        connection.commit()
        connection.close()
    except sqlite3.Error as error:
        print("Xatoingiz bor",error)
    finally:
        if connection:
            cursor.close()
            

def add_new_word(word,translate,id):
    try:
        connection = sqlite3.connect("telegram.db")
        cursor = connection.cursor()
        new_table="""INSERT INTO englishbot(WORD,ID,TRANSLATE) VALUES(?,?,?)"""
        cursor.execute(new_table,(word,id,translate))
        connection.commit()
    except sqlite3.Error as error:
        print("Xatoingiz bor",error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def read_word():
    try:
        connection = sqlite3.connect("telegram.db")
        cursor = connection.cursor()
        new_table="""SELECT * FROM englishbot"""

        cursor.execute(new_table)

        r = cursor.fetchall()
        return r
    except:
        print("Xatoingiz bor")
    finally:
        if connection:
            cursor.close()
            connection.close()


def read_word_game():
    try:
        connection = sqlite3.connect("telegram.db")
        cursor = connection.cursor()
        new_table="""SELECT word,translate FROM englishbot"""

        cursor.execute(new_table)

        r = cursor.fetchall()
        return r
    except:
        print("Xatoingiz bor")
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete(word,id,translate):
    try:
        connection = sqlite3.connect('telegram.db')
        cursor = connection.cursor()
        new_table="""Delete from englishbot where word=? and id=? and translate=?"""

        cursor.execute(new_table,(word,id,translate))
        connection.commit()
        
        cursor.close()
    except sqlite3.Error as error:
        print("Xatoingiz bor",error)
    finally:
        if connection:
            connection.close()


def read_id():
    try:
        connection = sqlite3.connect("telegram.db")
        cursor = connection.cursor()
        new_table="""SELECT ID FROM englishbot"""

        cursor.execute(new_table)

        r = cursor.fetchall()
        return r
    except:
        print("Xatoingiz bor")
    finally:
        if connection:
            cursor.close()
            connection.close()