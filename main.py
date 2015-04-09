import config
import sys

bank = []
bank_o_index = {} #original index, ie. column 1
bank_t_index = {} #translated index, i.e, column 2
bank_a_index = {} #alternative / explanation

def get_index(col):
    if col == 0: return bank_o_index
    if col == 1: return bank_a_index
    if col == 2: return bank_t_index
    return {}

def deposit_to_bank(a,count = None, new=False):
    
    if a[0] in bank_o_index:
        print "> Already in bank. Item Number: ", bank_o_index[a[0]]
        count = bank_o_index[a[0]]
        bank[count] = a
        print "> Updated temporarily to bank. Remember to save."
        return
    if count is None:
        count = len(bank)

    bank.append(a)
    bank_o_index[a[0]] = count
    bank_a_index[a[1]] = count
    bank_t_index[a[2]] = count
    if new: print "> Deposited the word to bank. Item Number: ", count+1

def display(a, i=None):
    if len(a) < config.no_fields:
        print "> Invalid row."
        return

    if i is not None:
        print "> Getting from row ", i, "(-th)"
    print ">", a[0], ":", a[1]
    print "> [", a[2], "]"
    print ">", a[3]

def info():
    print "> You have learned: ", len(bank), "word(s)"

def get():
    try:
        row = raw_input("$ Enter the row number from bank: ")
        row = int(row)
        if row < 1 or row> len(bank):
            print "> We cannot found ur record/ transaction"
            return

        #display(bank[row-1], row)
        display(bank[row-1])

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
        deposit_to_bank(a, new=True)

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def modify():
    try:
        row = raw_input("$ Enter the row you want: ")
        row = int(row)
        if row < 1 or row > len(bank):
            print ("> Invalid row.")
            return
        print "$ 1: Original, 2: explanation, 3: translated (used to memorize the word), 4:description"
        col = raw_input("$ Enter the column u want: ")
        col = int(col)
        if col < 1 or col > config.no_fields:
            print "> Invalid col"
            return
        text = raw_input("$ Change to: ")
        text= text.strip()
        old_text = bank[row-1][col-1]
        if len(text) > 0 and text[0] == "+":
            bank[row-1][col-1] = bank[row-1][col-1] +","+ text[1:]
        elif len(text) > 0 and text[-1] == "+": 
            bank[row-1][col-1] = text[:-1] + ","+ bank[row-1][col-1]
        else: bank[row-1][col-1] = text

        d = bank_o_index
        if col == 1: d = bank_a_index
        elif col == 2: d = bank_t_index

        if old_text in d:
            del d[old_text]
            d[bank[row-1][col-1]] = row - 1

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def swap():
    try:
        row = raw_input("$ Enter row: ")
        row = int(row)
        col1 = raw_input("$ Enter column 1: ")
        col2 = raw_input("$ Enter column 2: ")
        col1 = int(col1)
        col2 = int(col2)
        temp = bank[row - 1][col1-1]

        col1_index = get_index(col1-1)
        if bank[row - 1][col1-1] in col1_index:
            del col1_index[bank[row - 1][col1-1]]
        col2_index = get_index(col2-1)
        if bank[row - 1][col2-1] in col2_index:
            del col2_index[bank[row - 1][col2-1]]
        bank[row - 1][col1-1] = bank[row-1][col2-1]
        bank[row-1][col2-1] = temp

        col1_index[bank[row - 1][col1-1]] = row-1
        col2_index[bank[row - 1][col2-1]] = row-1

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def remove():
    try:
        row = raw_input("$ Enter the row u want to remove: ")
        row = int(row)
        if bank[row-1][0] in bank_o_index: del bank_o_index[bank[row-1][0]]
        if bank[row-1][1] in bank_a_index: del bank_a_index[bank[row-1][1]]
        if bank[row-1][2] in bank_t_index: del bank_t_index[bank[row-1][2]]

        del bank[row-1]

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass

def search(findfirst=False):
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
                found.append(i+1)
                if findfirst == True:
                    display(bank[i], i+1)
                    return

        print "> Found: ", [(str(f)+":"+bank[f-1][0]) for f in found]

    except KeyboardInterrupt as k:
        pass
    except EOFError as e:
        pass


def save():
    with open(config.bank_file, "w") as f:
        for cash in bank:
            f.write(config.separator.join(cash) + "\n")
    print "> Saved successfully."

def run():
    while True:
        try:
            command = raw_input("$ ")
            command = command.strip()
            command = command.lower()
            if command == "add":
                add()
            elif "search" in command or "find" in command:
                search()
            elif command == "first":
                search(findfirst=True)
            elif command == "modify":
                modify()
            elif command == "save":
                save()
            elif command == "get":
                get()
            elif command == "info" or command == "ls":
                info()
            elif command == "delete" or command == "remove":
                remove()
            elif command == "swap":
                swap()
            elif command == "exit":
                sys.exit(0)

        except KeyboardInterrupt as k:
            break
        except Exception as ex:
            print "> There is an error happened."
            print str(ex)

def load():
    
    with open(config.bank_file, "r") as f:
        count = 0
        for line in f:
            line = line.strip()
            a = line.split(config.separator)
            if len(a) < config.no_fields:
                continue
            deposit_to_bank(a, count)
            count += 1



if __name__ == "__main__":
    if config.auto_load_bank:
        load()
    run()