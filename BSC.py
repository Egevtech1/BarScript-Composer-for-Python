import json, sys, os
from colorama import Fore, init

init(autoreset=True)
print('BarScript Composer for Python: ver.:0.0.1.1')
args = []
j = sys.argv
for i in range(1, len(j)):
    args.append(j[i])

if not '-l' in args or not '-o' in args:
    print(Fore.RED+'Слишком мало аргументов')
    sys.exit()

for i in range(0, len(args)):
    arg = args[i]
    if arg == '-l':
        i+=1
        try:
            fileToRun = args[i]
        except:
            print(Fore.RED + 'Что-то пошло не так')
            sys.exit()
        continue
    if arg == '-o':
        i+=1
        try:
            fileToWrite = args[i]
        except:
            print(Fore.RED + 'Что-то пошло не так')
            sys.exit()
        continue
print(F'{Fore.YELLOW}[--]{Fore.WHITE}Открытие файла')
if os.path.exists(fileToRun) == False:
    print(F'{Fore.RED}[ER]{Fore.WHITE}Открытие файла: файл не найден')
    sys.exit()

with open(fileToRun, 'r') as file:
    data = json.loads(file.read())

if data['Header']['fileType'] != 'brslf':
    print(F'{Fore.RED}[ER]{Fore.WHITE}Открытие файла: файл не формата brs')
    sys.exit()

print(F'{Fore.GREEN}[ОК]{Fore.WHITE}Открытие файла')
sectionCode = data['Code']
pythonScript = []
vars = {}

print(F'{Fore.YELLOW}[--]{Fore.WHITE}Компоновка скетча')
for code in sectionCode:
    try:
        nameOf=code['name']
        typeOf=code['type']
        metadata=code['metadata']
        data=code['data']

        length = len(sectionCode)
        where = sectionCode.index(code) + 1
        print(F'{Fore.GREEN}[{int(where/length*100)}%]{Fore.WHITE}Компоновка скетча')

        if nameOf=='print' and typeOf=='function':
            out = []
            for i in data:

                if i['type'] in ['string', 'boolean']:
                    out.append(i['data'])
                elif i['type'] in ['*boolean', '*string']:
                    out.append(vars[i['data']])
                else:
                    print(F'{Fore.RED}[ERR]{Fore.White} Компоновка скетча: неизвестный тип данных:' + Fore.WHITE + F' "{i['type']}"')
                    sys.exit()

            outScript = ['print("', ''.join(out), '")']
            pythonScript.append(''.join(outScript))
        if typeOf in ['string', 'boolean']:
            vars[nameOf] = data
    except:
        print(F'{Fore.RED}[ERR]{Fore.WHITE}Компоновка скетча: ошибка LexCode')

print(F'{Fore.GREEN}[ОК]{Fore.WHITE}Компоновка скетча')
print(F'{Fore.YELLOW}[--]{Fore.WHITE}Запись')

try:
    fileWrited = open(fileToWrite, 'w')

    fileWrited.write('\n'.join(pythonScript))
    print(F'{Fore.GREEN}[ОК]{Fore.WHITE}Запись')
except:
    print(F'{Fore.RED}[ER]{Fore.WHITE}Запись')
