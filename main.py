# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import unidecode as uc
import website as web
import util
import time
import os

start_time = time.perf_counter()
load_dotenv()
ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ç','-','.',' ']
all_words = open('dictionary.txt', encoding='utf-8').readlines()
all_words = list(map(str.lower, all_words))
all_words = list(map(uc.unidecode, all_words))
util.remove_line_break(all_words)
url = os.getenv("URL")

driver = web.setup_driver()
web.start_game(driver, url)
useful_letters = web.find_useful_letters(driver)
useful_letters = list(map(str.lower, useful_letters))
required_letter = useful_letters[0]
unwanted_letters = util.find_unwanted_letters(ALPHABET, useful_letters)
unwanted_words = util.find_unwanted_words(all_words, unwanted_letters)
filtered_words = util.remove_unwanted_words(all_words, unwanted_words)
filtered_words = util.find_required_words(filtered_words, required_letter)
filtered_words = list(set(filtered_words))
filtered_words = sorted(filtered_words)
filtered_words = sorted(filtered_words, key=len)

words_tried = web.send_answers(driver, filtered_words)
points = web.check_success(driver)
correct_guesses = int(points[0])
total_words = int(points[1])
time.sleep(10)
driver.quit()
end_time = time.perf_counter()
total_time = round(end_time-start_time, 2)

print(f"\nWords that met the criteria: {len(filtered_words)}")
print(f"Words attempted by the program: {words_tried}")
print(f"Total words in today's game; {total_words}")
print(f"Words correctly founf by the program: {correct_guesses} ({round((correct_guesses/total_words)*100, 2)}%)")
print(f"Total runtime: {total_time} ({round(round(total_time)/60)}m{round(total_time)%60}s)")