import tkinter, subprocess, os, stat, requests, json, csv, cv2
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

window = tkinter.Tk()
window.geometry("1280x720")
window.minsize(1280,720)
window.maxsize(1280,720)
window.resizable(False,False)
window.title("bet365 app")
light_mode = True

def set_theme(screen):
    if light_mode:
        screen.configure(bg="white")
    else:
        screen.configure(bg="black")

def set_btn(screen, command, height, width, text):
    if light_mode:
        return Button(screen, command=command, fg="black", bg="white", height=height, width=width, text= text)
    else:
        return Button(screen, command=command, fg="black", bg="black", height=height, width=width, text= text)

def switch_theme():
    global light_mode
    menu.destroy()
    if light_mode:
        light_mode = False
    else:
        light_mode = True
    startscreen()

def startscreen():
    global menu, theme_btn
    menu = Canvas(window, width=1280, height=720)
    menu.pack()

    #logo
    logo_src = Image.open("logo.jpeg")
    resized_logo_src = logo_src.resize((250,70))
    logo = ImageTk.PhotoImage(resized_logo_src)
    menu.create_image(640, 30, image=logo, anchor="center")
    # background
    set_theme(menu)

    # Buttons
    stat_btn = set_btn(menu, stats_screen,9, 9, "Match Prediction")
    stat_btn.place(x=300, y=250)
    # ar_btn = set_btn(menu, ar_screen,9,9, "Goal Count")
    # ar_btn.place(x=593, y=250)
    ml_btn = set_btn(menu,ml_screen,9,9, "Player Search")
    ml_btn.place(x=886, y=250)
    theme_btn = set_btn(menu,switch_theme,3, 2,"Theme")
    theme_btn.place(x=1200, y=100)
    menu.mainloop()

def kill_command():
    os.chmod('./kill.bash', stat.S_IRWXU)
    subprocess.run('./kill.bash')

def ml_screen():
    global ml_view, playerLabel, playerLabel1, playerLabel2, playerLabel3, playerLabel4
    ml_view = Canvas(menu, width=1280, height=720)
    ml_view.pack()
    # logo
    logo_src = Image.open("logo.jpeg")
    resized_logo_src = logo_src.resize((250, 70))
    logo = ImageTk.PhotoImage(resized_logo_src)

    ml_view.create_image(640, 30, image=logo, anchor="center")
    # background
    set_theme(ml_view)

    # Buttons
    activate_btn = set_btn(ml_view, camera, 9,9, "AR Camera")
    activate_btn.place(x=250,y=250)
    home_btn = set_btn(ml_view,ml_view.destroy,2,5, "Menu")
    home_btn.place(x=100, y=100)

    # Text
    playerLabel = Label(ml_view, text="Player: ")
    playerLabel.config(font="Arial 24")
    playerLabel.place(x=600, y=150)
    playerLabel1 = Label(ml_view, text="Team: ")
    playerLabel1.config(font="Arial 24")
    playerLabel1.place(x=600, y=250)
    playerLabel2 = Label(ml_view, text="DOB: ")
    playerLabel2.config(font="Arial 24")
    playerLabel2.place(x=600, y=350)
    playerLabel3 = Label(ml_view, text="Height: ")
    playerLabel3.config(font="Arial 24")
    playerLabel3.place(x=600, y=450)
    playerLabel4 = Label(ml_view, text="Number: ")
    playerLabel4.config(font="Arial 24")
    playerLabel4.place(x=600, y=550)

    ml_view.mainloop()

def ar_screen():
    ar_view = Canvas(menu, width=1280, height=720)
    ar_view.pack()
    # logo
    logo_src = Image.open("logo.jpeg")
    resized_logo_src = logo_src.resize((250, 70))
    logo = ImageTk.PhotoImage(resized_logo_src)

    ar_view.create_image(640, 30, image=logo, anchor="center")
    # background
    set_theme(ar_view)

    # Buttons
    home_btn = set_btn(ar_view, ar_view.destroy, 2, 5, "Menu")
    home_btn.place(x=100, y=100)

    ar_view.mainloop()

def stats_screen():
    # create frame and scroll bar
    stats_view = Frame(menu)
    stats_view.pack(fill=BOTH, expand=1)
    leaderboard = Canvas(stats_view, width=1260, height=720)
    set_theme(leaderboard)
    leaderboard.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(stats_view, orient=VERTICAL, command=leaderboard.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    logo_src = Image.open("logo.jpeg")
    resized_logo_src = logo_src.resize((250, 70))
    logo = ImageTk.PhotoImage(resized_logo_src)
    leaderboard.create_image(640, 0, image=logo, anchor="center")

    # configure the canvas
    leaderboard.configure(yscrollcommand=scrollbar.set)
    leaderboard.bind('<Configure>', lambda e: leaderboard.configure(scrollregion=leaderboard.bbox("all")))
    # create second frome
    secondframe = Frame(leaderboard)
    leaderboard.create_window((0, 0), window=secondframe, anchor="nw")
    y_axis = 100
    # bet()
    with open('./bets.csv', 'r', newline="") as csvfile:
        fieldnames = ["fixtureId", "Bookie", "Winner", "Odd"]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        if light_mode:
            for line in reader:
                leaderboard.create_text(250, y_axis, text=line["fixtureId"], font="Arial 18")
                leaderboard.create_text(490, y_axis, text=line["Bookie"], font="Arial 18")
                leaderboard.create_text(730, y_axis, text=line["Winner"], font="Arial 18")
                leaderboard.create_text(930, y_axis, text=line["Odd"], font="Arial 18")
                y_axis += 60
        else:
            for line in reader:
                leaderboard.create_text(250, y_axis, text=line["fixtureId"], font="Arial 18", fill="white")
                leaderboard.create_text(490, y_axis, text=line["Bookie"], font="Arial 18", fill="white")
                leaderboard.create_text(730, y_axis, text=line["Winner"], font="Arial 18", fill="white")
                leaderboard.create_text(930, y_axis, text=line["Odd"], font="Arial 18", fill="white")
                y_axis += 60


    # Buttons
    home_btn = set_btn(stats_view, stats_view.destroy, 2, 5, "Menu")
    home_btn.place(x=100, y=100)

    stats_view.mainloop()

player_data = {'Christiano Ronaldo\n':['Team: Man Utd','DOB: 5-2-1985','Height: 187cm','Number: 7'],
               'Lionel Messi\n':['Team: Paris Saint-Germain','DOB: 24-6-1987','Height: 170cm', 'Number: 30'],
               'Erring Harland\n':['Team: Man City','DOB: 21-7-2000','Height: 195cm','Number: 9'],
               'Rod Fanni\n':['Team: -','DOB: 6-12-1986','Height: 186cm','Number: -']
               }

def camera():
    # Load the model
    global playername
    model = load_model('./converted_keras/keras_model.h5')

    # CAMERA can be 0 or 1 based on default camera of your computer.
    camera = cv2.VideoCapture(0)

    # Grab the labels from the labels.txt file. This will be used later.
    labels = open('./converted_keras/labels.txt', 'r').readlines()

    while True:
        # Grab the webcameras image.
        ret, image = camera.read()
        # Resize the raw image into (224-height,224-width) pixels.
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Show the image in a window
        cv2.imshow('Webcam Image', image)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Have the model predict what the current image is. Model.predict
        # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
        # it is the first label and 80% sure its the second label.
        probabilities = model.predict(image)
        # Print what the highest value probabilitie label
        playername = labels[np.argmax(probabilities)]
        print(labels[np.argmax(probabilities)])
        playerLabel.configure(text="Player: " + playername)
        playerLabel1.configure(text=player_data[playername][0])
        playerLabel2.configure(text=player_data[playername][1])
        playerLabel3.configure(text=player_data[playername][2])
        playerLabel4.configure(text=player_data[playername][3])
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break
        window.update()

    camera.release()
    cv2.destroyAllWindows()

def bet():
    headers = {
        "X-RapidAPI-Key": "f070711c08msh798e7116b91842ep1b12b6jsnc9dc1063808b",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    def GetNextFixtures(amount):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        querystring = {"league": "39", "season": "2022", "next": str(amount)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.loads(response.text)['response']

    def GetFixturePredictions(fixtureID):
        url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

        querystring = {"fixture": str(fixtureID)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        dict = json.loads(response.text)['response']
        if len(dict) > 0:
            return dict[0]
        else:
            return None

    def GetFixtureBets(fixtureID):
        url = "https://api-football-v1.p.rapidapi.com/v3/odds"
        querystring = {"fixture": str(fixtureID)}
        response = requests.request("GET", url, headers=headers, params=querystring)
        dict = json.loads(response.text)['response']
        if len(dict) > 0:
            return dict[0]
        else:
            return None

    def CalculateReturnChance(homeWinFrac, awayWinFrac, homeOdds, awayOdds):
        fracdiff = abs(homeWinFrac - awayWinFrac)
        odddiff = abs(homeOdds - awayOdds)
        if fracdiff * odddiff < 0.71:
            # take a risk with the underdog
            return max(homeOdds, awayOdds)
        else:
            # prefer the favourite
            return min(homeOdds, awayOdds)

        return

    def CalculateBestBetForProvider(fixture, fixtureID, prediction, f):
        bets = GetFixtureBets(fixtureID)
        winningTeamID = int(prediction['predictions']['winner']['id'])

        homeWinPercent = float(prediction['predictions']['percent']['home'].strip("%")) / 100.0
        awayWinPercent = float(prediction['predictions']['percent']['away'].strip("%")) / 100.0

        winningTeamID = int(prediction['predictions']['winner']['id'])
        winSide = 0  # 0 = home, 1 = away, 2 = draw
        homeID = int(prediction['teams']['home']['id'])
        awayID = int(prediction['teams']['away']['id'])

        if not prediction or not bets:
            return False, {}

        if winningTeamID == homeID:
            winSide = 0
        elif winningTeamID == awayID:
            winSide = 1
        else:
            return False, {}

        bestOdds = {}
        returnChance = -10000
        bookmakers = bets['bookmakers']
        for book in bookmakers:
            homeOdds = float(book['bets'][0]['values'][0]['odd'])
            awayOdds = float(book['bets'][0]['values'][2]['odd'])
            odd = 0.0
            chance = CalculateReturnChance(homeWinPercent, awayWinPercent, homeOdds, awayOdds)
            winner = "None"
            if chance == homeOdds:
                winner = fixture['teams']['home']['name']
                odd = homeOdds
            else:
                winner = fixture['teams']['away']['name']
                odd = awayOdds

            f.write("{},{},{},{}\n".format(fixtureID, book['name'], winner, str(odd)))
            print("Best Bet For " + book['name'] + "\nMatch Winner: " + winner + "\nOdd: " + str(odd) + "\n")

    f = open("bets.csv", "w")
    next5Fixtures = GetNextFixtures(2)
    f.write("fixtureId,Bookie,Winner,Odd\n")
    for fixture in next5Fixtures:
        fixtureID = fixture['fixture']['id']
        home = fixture['teams']['home']['name']
        away = fixture['teams']['away']['name']
        prediction = GetFixturePredictions(fixtureID)
        CalculateBestBetForProvider(fixture, fixtureID, prediction, f)

    f.close()

startscreen()

