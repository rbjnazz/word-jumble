import csv
import random
import requests
from bs4 import BeautifulSoup
#from os import system, name, path
import os

# 370_103 words


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class WordIndex:
    indexBin = []

    def __init__(self, word):
        self.word = word

    def StoreIndex(self):
        collect = self.indexBin.append(self.word)
        return collect


class WordGenerator:
    show = ''

    def __init__(self, word):
        self.word = word

    def OrigWord(self):
        return self.word

    def GetJumbleWord(self):
        jumbled_word = random.sample(self.word, len(self.word))
        return word_splitter(jumbled_word).upper()


class GetAttempts:
    totalAttempts = 0

    @classmethod
    def add(cls):
        cls.totalAttempts += 1
        return cls.totalAttempts

    @classmethod
    def revert(cls):
        cls.totalAttempts = 0
        return cls.totalAttempts


class AddPoints:
    addedPoints = 0

    def __init__(self, point):
        self.point = point

    def add(self, add_point):
        self.point += add_point
        self.addedPoints = self.point
        return self.addedPoints


def get_index():
    word = random.randint(0, 370_102)
    return word


def get_word():
    index = get_index()
    if index in WordIndex.indexBin:
        get_index()
    else:
        WordIndex(index).StoreIndex()
        with open('words.txt', mode='r', encoding='utf-8') as file:
            read_word = file.readlines()
            word = read_word[index]
            if len(word) <= 2:
                get_word()
            elif word in read_status(False):
                get_word()
            else:
                return word


def word_splitter(word):
    split_word = ""
    for char in word:
        split_word += char + ' '
    return split_word[:-1]


def load_status():
    try:
        with open('status.csv', mode='r', encoding='utf-8') as csv_file:
            file = csv.reader(csv_file)
            total_points = []
            for row in file:
                total_points.append(int(row[1]))
            return sum(total_points)
    except FileNotFoundError:
        with open('status.csv', mode='w+', encoding='utf-8', newline='') as csv_file:
            write_file = csv.writer(csv_file)
            write_file.writerow([20 * '-', 0])
            return 0


def read_status(read_all):
    with open('status.csv', mode='r', encoding='utf-8') as csv_file:
        words = []
        points = []
        stat = ''
        status = csv.reader(csv_file)
        if not read_all:
            for line in status:
                words.append(line[0])
            return words
        else:
            for line in status:
                words.append(line[0])
                points.append(line[1])
            for word, point in zip(words, points):
                stat += ''.rjust(20) + word.ljust(40) + '+' + point.ljust(10) + '\n'
            return '\n' + stat


def save_status(word, points):
    with open('status.csv', mode='a', encoding='utf-8', newline='') as csv_file:
        status = [word, points]
        stat = csv.writer(csv_file)
        stat.writerow(status)


def save_temp_definition(definition):
    with open('temp_.txt', mode='a', encoding='utf-8') as temp:
        temp.write(definition)


def read_temp_definition(line_num):
    try:
        r = line_num - 1
        line = random.randint(0, r)
    except ValueError:
        line = 0
    with open('temp_.txt', mode='r', encoding='utf-8') as temp:
        read = temp.readlines()
        return f'\nDefinition:\n{read[line]}'


def del_temp_definition():
    if os.path.exists('temp_.txt'):
        os.remove('temp_.txt')
    else:
        pass


def welcome():
    clear_terminal()
    input('\n\tWelcome to Word Jumble\n\n\tGuess the jumbled word and earn points.\n'
          '\n\tInstructions:\n\t"W" to skip or show the word.\n\t"S" to show status.'
          '\n\t"ENTER" to reshuffle.\n\t"Q" to quit.\n\n\tcontinue...\n\t>>> ')


def run_game():
    clear_terminal()
    word = get_word().replace("\n", "")
    correct_answer = WordGenerator(word)
    WordGenerator.show = correct_answer.GetJumbleWord()
    attempts = GetAttempts
    points = AddPoints(0)
    match_list_len = []
    get_definition(word, match_list_len)

    def start_game():
        print(f'\n\n\t{WordGenerator.show}')
        user = str(input('\n\t>>> '))
        answer = str(correct_answer.OrigWord()).upper()
        half = int(len(word) / 2)
        if attempts.totalAttempts >= 5:
            r = random.randint(1, half)
            input(f'\n\twrong!\n\n\tClue: starts with {answer[:r]}\n<<<')
            attempts.revert()
            clear_terminal()
            try:
                line = match_list_len[0]
                print(read_temp_definition(line))
            except IndexError:
                print('\nDefinition:\n???\nNo internet connection')
        elif user == '':
            clear_terminal()
            WordGenerator.show = correct_answer.GetJumbleWord()

            print(4 * '\n')
            start_game()
        elif user.upper() == 'S':
            clear_terminal()
            print('\n\n' + ''.rjust(20) + 'Words'.ljust(40) + 'Points'.ljust(10))
            input(f'{read_status(True)}\n{"".rjust(20)}{"Total points:".ljust(40)}{str(load_status()).ljust(10)}\n<<<')
            clear_terminal()
            try:
                line = match_list_len[0]
                print(read_temp_definition(line))
            except IndexError:
                print('\nDefinition:\n???\nNo internet connection')
        elif user.upper() == 'Q':
            del_temp_definition()
            exit()
        elif user.upper() == 'W':
            input(f'\n\tWord: {answer.capitalize()}\n<<<')
            del_temp_definition()
            attempts.revert()
            run_game()
        elif user.upper() == answer:
            pt = points.add(len(word))
            AddPoints.addedPoints = pt
            save_status(word.capitalize(), AddPoints.addedPoints)
            input(f'\n\tcorrect!\n\n\tWord: {answer.capitalize()}\n\tPoints: {AddPoints.addedPoints}\n<<<')
            del_temp_definition()
            attempts.revert()
            run_game()
        else:
            input(f'\n\twrong!\n<<<')
            attempts.add()
            clear_terminal()
            try:
                line = match_list_len[0]
                print(read_temp_definition(line))
            except IndexError:
                print('\nDefinition:\n???\nNo internet connection')
        start_game()
    start_game()


def get_definition(word, match_list_len):
    print('\n\tplease wait...\n\treading online content')
    try:
        url = f"https://www.merriam-webster.com/dictionary/{word}"
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        match_list = []
        wiki_list = []
        try:
            for definition in soup.find_all('span', class_='dtText'):
                match_list.append(definition.text)
                save_temp_definition(definition.text + '\n')
            if len(match_list) == 0:
                url = f'https://en.wiktionary.org/wiki/{word}#English'
                source = requests.get(url).text
                soup = BeautifulSoup(source, 'lxml')
                try:
                    for definition in soup.find_all('ol'):
                        wiki_list.append(definition.find('li').text)
                        save_temp_definition(definition.text + "\n")
                    if len(wiki_list) == 0:
                        run_game()
                    else:
                        pass
                except AttributeError:
                    run_game()
                clear_terminal()
                w = len(wiki_list)
                match_list_len.append(w)
                print(read_temp_definition(w))
            else:
                pass
        except AttributeError:
            run_game()
        if len(wiki_list) == 0:
            clear_terminal()
            x = len(match_list)
            match_list_len.append(x)
            print(read_temp_definition(x))
        else:
            pass
    except requests.ConnectionError:
        clear_terminal()
        print('\nDefinition:\n???\nNo internet connection')


if __name__ == '__main__':
    try:
        del_temp_definition()
        AddPoints.totalPoints = load_status()
        welcome()
        run_game()
    except FileNotFoundError:
        AddPoints.totalPoints = load_status()
        welcome()
        run_game()
    except KeyboardInterrupt:
        del_temp_definition()
