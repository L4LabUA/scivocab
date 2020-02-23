from appJar import gui


def press():
    print("User:", app.entry("User"), "Part", app.entry("Participant"), "YY",
            app.entry("YY"), "MM", app.entry("MM"), "DD", app.entry("DD"))

with gui("Login Window", "400x200", bg='orange', font={'size': 18}) as app:
    app.label("Welcome to appJar", bg='blue', fg='orange')
    app.entry("User", label=True, focus=True)
    app.entry("Participant", label=True, secret=False)
    app.entry("YY", label=True)
    app.entry("MM", label=True)
    app.entry("DD", label=True)
    app.buttons(["Submit", "Cancel"], [press, app.stop])

def press(btn):
    print(btn)

app = gui("Breadth")

app.setFont(10)
app.setExpand("both")
app.setSticky("ew")

app.startLabelFrame("Breadth 1", 3, 2, 1)
app.addImageButton("Breadth 1, A", press, "b001_fp.gif", 1, 1)
app.addImageButton("Breadth 1, B", press, "b001_fs.gif", 1, 2)
app.addImageButton("Breadth 1, C", press, "b001_fx.gif", 2, 1)
app.addImageButton("Breadth 1, D", press, "b001_tw.gif", 2, 2)
app.addButton("FIRST", press, 0, 1)
app.addButton("PREV", press, 0, 2)
app.addButton("NEXT", press, 3, 1)
app.addButton("LAST", press, 3, 2)
app.stopLabelFrame()

app.go()
