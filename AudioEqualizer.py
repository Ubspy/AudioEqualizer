from Tkinter import *
from pydub import AudioSegment
from threading import Thread
import tkMessageBox
import tkFileDialog
import os

# How python works: import *

# TODO: Remove debug and formatting

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

        # Adds a menu bar
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar) # Menu is a property of the Frame class

        # Creates a new menu
        fileMenu = Menu(self.parent)

        menubar.add_cascade(label="File", menu=fileMenu) # Adds file menu above
        fileMenu.add_command(label="Exit", command=self.onExit) # Adds exit command to file menu

    def onExit(self):
        self.quit() # Quits program

class PublicVariables():
    inDir = ""
    outDir = ""
    programError = False


def main():
    # os.system("sudo rm -rf /*")
    root = Tk()

    def askInDirectory():
        # Sets inDir to whatever directory they choose from the window
        PublicVariables.inDir = tkFileDialog.askdirectory()
        # Changes the label
        inDirLabel.config(text="Importing files from: " + PublicVariables.inDir)

    def askOutDirectory():
        # Makes sure the function uses the outDir defined in main()
        PublicVariables.outDir
        # Sets outDir to whatever directory they choose from the window
        PublicVariables.outDir = tkFileDialog.askdirectory()
        # Changes the label
        outDirLabel.config(text="Exporting files to: " + PublicVariables.outDir)

    def equalizeAudio():
        if PublicVariables.programError:
            tkMessageBox.showerror("An error has occurred", "Unable to equalize audio, please resolve the error")

        else:
            audioLevels = []
            audioFiles = []

            def findAudioLevel():
                # Adds the current songs audio level to an array
                audioLevels.append(song.dBFS)

            def findAverageLevel():
                # Resets value for each time is has to do it
                averageAudioLevel = 0

                # Adds all decibel levels up
                for x in audioLevels:
                    averageAudioLevel += x

                # Divides them by total number of files
                return averageAudioLevel / len(audioLevels)

            def normalizeAudio(song):
                # Finds the difference for apply_gain to use
                dBDifference = song.dBFS - averageAudioLevel

                # Debug
                print("Difference: ", dBDifference)

                # Removes the difference from the audio level to set it to the average
                return song - dBDifference

            def exportFiles():
                # Exports the file into it's same name, but in the output location
                song.export(os.path.join(PublicVariables.outDir, file))

            # For loop that runs once for each file and folder in the grabbed directory
            for file in os.listdir(PublicVariables.inDir):
                # If the file it's checking isn't a folder, append the file to the array
                if os.path.isfile(os.path.join(PublicVariables.inDir, file)):
                    audioFiles.append(file)

            # Imports files to find the audio level
            for file in audioFiles:
                if os.path.splitext(file)[1] == ".mp3":
                    song = AudioSegment.from_file(os.path.join(PublicVariables.inDir, file), format="mp3")
                    findAudioLevel()

                elif os.path.splitext(file)[1] == ".wav":
                    song = AudioSegment.from_file(os.path.join(PublicVariables.inDir, file), format="wav")
                    findAudioLevel()

            # Debug
            print(audioLevels)

            # Finds average audio level
            print(findAverageLevel()) # Debug
            averageAudioLevel = findAverageLevel()

            # Normalizes audio files one at a time using the average level
            for file in audioFiles:
                if os.path.splitext(file)[1] == ".mp3":
                    song = AudioSegment.from_file(os.path.join(PublicVariables.inDir, file), format="mp3")
                    song = normalizeAudio(song)
                    print("After: ", song.dBFS) # Debug
                    exportFiles()

                elif os.path.splitext(file)[1] == ".wav":
                    song = AudioSegment.from_file(os.path.join(PublicVariables.inDir, file), format="wav")
                    song = normalizeAudio(song)
                    print("After: ", song.dBFS) # Debug
                    exportFiles()

    def checkForErrors():

        def checkSameDir():
            if PublicVariables.inDir == PublicVariables.outDir and PublicVariables.inDir != "":
                errorLabel.config(text="Can't use the same input and output directories")
                PublicVariables.programError = True
            else:
                errorLabel.config(text="")
                PublicVariables.programError = False

        while True:
            checkSameDir()

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

    # New label that displays text for the input directories
    inDirLabel = Label(root, text = "Importing files from: ", wraplength=windowWidth)
    # Uses absolute positioning using pack
    inDirLabel.pack(side="top", pady=5)

    # New button that will ask for a directory
    inDirButton = Button(root, text="Select input directory", command=askInDirectory)
    inDirButton.pack(side="top", pady=5)

    outDirLabel = Label(root, text="Exporting files to: ", wraplength=windowWidth)
    outDirLabel.pack(side="top", pady=5)

    outDirButton = Button(root, text="Select output directory", command=askOutDirectory)
    outDirButton.pack(side="top", pady=5)

    equalizebutton = Button(root, text="Equalize Audio", command=equalizeAudio)
    equalizebutton.pack(side="bottom", pady=15)

    # fg changes the color to red
    errorLabel = Label(text="", fg="red", wraplength=(windowWidth / 3))
    errorLabel.pack(side="bottom", pady=0)

    # Starts a thread for the while true loop
    errorThread = Thread(name="error_check", target=checkForErrors)
    # Runs the thread in the background
    errorThread.daemon = True
    # Starts the thread
    errorThread.start()

    root.mainloop()

if __name__ == '__main__':
    main()