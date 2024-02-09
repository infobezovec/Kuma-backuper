import requests
import json
import sys
import random
from termcolor import colored


DEBUG = True
backup_url = 'https://kuma-addres:7223/api/v1/system/backup/'
resources_url = 'https://kuma-addres:7223/api/v1/resources/'
token = "your-token"  

version = '0.1'

def kuma_backup():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(backup_url, headers=headers, verify=False)

    if response.status_code == 200:
        with open("backup.tar.gz", "wb") as file:
            file.write(response.content)
        print("Файл успешно сохранен.")
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")

def generate_readme(answer):
    ctr = 0
    fctr = 0
    with open("responce.json", "wt") as res:
        with open("RULES-README.md", "wt") as file:
            file.write("<caption style=\"text-align: center;\">KUMA's correlation rules knowledgebase</caption>\n\
<table border=\"1\">\n\
    <tr name=\"HEADER\"> \n\
        <td style=\"text-align: center;\">LID</td>\n\
        <td style=\"text-align: center;\">Tenant</td>\n\
        <td style=\"text-align: center;\">Tag</td>\n\
        <td style=\"text-align: center;\">Rule name</td>\n\
        <td style=\"text-align: center;\">Rule description</td>\n\
        <td style=\"text-align: center;\">KUMA ID</td>\n\
        <td style=\"text-align: center;\">Created by</td>\n\
    </tr>\n")
            while len(answer) > ctr:
                buff = json.dumps(answer[ctr])
                res.write(buff)
                buff = json.loads(buff)
                name = buff.get("kind")
                if name == "correlationRule":
                    file.write("\t<tr>\n")
                    file.write("\t\t<td>" + str(fctr) + "</td>\n") 
                    file.write("\t\t<td>" + buff.get("tenantName") + "</td>\n")
                    file.write("\t\t<td>" + "-" + "</td>\n")
                    file.write("\t\t<td>" + buff.get("name") + "</td>\n")
                    file.write("\t\t<td>" + buff.get("description") + "</td>\n")
                    file.write("\t\t<td>" + buff.get("id") + "</td>\n")
                    file.write("\t\t<td>" + buff.get("userName") + "</td>\n")
                    file.write("\t</tr>\n")
                    fctr +=1
                        
                ctr +=1
            file.write("</table>\n")
            file.close  
        res.close

def kuma_rules_request():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "kind": "correlationRule",
    }
    try:
        response = requests.get(resources_url, headers=headers, verify=False)
        if response.status_code == 200:
            answer = json.loads(response.text)
            print(response.status_code)
            return answer
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
    except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(colored("Ошибка! \n", "red"))
            print(str(exc_value))
    return 0

def print_help():  
   print("-h: To print help\n\
-r: To make rules dump int to README.md\n\
-b: To make backup in 'backup.tar.gz'")
    
    
def print_logo():
    color = ['red','green', 'yellow', 'blue', 'magenta', 'cyan']
    print(colored("""
 __    __                                          __                            __                                               
|  \  /  \                                        |  \                          |  \                                              
| $$ /  $$ __    __  ______ ____    ______        | $$____    ______    _______ | $$   __  __    __   ______    ______    ______  
| $$/  $$ |  \  |  \|      \    \  |      \       | $$    \  |      \  /       \| $$  /  \|  \  |  \ /      \  /      \  /      \ 
| $$  $$  | $$  | $$| $$$$$$\$$$$\  \$$$$$$\      | $$$$$$$\  \$$$$$$\|  $$$$$$$| $$_/  $$| $$  | $$|  $$$$$$\|  $$$$$$\|  $$$$$$\\
| $$$$$\  | $$  | $$| $$ | $$ | $$ /      $$      | $$  | $$ /      $$| $$      | $$   $$ | $$  | $$| $$  | $$| $$    $$| $$   \$$\\
| $$ \$$\ | $$__/ $$| $$ | $$ | $$|  $$$$$$$      | $$__/ $$|  $$$$$$$| $$_____ | $$$$$$\ | $$__/ $$| $$__/ $$| $$$$$$$$| $$      
| $$  \$$\ \$$    $$| $$ | $$ | $$ \$$    $$      | $$    $$ \$$    $$ \$$     \| $$  \$$\ \$$    $$| $$    $$ \$$     \| $$      
 \$$   \$$\ \$$$$$$  \$$  \$$  \$$  \$$$$$$$       \$$$$$$$   \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$ | $$$$$$$   \$$$$$$$ \$$      
                                                                                                    | $$                          
                                                                                                    | $$                          
                                                                                                     \$$                                                                                          
""", color[random.randint(0, len(color)-1)]))
    print(colored("Kuma backup automatization! \t Now we can backup only Rules and Kuma's data!", 'green',  attrs=['bold']))
    print (colored('version:' + version,  attrs=['bold']))

def main():
    print_logo()

    if len(sys.argv) < 2:
        
        print(colored("Less Args! \nUse -h to help!", 'red', attrs=['bold']))
    else:
        if sys.argv[1] == '-h':
            print_help()
        elif sys.argv[1] == '-r':
            responce = kuma_rules_request()
            if responce != 0:
                generate_readme(responce)

        elif sys.argv[1] == '-b':
            kuma_backup()
        else:
            print(colored("Wrong Args! \nUse -h to help!", 'red', attrs=['bold']))


if __name__ == '__main__':
    main()

    