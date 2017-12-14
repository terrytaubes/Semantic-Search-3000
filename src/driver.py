# coding: utf-8

"""
Application Driver
"""

import settings
import menu_functions as menu
import gui


"""
main():

This is the main function of the application that initializes the program
   and runs the GUI and backend menu options of the app.

param:      n/a
return:     n/a
"""
def main():
    

    ###  Create Global Variables ###
    settings.init()

    ###  Command Line Menu  ###
    #menu.run()

    ###  GUI Run  ###
    gui.run()

    


if __name__ == "__main__":
    main()
