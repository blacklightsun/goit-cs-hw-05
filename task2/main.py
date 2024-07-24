import string
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        # print(response.status_code)
        # print(response.text)
        return response.text
    except requests.RequestException as e:
        print('Error is ', e)
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(result):
    word_list = []
    qty_list = []
    for key, value in result.items():
        word_list.append(key)
        qty_list.append(value)

    df = pd.DataFrame({'words': word_list, 'qty': qty_list})
    df_sorted = df.sort_values(by="qty", ascending=False).iloc[:10,:].sort_values(by="qty", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df_sorted['words'], df_sorted['qty'])
    plt.ylabel("Word", fontsize="small", color="midnightblue")
    plt.xlabel("Quantity", fontsize="small", color="midnightblue")
    plt.title("TOP-10 words of the text", fontsize=15)
    plt.show()

    # print(df_sorted)
    return df_sorted.sort_values(by="qty", ascending=False)

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        search_words = []
        result = map_reduce(text, search_words)
        top_result = visualize_top_words(result)

        print("TOP-10 words of the text:", top_result)
    else:
        print("Error: entry text don`t be received.")