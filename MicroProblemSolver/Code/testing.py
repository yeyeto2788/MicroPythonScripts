import json, time, random

def print_wrapped(pstrMessage):
    """"""
    Lines = [0, 8, 16, 24, 32, 40, 48]
    MaxChars = 16
    words = pstrMessage.split(" ")
    wordlines = []
    message = ""
    for iteraction, word in enumerate(words):
        #print(message)
        remaining_chars = MaxChars - len(message)
        if (len(message + " " + word) <= remaining_chars) or ((len(word) + 1) <= remaining_chars):
            if iteraction == len(words) - 1:
                message += word + " "
                wordlines.append(message)
                break
            else:
                message += word + " "
        else:
            if iteraction == len(words) - 1:
                wordlines.append(message)
                message = word + (" " * remaining_chars)
                wordlines.append(message)
                break
            else:
                wordlines.append(message)
                message = word + " "
        if (len(message) >= MaxChars):
            wordlines.append(message)
            message = ""
    print(wordlines)
    #for Item, Message in enumerate(wordlines):
        #print(Message)
        #print(len(Message))
        #display.text(Message, 0, Lines[Item])
        #display.show()



with open("questions.json", "r") as questionsfile:
    questions = json.loads(questionsfile.read())



b = random.randint(0, len(questions) - 1)
a = questions[str(b)]
#print_wrapped("Can the problem be broken down?")

for i in range(len(questions)):
    print(questions[str(i)])
    print_wrapped(questions[str(i)])

