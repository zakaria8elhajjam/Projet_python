import os
from random import *
import shutil
from colorama import *
from datetime import *
def clearTerminal():
    os.system('cls')
def PrintPoints(num):
    print(Fore.LIGHTBLACK_EX+"•"*num)
def EndLine(num):
    print("\n"*num)
def Space(num):
    print("\t"*num,end="")
def IdGenerator(DB):
    DB.execute("SELECT id FROM person")
    AllId = DB.fetchall()
    Id = randint(100000,999999)
    while Id in AllId :
        Id = randint(100000,999999)
    return Id
def CompareDate(date):
    today = datetime.now().date()
    date = datetime.strptime(date, "%Y-%m-%d").date()
    if date ==  today:
        return True
    else:
        return False
def delete(DB,conn):
    today = datetime.now().date()
    DB.execute("DELETE FROM reminder WHERE date<?",(today,))
    conn.commit()
def calculate_num_lines(text):
    text_length = len(text)
    terminal_width , _ = shutil.get_terminal_size()
    num_lines = (text_length + terminal_width - 1) // terminal_width
    return num_lines
def create_paragraphs(text, max_chars_per_paragraph):
    words = text.split()
    paragraphs = []
    current_paragraph = ""
    terminal_width , _ = shutil.get_terminal_size()
    for word in words:
        if len(current_paragraph + word) <= max_chars_per_paragraph:
            current_paragraph += word + " "
        else:
            paragraphs.append(current_paragraph.ljust(terminal_width-16))
            current_paragraph = word + " "
    if current_paragraph:
        paragraphs.append(current_paragraph.ljust(terminal_width-16))

    return paragraphs


