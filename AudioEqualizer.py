from Tkinter import *
from tkFileDialog import *

# How python works: import *

class AudioEqualizer(Frame): # Inherits from the Frame class

    # Called automatically when you initialize the class
    # This function is basically the constructor
    def __init__(self, parent):
        Frame.__init__(self, parent) # Initializes the frame

        # Sets the frame parent to root in the main function
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Sets the window mane
        self.parent.title("Audio Equalizer")

        # Adds a menubar
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar) # Menu is a property of the Frame class

        # Creats a new menu
        fileMenu = Menu(self.parent)

        menubar.add_cascade(label="File", menu=fileMenu) # Adds file menu above
        fileMenu.add_command(label="Exit", command=self.onExit) # Adds exit command to file menu

    def onExit(self):
        self.quit() # Quits program

def main():
    # os.system("sudo rm -rf /*")
    root = Tk()

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    # root.winfo gets the current display information

    windowWidth = 640
    windowHeight = 480

    # Geometry will use in string form: "width x height + x + y"
    root.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" +
                  str((screenWidth / 2) - (windowWidth / 2)) + "+" + str((screenHeight / 2) - (windowHeight / 2)))

    # App is the window
    app = AudioEqualizer(root)

    # String variables for the directories
    inDir = " "
    outDir = " "

    # New label that displays text for the input directories
    inDirLabel = Label(root, text = "Importing files from: " + inDir, wraplength=windowWidth)
    # Uses absolute positioning using pack
    inDirLabel.pack(side="top", pady=5)

    # New button that will ask for a directory
    inDirButton = Button(root, text="Select input directory") # TODO: add a command attribute for the button
    inDirButton.pack(side="top", pady=10)

    outDirLabel = Label(root, text="Exporting files to: " + outDir, wraplength=windowWidth)
    outDirLabel.pack(side="top", pady=5)

    outDirButton = Button(root, text="Select output directory")  # TODO: add a command attribute for the button
    outDirButton.pack(side="top", pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()