from json import JSONEncoder, loads
import FSMlib
import os.path

class FSMEncoder(JSONEncoder):
    def default(self, fsm):
        allStates = fsm.getAllStates()
        fsmDict = {}
        fsmDict['States'] = {}
        fsmDict['Type'] = fsm.FSMType
        fsmDict['Initial'] = fsm.initialState.identifier
        if(fsm.FSMType == "DFA"):
            for i in range(len(allStates)):
                   identifier = allStates[i].getIdentifier();
                   transitionChars = allStates[i].getChars();
                   transitionStates = allStates[i].getStates();
                   transitions = (list(zip(transitionChars, transitionStates)))                 
                   acceptingFlag = allStates[i].getAccepting();  
                   fsmDict['States'][identifier] = {"Transitions": transitions, "Accepting": acceptingFlag}
        if(fsm.FSMType == "2DFA"):
            for i in range(len(allStates)):
                   identifier = allStates[i].getIdentifier();
                   transitionChars = allStates[i].getChars();
                   transitionStates = allStates[i].getStates();
                   transitionDirections = allStates[i].getDirections();
                   transitions = (list(zip(transitionChars, transitionStates, transitionDirections)))                 
                   acceptingFlag = allStates[i].getAccepting();  
                   fsmDict['States'][identifier] = {"Transitions": transitions, "Accepting": acceptingFlag}
        return fsmDict
    
def FSMDecode(jsontxt):
    decoded = loads(jsontxt)
    allStates = []
    for key in decoded['States']:
        initial_id = decoded['Initial'] 
        #print(key, '->', decoded['States'][key]['Transitions'])
        #for i in range(len(decoded['States'][key]['Transitions'])):
        FSMAttributes = list(zip(*decoded['States'][key]['Transitions']))
        chars = FSMAttributes[0]
        states = FSMAttributes[1]
        accepting = decoded['States'][key]['Accepting']
        
        #print("Identifier:", key)
        #print("\nChars:", chars)
        #print("\nStates:", states)
        #print("\nAccepting:", accepting)
        
        if(decoded['Type'] == "2DFA"):
            direction = FSMAttributes[2]
            #print("\nDirection:", direction)    
            state = FSMlib.State(key, chars, states,direction, accepting)
            if(key == initial_id):
                initial_state = state
            allStates.append(state)
        
        elif(decoded['Type'] == "DFA"):
            state = FSMlib.State(key, chars, states, accepting=accepting)
            if(key == initial_id):
                initial_state = state
            allStates.append(state)
    
            
    DFA = FSMlib.FSM(decoded['Type'],initial_state, allStates)
    #res = list(zip(*decoded['States'][key]['Transitions'])) 
    #print("\nRES:\n",res)
    print("FSM Load successful.")
    print(DFA)
    return DFA
    
    

def writeToFile(filename, text=None, option=None):
        if option == "JSON":
            ext = ".json"
        if option == "Visualize":
            ext = ".tex"
        exists = checkExists(filename + ext)
        while(exists == True):
            print("File '" + filename + "' Already exists, what would you like to do?\n")
            print("O: Overwrite")
            print("N: Specify alternative filename")
            print("C: Cancel")
            option = input(">\t")
            print()
            if(option.upper() == "O"):
                exists = False
            if(option.upper() == "N"):
                filename = input("Please specify a new filename:\n>\t")
                exists = checkExists(filename + ext)
            if(option.upper() == "C"):
                print("Save cancelled")
                return -1
        f = open(str(filename) + ext, "w")
        f.write(text)
        f.close()
        if(checkExists(filename + ext) == True):
            print("File saved successfully: " + filename + ext)
        return 1

def checkExists(filename):
    return os.path.isfile(filename)