
import sys
from appJar import gui

import settings
import menu_functions as menu



def setup():
    global app
    
    app = gui("Semantic Search 3000", "1350x850")

    app.setFont(16)
    
    ###  Frame 1 - Login / Main Menu  ###
    app.startPanedFrame("p1")
    app.addLabel("title", "Semantic Search 3000")
    app.setLabelPadding("title", 0, 12)
    app.setLabelBg("title", "yellow")

    ## Login / Main Menu Label
    #  - "l1" displays "Login" in our setup() function, but if
    #       you look below at the main_menu() function you can
    #       see how I changed the label to say "Main Menu."
    #  - Other labels and objects will need to change similar to this,
    #       like when users select different options from the main menu.
    app.addLabel("l1", "Login")
    app.setLabelPadding("l1", 0, 6)
    
    app.setLabelBg("l1", "white")
    app.setLabelWidth("l1", 8)

    app.addMessage("m1","")
    app.setMessageSticky("m1", "left")
    app.setMessageWidths("m1", 350)

    app.addLabelEntry("Username ")
    app.addLabelSecretEntry("Password ")
    app.setFocus("Username ")

    app.addButtons(["Login", "Cancel"], frame1_press)

    ###  Frame 2 - Explorer Window  ###
    app.startPanedFrameVertical("p2")
    app.addLabel("l2", "")
    app.setLabelPadding("l2", 0, 6)

    
    app.addListBox("doc_display", ["" for x in range(30)])
    app.disableListBox("doc_display")

    app.addValidationEntry("v1")
    app.disableEntry("v1")

    app.addDirectoryEntry("d1")
    app.disableDirectoryEntry("d1")

    app.addLabelOptionBox("View Text", ["" for x in range(51)])
    app.setOptionBoxWidth("View Text", 30)
    app.disableOptionBox("View Text")
    
    app.addButtons(["Search", "Select", "Text", "Return"], frame2_press)
    app.disableButton("Search")
    app.disableButton("Select")
    app.disableButton("Text")
    app.disableButton("Return")

    



    ###  Frame 3 - Console / Display  ###
    app.startPanedFrame("p3")
    app.addMessage("m3", "")
    app.setMessageWidth("m3", 600)
    app.setMessagePadding("m3", 0, 6)

    #app.addLabel("l4", "Document Information")

    app.addScrolledTextArea("t1")
    app.disableTextArea("t1")

   
    ## Closes Frame 3
    app.stopPanedFrame()
    ## Closes Frame 2
    app.stopPanedFrame()
    ## Closes Frame 1
    app.stopPanedFrame()

    return


    
    
def frame1_press(button):
    
    if button == "Cancel":
        app.stop()
        
    elif button == "Login":
        entry = app.getEntry("Username ")
                    
        if settings.login == False:
            pwd = app.getEntry("Password ")
            #print "user:", entry, ", pass:", pwd
            settings.user = entry
            settings.login = True
            #print settings.user
        
        if entry == "1":
            app.setEntry("Username ", "")
            app.enableListBox("doc_display")
            app.enableTextArea("t1")
            search()
        elif entry == "2":
            app.setEntry("Username ", "")
            select_documents()
        elif entry == "3":
            app.setEntry("Username ", "")
            upload_documents()
        elif entry == "4":
             app.stop()
        else:
            main_menu()


def frame2_press(button):
    
    if button == "Search":
        settings.query = app.getEntry("v1")
        #print settings.query

        ## Menu Function ##
        scores = menu.search(settings.query)
        
        app.setEntryValid("v1")
        app.enableOptionBox("View Text")
        app.enableButton("Select")
        app.enableButton("Text")
        app.enableTextArea("t1")

        names = []
        names.append("-"+settings.group+"-")

        if len(scores) > 50:
            x = 50
        else:
            x = len(scores)
            
        for i in range(x):
            app.setListItemAtPos("doc_display", i, "{:4} {} {} {}".format(str(i+1)+". ", str(scores[i][1]), "_"*(75-len(scores[i][1])), str(round(scores[i][2]*100, 1))))
            names.append(str(scores[i][1]))

        app.changeOptionBox("View Text", names)
        
    elif button == "Select":
        settings.path = app.getDirectoryEntryWidget("d1")
        print settings.path

    elif button == "Text":
        doc = app.getOptionBox("View Text")
        print doc

        app.setTextArea("t1", settings.doc_info[doc]['text'])
        
    elif button == "Return":
        main_menu()
    


def main_menu():
    
    app.openPanedFrame("p1")
    app.setLabel("l1", "Main Menu")
    app.setMessage("m1", "  1) Search\n\n  2) Select Documents\n\n  3) Upload Documents\n\n  4) exit")
    app.setLabel("Username ", "Select ")
    app.setEntry("Username ", "")
    app.setButton("Login", "Enter")
    app.hideEntry("Password ")

    app.setLabel("l2", "Explorer")
    #app.setLabelBg("l2", "DarkKhaki")
    app.setMessage("m3", "Console")
    #app.setMessageBg("m3", "DarkKhaki")


    ###  Disable  ###

    ## Frame 2 ##
    for i in range(50):
        app.setListItemAtPos("doc_display", i, "")
            
    app.disableListBox("doc_display")

    app.disableOptionBox("View Text")


    app.setEntry("v1", "")
    app.setEntryWaitingValidation("v1")
    app.disableEntry("v1")

    app.disableDirectoryEntry("d1")
    app.setEntry("d1", "")
    
    app.disableButton("Search")
    app.disableButton("Select")
    app.disableButton("Text")
    app.disableButton("Return")



    ## Frame 3 ##
    app.clearTextArea("t1")
    app.disableTextArea("t1")

    
    app.stopPanedFrame()



def search():

    app.setLabel("l1", "[ Search ]")

    app.enableEntry("v1")
    app.setEntryValid("v1")
    app.disableDirectoryEntry("d1")

    app.enableButton("Search")
    app.enableButton("Return")


    return


def select_documents():

    app.setLabel("l1", "[ Select Documents ]")
    app.enableDirectoryEntry("d1")

    app.enableButton("Select")
    app.enableButton("Return")


    
    return


def upload_documents():

    app.setLabel("l1", "[ Upload Documents ]")
    app.enableDirectoryEntry("d1")

    app.enableButton("Select")
    app.enableButton("Return")
    

    
    return


def launch(win):
    app.showSubWindow(win)

## Main Function ##
def run():
    
    setup()
    app.go()


if __name__ == '__main__':
    run()
