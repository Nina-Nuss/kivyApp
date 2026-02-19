import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty

version = "Version: 0.1"
startPicture = "Bilder//test.png"
background = "Bilder//empty.png"

# "LevelNummer;Name;Bestzeit" Temporär
fromSQL1 = "1;Anfang;12:35"
fromSQL2 = "2;Das Beispiel;1:35"
fromSQL3 = "3;Das nächste Beispiel;12:01"
fromSQL4 = "4;Das Ende;1:10"
SqlListe = [fromSQL1,fromSQL2,fromSQL3,fromSQL4]
#https://www.geeksforgeeks.org/python/python-set-background-template-in-kivy/

class myGridLayout(GridLayout):
    version = StringProperty(version)
    startPicture = StringProperty(startPicture)
    background = StringProperty(background)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class myScrollView(ScrollView):
    xBreite, yHoehe = NumericProperty(0.9), NumericProperty(0.9)
    test = ListProperty(["Bilder//testVorschau.png","Bilder//testVorschau.png","Bilder//testVorschau.png","Bilder//testVorschau.png"])
    startPicture = StringProperty(startPicture)
    background = StringProperty(background)
    temp =[]
    #Momentan Temporär bis SQL funktioniert
    for i in SqlListe:
        tempStrlis = (i.split(";"))
        tempStr = "Level "+tempStrlis[0].ljust(40,' ')
        print(len("Level "+tempStrlis[0].ljust(40,'-')))
        tempStr += tempStrlis[1].ljust(50,' ')
        print(len(tempStrlis[1].ljust(50,'-')))
        tempStr += tempStrlis[2].rjust(5,' ')
        print(len(tempStrlis[2].rjust(5,'-')))
        print(len(tempStr))
        print("-"*50)
        temp.append(tempStr)
    tSQL = ListProperty(temp)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    


class startApp(App):
    def build(self):
        self.title = 'Kugel Spiel'
        return myGridLayout()

class levelAuswahlApp(App):
    def build(self):
        self.title = 'Level'
        return myScrollView()




if __name__ == '__main__':
    # startApp().run()
    levelAuswahlApp().run()
    # print()
    pass
















import os
#Map Idee
def Map(x,y):
    map = "1"*x
    mapLesen = "1"*x + "\n"
    for i in range(y):
        map += "1"+ "0"*(x-2) + "1"
        mapLesen += "1"+ "0"*(x-2) + "1" + "\n"
    map += "1"*x
    mapLesen += "1"*x +"\n"
    return map, mapLesen

def aufbau(map, x, kugel="\033[92m#\033[0m"):
    for i in range(1,len(map)//x+1):
        temp = map[x*(i-1):x*i]
        if '#' in temp :
            print(temp.replace("#", kugel))
        else:
            print(temp)
    
def spiel(x, map):
    Kugel = None
    pos = x+1
    valid = ["a","s","d","w","aw","wa", "as", "sa", "sd","ds","dw","wd"]
    os.system('cls' if os.name == 'nt' else 'clear')
    mapLesen = map[:pos] + "#" + map[pos+1:]
    aufbau(mapLesen, x)
    while True:
        eingabe = input()
        if eingabe in valid:
            match eingabe:
                case "a":
                    pos -= 1
                case "s":
                    pos += x
                case "d":
                    pos += 1
                case "w":
                    pos -= x
                case "aw"|"wa":
                    pos -= x+1
                case "as"|"sa":
                    pos += x-1
                case "sd"|"ds":
                    pos += x+1
                case "dw"|"wd":
                    pos -= x-1
            if map[pos] == "1":
                print("duhduhduh")
                return
            elif map[pos] == "2":
                print("duhduhduh")
                return
            else:
                mapLesen = map[:pos] + "#" + map[pos+1:]
                os.system('cls' if os.name == 'nt' else 'clear')
                aufbau(mapLesen, x)
x=120
# map, mapLesen = Map(x, 20)
# # print(mapLesen)
# spiel(x, map)