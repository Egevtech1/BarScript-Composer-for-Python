import json, sys, os
from colorama import Fore, init

init(autoreset=True)

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

if os.path.exists(fileToRun) == False:
    print(Fore.RED + "Файл не существует")
    sys.exit()

with open(fileToRun, 'r') as file:
    data = json.loads(file.read())

if data['Header']['fileType'] != 'brslf':
    print(Fore.RED + 'Возможно, это не файл формата brs')
    sys.exit()

sectionCode = data['Code']
pythonScript = []
vars = {}

for code in sectionCode:
    nameOf=code['name']
    typeOf=code['type']
    metadata=code['metadata']
    data=code['data']

    length = len(sectionCode)
    where = sectionCode.index(code) + 1
    print(Fore.GREEN+'Компиляция скетча'+Fore.WHITE + F' Завершено: {where/length*100}%')

    if nameOf=='print' and typeOf=='function':
        out = []
        for i in data:

            if i['type'] in ['string', 'boolean']:
                out.append(i['data'])
            elif i['type'] in ['*boolean', '*string']:
                out.append(vars[i['data']])
            else:
                print(Fore.RED+'Неизвестный тип данных:' + Fore.WHITE + F' "{i['type']}"')
                sys.exit()

        outScript = ['print("', ''.join(out), '")']
        pythonScript.append(''.join(outScript))
    if typeOf in ['string', 'boolean']:
        vars[nameOf] = data

fileWrited = open(fileToWrite, 'w')

fileWrited.write('\n'.join(pythonScript))
