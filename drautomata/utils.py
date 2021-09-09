from json import JSONEncoder, loads
from more_itertools import distinct_permutations
import FSMlib
import os.path
import sys
import time

#Save to file, uses normal JSONEncoder library for clarity.
class FSMEncoder(JSONEncoder):
    def default(self, fsm):
        allStates = fsm.getAllStates()
        fsmDict = {}
        fsmDict['States'] = {}
        fsmDict['Type'] = fsm.FSMType
        fsmDict['Initial'] = fsm.initialState.identifier
        if(fsm.FSMType == "DFA" or fsm.FSMType == "NFA"):
            for i in range(len(allStates)):
                   identifier = allStates[i].getIdentifier();
                   transitionChars = allStates[i].getChars();
                   transitionStates = allStates[i].getStates();
                   transitions = (list(zip(transitionChars, transitionStates)))                 
                   acceptingFlag = allStates[i].getAccepting();  
                   fsmDict['States'][identifier] = {"Transitions": transitions, "Accepting": acceptingFlag}
        if(fsm.FSMType == "2DFA" or fsm.FSMType == "2NFA"):
            for i in range(len(allStates)):
                   identifier = allStates[i].getIdentifier();
                   transitionChars = allStates[i].getChars();
                   transitionStates = allStates[i].getStates();
                   transitionDirections = allStates[i].getDirections();
                   transitions = (list(zip(transitionChars, transitionStates, transitionDirections)))                 
                   acceptingFlag = allStates[i].getAccepting();  
                   fsmDict['States'][identifier] = {"Transitions": transitions, "Accepting": acceptingFlag}
        return fsmDict

#Load from file
def FSMDecode(jsontxt):
    decoded = loads(jsontxt)
    allStates = []
    for key in decoded['States']:
        initial_id = decoded['Initial'] 
        FSMAttributes = list(zip(*decoded['States'][key]['Transitions']))
        chars = FSMAttributes[0]
        states = FSMAttributes[1]
        accepting = decoded['States'][key]['Accepting']
      
        if(decoded['Type'] == "2DFA" or decoded['Type'] == "2NFA"):
            direction = FSMAttributes[2]
            state = FSMlib.State(key, chars, states,direction, accepting)
            if(key == initial_id):
                initial_state = state
            allStates.append(state)
        
        elif(decoded['Type'] == "DFA" or decoded['Type'] == "NFA"):
            state = FSMlib.State(key, chars, states, accepting=accepting)
            if(key == initial_id):
                initial_state = state
            allStates.append(state)
    
    #If no states are defined
    if(len(allStates) == 0):
        print("States load error")
        return -1     
    
    #If type is unrecognised
    if (decoded['Type'] != "DFA" and decoded['Type'] != "2DFA" and decoded['Type'] != "NFA" and decoded['Type'] != "2NFA"): 
        print("FSM type error")
        return -1
    
    FSM = FSMlib.FSM(decoded['Type'],initial_state, allStates)

    print("FSM Load successful.")
    print(FSM)
    return FSM

#Process from text file    
def processMultipleStrings(filename, FSM, name="", output=False, rtn=False):
    acceptedIndices = []
    acceptedCount = 0
    outputContent = "inputstring, statesVisited, stateCount, timetaken,transitionsmade,sizeInMemory\n"
    rtnContent= "inputstring, statesVisited, stateCount, timetaken,transitionsmade,sizeInMemory\n"
    
    f = open(filename, "r") 
    lines = f.readlines()
    for i in range(len(lines)):
        inputString = lines[i].strip()
        starttime = time.time()
        accepted, statesVisited, transitionsmade = FSM.processString(inputString)
        endtime = time.time()
        timetaken = endtime-starttime
        if(accepted):
            acceptedCount += 1
            acceptedIndices.append(i)
        if(rtn):
            rtnContent += inputString + "," + str(len(statesVisited)) + "," + str(len(FSM.allStates)) + "," + str(timetaken) + "," +  str(transitionsmade) + "," + str(sys.getsizeof(FSM)+sys.getsizeof(inputString)) + "\n"
        if(output):
            outputContent += inputString + "," + str(len(statesVisited)) + "," + str(len(FSM.allStates)) + "," + str(timetaken) + "," +  str(transitionsmade) + "," + str(sys.getsizeof(FSM)+sys.getsizeof(inputString)) + "\n"
      
    if(output):
        #Save to file
        outputFilename = str(name)
        writeToFile(outputFilename, outputContent, "Results")   
        
        
    if(rtn):
        #Return from function
        return acceptedCount, acceptedIndices, rtnContent
    
    return acceptedCount, acceptedIndices
    
def stepwiseInput():
    #Step-wise creation of automata
    inputAlphabet = ""
    FSMType = ""
    
       
    states = {}
    pending_states = []
    directions = None
    
        
    
    #Should a different symbol be used here? why not vdash/dashv for endmarkers?
    inputAlphabet = input("Please enter the input alphabet, with characters separated by a vertical bar \"|\" \nNOTE: '<' and '>' are reserved for 2DFA end-markers \n>\t")
    arrAlphabet = inputAlphabet.split('|')
    arrAlphabet.sort()
    
    
    while(FSMType != 'DFA' and FSMType != '2DFA' and FSMType != 'NFA' and FSMType != "2NFA"):
        FSMType = input("Please enter the FSM type:\nCurrently Supported Types: 'DFA', '2DFA', 'NFA', '2NFA'\n>\t")
        
    
    if(FSMType == '2DFA' or FSMType=='2NFA'):
        #Add the end markers as part of the input alphabet
        
        #Rotating/Sweeping Automata - https://link.springer.com/chapter/10.1007%2F978-3-540-85780-8_36
        print("Please enter the Two-way FA restriction mode:")
        print("0: None")
        print("1: Rotating")
        print("2: Sweeping")
        _2dfa_restriction = input()
        
        arrAlphabet.insert(0,"<")
        arrAlphabet.append(">")
        directions = []
        
    
    state_id = input("Please enter the identifier for the starting state (q0)\n>\t")
    
    acceptingInput = ""
    while(acceptingInput.upper() != 'Y' and acceptingInput.upper() != 'N'):
        acceptingInput = input("Is this state an accepting state? (Y/N)\n>\t")
    if(acceptingInput.upper() == 'Y'):
        accepting=True
    elif(acceptingInput.upper() == 'N'):
        accepting=False
    
    initial_state = FSMlib.State(state_id, [], [], directions, accepting)
    states[state_id] = initial_state
    pending_states.append(state_id)
    
    
    
    
    while(pending_states):
        currentState = pending_states[0]
        directions = []
        symbolIndex=0
        
        print()
        print("--- Transition information ---")
        for key in states.keys():
            print("State:",key)
            for i in range(len(states[key].getStates())):
                print("Upon receiving", states[key].getChars()[i], "transition into state", states[key].getStates()[i])
            if(len(states[key].getStates()) == 0):
                print("No transitions defined yet\n")
    
        #For all symbols in alphabet
        while symbolIndex in range(len(arrAlphabet)):
                symbol = arrAlphabet[symbolIndex]
                transitionType = ""
                
                #Should it connect to an existing state or new state?
                while(transitionType.upper() != "N" and transitionType.upper() != "E"):
                    print("Where should state", currentState, "transition to, upon recieving symbol:", symbol)
                    print("N: New state")
                    print("E: Existing State")
                    transitionType = input(">\t")
                    
                #New State
                if(transitionType.upper() == 'N'):
                    new_state_id = input("Please enter the identifier for the new state:\n>\t")
                    acceptingInput = ""
                    while(acceptingInput.upper() != "Y" and acceptingInput.upper() != "N"):
                        acceptingInput = input("Is this state an accepting state? (Y/N)\n>\t")
                    if(acceptingInput.upper() == 'Y'):
                        accepting=True
                    elif(acceptingInput.upper() == 'N'):
                        accepting=False
                        
                    #Initialize a new state
                    newState = FSMlib.State(new_state_id, [], [], directions.copy(), accepting)
                    states[new_state_id] = newState                
                    
                    
                    #Set the transition state to be this new state
                    transition_state_id = new_state_id    
                    
                    #Add the state to the pending states list, so that transitions can be defined for it.
                    pending_states.append(new_state_id)
                
                #Existing State
                if(transitionType.upper() == 'E'):
                    print("Choose an existing state to transition to:")                
                    for key in states.keys():
                        print("State:",key)
                        for i in range(len(states[key].getStates())):
                            print("Upon receiving", states[key].getChars()[i], "transition into state", states[key].getStates()[i])
    
                        if(len(states[key].getStates()) == 0):
                            print("No transitions defined yet")
                    print()
                    while(existing_state_id not in states.keys()):
                        existing_state_id = input("\n>\t")
                    
                    
                    #Set the transition state to be this existing state
                    transition_state_id = existing_state_id
    
                    
                   
                #Add directions for 2DFA  
                if(FSMType == '2DFA' or FSMType == '2NFA'):
                    direction = ""
                    
                    #No restriction
                    if(_2dfa_restriction == "0"):
                        while(direction != 'L' and direction != 'R'):
                            direction = input("Upon transitioning, which direction should the read-head move (L/R)\n>\t")
                            direction = direction.upper()
                    
                    #Rotating 2DFA
                    if(_2dfa_restriction == "1"):      
                        if(symbol == ">"):
                            print("Rotating automata selected, upon reaching the right endmarker, the automata may return to the beginning of the string and scan again (L->R only)")
                            print("Upon reading the end marker in state", currentState, "should the system move back to the beginning of the input? (Y/N)(Rotate)\n")
                            choice = input(">\t")
                            if(choice.upper() == "Y"): direction = "ROTATE"
                            else: direction = "R"
                        else:
                            direction = "R"
                     
                    #Sweeping 2DFA
                    if(_2dfa_restriction == "2"):
                        if(symbol == "<" or symbol == ">"):
                            while(direction.upper() != 'L' and direction.upper() != 'R'):
                                direction = input("Upon transitioning, which direction should the read-head move (L/R)\n>\t")
                        else:
                            print("Sweeping automata selected, reversal is not possible on non-endmarker symbols, if this symbol (" + str(symbol) + ") is read whilst in State:", currentState, "traversal will continue in the same direction.")
                            direction = "C"
                  
                #If deterministic, only 1 transition per symbol is allowed.
                if(FSMType == 'DFA' or FSMType == '2DFA'):
                    symbolIndex+=1
                    
                #If non-deterministic, allow user to define more transitions for any given symbol.
                if(FSMType == 'NFA' or FSMType == '2NFA'):
                    option = ""
                    while option != "1" and option != "2":
                        print("Would you like to add an additional transition for symbol '" + symbol + "' ?")
                        print("1: Yes")
                        print("2: No")
                        option = input(">\t")
                        if option == "1": pass#Don't move to the next character
                        if option == "2": 
                            symbolIndex+=1 #Move to the next character
                            print("i is:",symbolIndex)
                
                if(FSMType == 'DFA' or FSMType == 'NFA'):
                    states[currentState].addTransition(symbol, transition_state_id)
                elif(FSMType == '2DFA' or FSMType == '2NFA'):
                    states[currentState].addTransition(symbol, transition_state_id, direction)
                          
        #Transitions defined, move on to next state      
        pending_states.remove(currentState)
    
    #Create a list of all states to add to the FSM
    allStates =  list(states.values())
    
    #Create the FSM
    FiniteStateMachine = FSMlib.FSM(FSMType ,allStates[0], allStates)
    
    print(FiniteStateMachine)
    filename = input("Please enter the FSM output filename\n>\t")
    FiniteStateMachine.save(filename);
             
        

                
#Print state info               
def printCurrentStates(states):
    for key in states.keys():
        print(key, ":", states[key])
 
    
def writeToFile(filename, text=None, option=None, mode="a"):  
    if option == "JSON":
        ext = ".json"
    elif option == "Visualize":
        ext = ".tex"
    elif option == "Results":
        ext = ".txt"
    else:
        ext = ""
     
    
    if(ext not in filename):
        filename += ext
        
    #Create new file
    if mode != "a":
        exists = checkExists(filename)
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
                #Make sure we check before we overwrite.
                exists = checkExists(filename)
            if(option.upper() == "C"):
                print("Save cancelled")
                return -1
        f = open(str(filename), mode)
        f.write(text)
        f.close()
        if(checkExists(filename) == True):
            print("File saved successfully: " + filename)
            
    #Append to existing, or create new if doesnt exist.
    else:
        f = open(str(filename), mode)
        f.write(text)
        f.close()
    return 1

def checkExists(filename):
    return os.path.isfile(filename)