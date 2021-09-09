from FSMlib import FSM, State
import utils
#drautomata Command Line Interface



def mainMenu():
    mainmenuoption = ""
    while(True):
        print("Welcome to the Commandline Interface for the drautomata library, a python-based Automata Simulator")
        print("1: Stepwise creation of automata")
        print("2: Automata Simulation")
        print("3: Automata Operations")
        print("4: Automata Visualization")
        print("X: Quit")
        print("?: Help\n>\t")
        mainmenuoption = input()
        
        if (mainmenuoption == "?"):
            print("This is the command line interface for an automata simulation library developed by Dylan Reynolds\nthis tool allows you to create, simulate and visualize different types of finite state machines, if you have downloaded this tool from the GitHub repository, you should also have a folder containing a series of templates of different finite state machines, please try loading one of these templates for an idea on how finite state automata operate.")
            print("\n\n")
        if (mainmenuoption == "1"):
            AutomataCreator()
            mainmenuoption = ""
        if (mainmenuoption == "2"):
            AutomataSimulator()
            mainmenuoption = ""
        if (mainmenuoption == "3"):
            AutomataOperator()
            mainmenuoption = ""
        if (mainmenuoption == "4"):
            AutomataVisualizer()
            mainmenuoption = ""
        if (mainmenuoption == "X"):
            return

def AutomataCreator():
    utils.stepwiseInput()
    
def AutomataSimulator():
    menuoption = ""
    while(menuoption != "1" and menuoption != "2" and menuoption != "X"):
        print("Welcome to the automata simulator, here you can choose to process input strings on a previously generated automata")
        print("1: Process a single input string")
        print("2: Process multiple input strings")
        print("X: Quit to main menu\n>\t")
        menuoption = input()
        
        if menuoption == "1" or menuoption == "2":
            FSM = loadAutomata()
            if menuoption == "1":
                inputstring = input("Please enter the input string you wish to process, ensure that no leading spaces are present\n>\t")
                accepted = FSM.processString(inputstring)
                if(accepted):
                    print("\nInput:", inputstring, " Accepted!\n\n")
                    input("Please press <ENTER> to return to the main menu")
            if menuoption == "2":
                filepath = input("Please enter the filepath of the input string text file\n>\t")
                savepath = input("Please enter the filepath of the generated output file\n>\t")
                utils.processMultipleStrings(filepath, FSM, name=savepath, output=True)
                print("String processing complete, please see the output details in file:", savepath)
                input("Please press <ENTER> to return to the main menu")
        if menuoption == "X":
            return
            
def AutomataOperator():
    menuoption = ""
    while(menuoption != "1" and menuoption != "2" and menuoption != "3" and menuoption != "X"):
        print("Welcome to the automata operator, here you can perform operations on DFA, do note that other automata types are not supported for union and intersection operations")
        print("1: Union")
        print("2: Intersection")
        print("3: Complement")
        print("X: Quit to main menu")
        menuoption = input()
        if menuoption == "1" or menuoption == "2":
            filename= ""
            print("These operations require two automata to function, next you will be prompted for filepaths for both of these automata, please ensure they are both of the same type, and support the same input alphabet")
            FSM_1 = loadAutomata()        
            FSM_2 = loadAutomata()
            if menuoption == "1":
                FA = FSM_1.operation("UNION", FSM_2)
                print("\n\nNew Automata:")
                print(FA)
                
                while(filename == ""):
                    filename = input("Please enter the name of the file to save the created automata\n>\t")             
                FA.save(filename)
                
            if menuoption == "2":
                FA = FSM_1.operation("INTERSECTION", FSM_2)
                
                print(FA)                
                while(filename == ""):
                    filename = input("Please enter the name of the file to save the created automata\n>\t")             
                FA.save(filename)
                
        if menuoption == "3":
            FSM_1 = loadAutomata()
            FA = FSM_1.operation("COMPLEMENT")
            print(FA)
            
            while(filename == ""):
                filename = input("Please enter the name of the file to save the created automata\n>\t")             
            FA.save(filename)
            
        if menuoption == "X":
            return
            
            
def AutomataVisualizer():
    print("Welcome to the automata visualizer, here you can visualize your previously saved automata.")
    FSM = loadAutomata()
    if(FSM != -1):
        FSM.visualize()
    return
                
def loadAutomata():
    automataLoaded = -1
    FSM = None
    while automataLoaded == -1:
        filepath = input("Please enter the filename of the FSM you wish to load:\n>\t")
        try:
            f = open(filepath, "r")
            readerror=0
        except OSError:
            print("Could not open file:", filepath)
            readerror=1                 
        if(readerror == 0):
            contents = f.read() 
            FSM = utils.FSMDecode(contents) 
            if(FSM != -1):
                automataLoaded = 1
                print("Automata loaded")
        if(readerror == 1):
            automataLoaded = -1
    return FSM


if __name__ == "__main__":
    mainMenu()