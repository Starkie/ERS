# !/usr/bin/env python3

import requests
import string

# 1. Define una función max () que toma como argumentos dos números y devuelve el mayor de ellos.
def max(x, y):
    if x >= y:
        return x
    else:
        return y

# 2. Escribe una función que toma un carácter (es decir, una cadena de longitud 1) y devuelve True si es una vocal, False en caso contrario
def isVowel(character):
    vowels = ['a', 'e', 'i', 'o', 'u']

    return character in vowels

# 3. Definir una función sum ()  que suma todos los números de una lista de números. Por ejemplo, suma ([1, 2, 3, 4]) debería devolver 10.
def sum(numberList):
    result = 0
    for value in numberList:
        result += value
    return result

# 4. Definir una función reverse () que retorna la inversión de una cadena. Por ejemplo, reverse ("I am testing") debería devolver la cadena "gnitset ma I".
def reverse(value):
    res = ''
    for i in range(len(value), 0, -1):
        res += value[i-1]
    return res

# 5. Un pangrama es una frase que contiene todas las letras del alfabeto Inglés, al menos una vez, por ejemplo: "The quick brown fox jumps over the lazy dog".  Escribe una función para comprobar si una sentencia para ver si es un pangrama o no.
def isPangram(value):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        if letter not in value:
            return False
    return True

def isPangramLambda(value):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return all(letter in value for letter in alphabet)

# 6. Escribe una función char_freq() que toma una cadena y crea una lista de frecuencias de los carácteres que figuran en el mismo. Representa la frecuencia de carácteres con un diccionario Python. Prueba con algo como char_freq ("abbabcbdbabdbdbabababcbcbab").
def char_freq(value):
    counter = dict()
    for char in value:
        counter[char] = counter.get(char, 0) + 1
    return counter

# 7. Escribe una función que Determine si una cadena formada por corchetes es equilibrada, es decir, si consiste enteramente de pares de apertura / cierre de corchetes (en ese orden), y todos los corchetes abiertos se cierran correctamente.
#    []        OK   ][        NOT OK
#    [][]      OK   ][][      NOT OK
#    [[][]]    OK   []][[]    NOT OK
def areBracketBalanced(value):
    nesting_level = 0
    for char in value:
        if char == '[':
            nesting_level += 1
        elif char == ']':
            nesting_level -= 1

        if nesting_level < 0:
            return False

    return nesting_level == 0

print(areBracketBalanced("[]") is True)
print(areBracketBalanced("][") is False)
print(areBracketBalanced("[][]") is True)
print(areBracketBalanced("][][") is False)
print(areBracketBalanced("[[][]]") is True)
print(areBracketBalanced("[]][[]") is False)

# 8. Realiza una función que descarge el libro "ALICE'S ADVENTURES IN WONDERLAND" de "http://www.gutenberg.org/files/11/11-0.txt" vuelque su contenido en un string, elimine caràcteres especiales ('\r.,!:@#$?\''), convierta letras mayúsculas a minúsculas, y muestre entonces las n palabras (pasado por parámetro) más comunes.
def word_frequency(content, num_words):
    counter = dict()

    clean_content = remove_punctuation(content)

    for word in clean_content.split():
        lowerWord = word.lower()
        counter[lowerWord] = counter.get(lowerWord, 0) + 1

    # Sort the dictionary by counting objects.
    sortedCounter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    # Take the first num_words words.
    return sortedCounter[:num_words]

def remove_punctuation(content):
    res = content

    for char in '“”' + string.punctuation:
        res = res.replace(char, "")
    
    return res

def get_content(url):
    return str(requests.get(url).content)
 
print(word_frequency(get_content("http://www.gutenberg.org/files/11/11-0.txt"), 15))

