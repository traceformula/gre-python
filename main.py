import config
import sys

bank = []
bank_o_index = {} #original index, ie. column 1
bank_t_index = {} #translated index, i.e, column 2
bank_a_index = {} #alternative / explanation

def deposit_to_bank(a,count = None):
    
    if a[0] in bank_o_index:
        count = bank_o_index[a[0]]
        bank[count] = a
        return
    if count is None:
        count = len(bank)

    bank.append(a)
    bank_o_index[a[0]] = count
    bank_a_index[a[1]] = count
    bank_t_index[a[2]] = count

def display(a, i=None):
    if len(a) < config.no_fields:
        print "> Invalid row."
        return

    if i is not None:
        print "> Getting from row ", i, "(-th)"
    print ">", a[0], ":", a[1]
    print "> [", a[2], "]"
    print a[3]

def info():
    print "You have learned: ", len(bank), "word(s)"

def get():
    try:
        row = raw_input("$ Enter the row number from bank: ")
        row = int(row)
        if row < 0 or row>= len(bank):
            print "> We cannot found ur record/ transaction"
            return

        display(bank[row], row)
    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def add():
    try:
        a = []
        word =         raw_input("$ Enter ur word           : ")
        a.append(word)
        explanation =  raw_input("$ Enter ur exp            : ")
        a.append(explanation)
        translated =   raw_input("$ Enter ur translated word: ")
        a.append(translated)
        example =      raw_input("$ Enter ur example        : ")
        a.append(example)
        deposit_to_bank(a)

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def modify():
    pass

def search():
    print "$ 1: Original, 2: explanation, 3: translated (used to memorize the word), 4:description"
    try:
        col = raw_input("$ Enter ur choice: ")
        col = int(col) - 1
        if col < 0 or col >= config.no_fields: 
            print "> Invalid choice."
            return
        word = raw_input("$ Enter ur word: ")
        word = word.strip()

        found = []
        for i in range(len(bank)):
            if  word in bank[i][col]:
                found.append(i)

        print "> Found: ", found

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass


def save():
    with open(config.bank_file, "w") as f:
        for cash in bank:
            f.write(config.separator.join(cash) + "\n")

def run():
    while True:
        try:
            command = raw_input("$ ")
            if command == "add":
                add()
            elif "search" in command:
                search()
            elif command == "modify":
                modify()
            elif command == "save":
                save()
            elif command == "get":
                get()
            elif command == "info":
                info()
            elif command == "exit":
                sys.exit(0)

        except KeyboardInterrupt as k:
            break

def load():
    
    with open(config.bank_file, "r") as f:
        count = 0
        for line in f:
            a = line.split(config.separator)
            if len(a) < config.no_fields:
                continue
            deposit_to_bank(a, count)
            count += 1



if __name__ == "__main__":
    if config.auto_load_bank:
        load()
    run()