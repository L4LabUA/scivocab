# run app jar

from appJar import gui

# login window

def press(btn):
    if btn == "Submit":
        app.addLabel("submit", "Submitted")
        print("Breadth Login", "User:", app.entry("User"), "Part:",
              app.entry("Participant"), app.getDatePicker("date"))
        app.addButton("Continue", app.stop)

with gui('Breadth Login', sticky='esw', stretch='column') as app:

    app.setFont(14)
    app.setBg("orange")

    app.label("title", "Breadth Task Login", bg='blue', fg='orange', stretch='column', sticky='nesw')

    app.entry("User", label=True)
    app.entry("Participant", label=True, secret=False)
    app.addDatePicker("date")
    app.setDatePickerRange("date", 2020)
    app.setDatePicker("date")
    app.getDatePicker("date")
    app.buttons(["Submit"], [press])

    def press(btn):
        print(btn)

with gui('Breadth Task', sticky='esw', stretch='column') as app:

    app.startPagedWindow("")
    app.startPage("nesw")
    app.label("Breadth Task", bg='blue', fg='yellow', sticky='nesw', stretch='both', font={'size':20, 'family':'Helvetica'})
    app.stopPage()

    app.startPage("nesw")
    app.label("Item 1", bg='blue', fg='orange', row=0, column=1, colspan=2)
    app.label("tw goes here", row=1, column=1, colspan=2)
    app.addImageButton("Item 1: A", press, "b001_fp.gif", row=2, column=1)
    app.addImageButton("Item 1: B", press, "b001_fs.gif", row=2, column=2)
    app.addImageButton("Item 1: C", press, "b001_fx.gif", row=3, column=1)
    app.addImageButton("Item 1: D", press, "b001_tw.gif", row=3, column=2)
    app.stopPage()

    app.startPage("nesw")
    app.label("Item 2", bg='blue', fg='orange', row=0, column=1, colspan=2)
    app.label("tw goes here", row=1, column=1, colspan=2)
    app.addImageButton("Item 2: A", press, "b002_fp.gif", row=2, column=1)
    app.addImageButton("Item 2: B", press, "b002_fs.gif", row=2, column=2)
    app.addImageButton("Item 2: C", press, "b002_fx.gif", row=3, column=1)
    app.addImageButton("Item 2: D", press, "b002_tw.gif", row=3, column=2)
    app.stopPage()

    app.startPage("nesw")
    app.label("Item 3", bg='blue', fg='orange', row=0, column=1, colspan=2)
    app.label("tw goes here", row=1, column=1, colspan=2)
    app.addImageButton("Item 3: A", press, "b001_fp.gif", row=2, column=1)
    app.addImageButton("Item 3: B", press, "b001_fs.gif", row=2, column=2)
    app.addImageButton("Item 3: C", press, "b001_fx.gif", row=3, column=1)
    app.addImageButton("Item 4:, D", press, "b001_tw.gif", row=3, column=2)
    app.stopPage()

    app.startPage("nesw")
    app.label("Item 4", bg='blue', fg='orange', row=0, column=1, colspan=2)
    app.label("tw goes here", row=1, column=1, colspan=2)
    app.addImageButton("Item 4: A", press, "b001_fp.gif", row=2, column=1)
    app.addImageButton("Item 4: B", press, "b001_fs.gif", row=2, column=2)
    app.addImageButton("Item 4: C", press, "b001_fx.gif", row=3, column=1)
    app.addImageButton("Item 4: D", press, "b001_tw.gif", row=3, column=2)
    app.stopPage()
    app.stopPagedWindow()