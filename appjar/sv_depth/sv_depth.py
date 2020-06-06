
from appJar import gui

app=gui("Grid Demo")
app.setFont(20)
app.setExpand("both")
app.setSticky("nesw")
app.startLabelFrame("Breadth 1", 2, 2, 1)
app.addImage("Breadth 1, A", "b001_fp.gif", 0, 0)
app.addImage("Breadth 1, B", "b001_fs.gif", 0, 1)
app.addImage("Breadth 1, C", "b001_fx.gif", 1, 0)
app.addImage("Breadth 1, D", "b001_tw.gif", 1, 1)
app.stopLabelFrame()
app.go()