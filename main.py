import openai, colorama, smtplib, imaplib, quopri, os,threading, pyautogui, time, pyAesCrypt, getpass, subprocess
from pynput.keyboard import Key, Listener


def chatgpt(question):
    openai.api_key = "API-KEY"
    model = "text-davinci-003"
    completion = openai.Completion.create(engine=model, prompt=question, max_tokens=1024, n=1,stop=None,temperature=0.5)
    message = completion.choices[0].text
    return message

def disscution():
    liste =[]
    while True:
        question = str(input(colorama.Fore.RED + "-> "))
        questionF = "ma question : " + str(question)
        liste.append(questionF)

        separateur = "\n"
        qst_poser = separateur.join(liste)

        reponse = str(chatgpt(qst_poser))
        liste.append(reponse)
        print(colorama.Fore.WHITE + liste[-1])

def send_mail(email_sender, email_reciver, mdp, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_sender, mdp)
    server.sendmail(email_sender, email_reciver, message)
    server.quit()

def check_mails(email_sender, mdp, email_reciver):
    # Connect to the email server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_sender, mdp)

    # Select the inbox
    mail.select('inbox')

    # Search for all emails
    result, data = mail.search(None, 'ALL')

    # Get the last email's ID
    emails = data[0].split()
    latest_email_id = emails[-1]

    # Fetch the last email
    result, data = mail.fetch(latest_email_id, '(RFC822)')

    encoded_string = data[0][1]
    decoded_string = quopri.decodestring(encoded_string).decode('ISO-8859-1')
    # print(decoded_string)

    split_paragraph = decoded_string.split(f"From: {email_reciver}")
    print(split_paragraph[1])

    # Close the connection
    mail.close()
    mail.logout()

def disscution_longue():
    liste = []
    while True:
        os.system("echo > text.txt")
        os.system("nano text.txt")
        fichier = open("text.txt", "r")
        contenu = fichier.read()
        fichier.close()

        liste.append(contenu)

        separateur = "\n"
        qst_poser = separateur.join(liste)

        reponse = str(chatgpt(qst_poser))
        liste.append(reponse)
        print(liste[-1])
        pause = input("tapez pour continuez...")

def on_release(key):
    if key == Key.esc:
        crypter(password,bufferSize)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.5)
        pyautogui.press('enter')

def thread_function():
    with Listener(on_release=on_release) as listener:
        listener.join()

def mail_thread():
    type_mail = str(input("(short/long) : "))
    if type_mail == "short":
        message = str(input("-> "))
        send_mail(email_sender, email_reciver, mdp, message)
    else:
        os.system("echo > text.txt")
        os.system("nano text.txt")
        fichier = open("text.txt", "r")
        contenu = fichier.read()
        fichier.close()
        send_mail(email_sender, email_reciver, mdp, str(contenu))

def crypter(password,bufferSize):
    for file in os.listdir("."):
        if file.endswith(".txt") or file.endswith(".py"):
            if file != "start.py":
                pyAesCrypt.encryptFile(file, file+".crp", password, bufferSize)
                os.remove(file)

def menu():
    print(" Menu\n")
    print(" [0] afficher le menu")
    print(" [1] envoyé un mail (long/court)")
    print(" [2] vérifier les mails recu")
    print(" [3] chatGPT (phrases courtes)")
    print(" [4] chatGPT (phrases longues)")
    print(" [5] Note") 
    print(" [Autre] Exit")
    print("\nRemarque :\n\ttoujours quitter l'App avec la touche 'esc' du clavier")

def note():
    os.system("nano note.txt")

# info pour envoyé les mails
email_sender = "mail 1"
email_reciver = "mail 2"
mdp = "password"
bufferSize = 64 * 1024

# Création du thread
quitter = threading.Thread(target=thread_function)
send = threading.Thread(target=mail_thread)

# Démarrage du thread
quitter.start()

print("\n** new pass **")
password = getpass.getpass()
password_confirm = getpass.getpass()

# on vérifie si les deux mot de passe se resemblent
while password != password_confirm:
    print("\nTry again !")
    password = getpass.getpass()
    password_confirm = getpass.getpass()

os.system("clear")
select = str(input("--> "))
if select == "0":
    menu()

elif select == "1":
    send.start()
    send.join()
    print("envoyé !")

elif select == "2":
    check_mails(email_sender,mdp, email_reciver)

elif select == "3":
    disscution()

elif select == "4":
    disscution_longue()

elif select == "5":
    note()
else:
    while select!="0" or  select!="1" or select!="2" or select!="3" or select!="4" or select!="5":
        select = str(input("--> "))
