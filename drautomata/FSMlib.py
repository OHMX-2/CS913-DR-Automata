import utils     
from copy import deepcopy
      
class FSM:
    def __init__(self, FSMType, initialState, allStates):
        self.FSMType = FSMType
        self.initialState = initialState
        self.currentState = initialState
        self.allStates = allStates
        
    def getFSMType(self):
        return self.FSMType
    
    def getInitialState(self):
        return self.initialState
    
    def getCurrentState(self):
        return self.currentState
    
    def getAllStates(self):
        return self.allStates
    
    def setInitialState(self, state):
        self.initialState = state
        
    def setCurrentState(self, state):
        self.currentState = state
        
    def setAllStates(self, states):
        self.allStates = states
    
    def find(self,newstate_code):
        for state in self.allStates:
            if(state.getIdentifier() == newstate_code):
                return state
                      
    def addState(self, state):
        states = self.getAllStates()
        states.append(state)
        self.setAllStates(states)
        
    def removeState(self, state):
        states = self.getAllStates()
        states.remove(state)
        self.setAllStates(states)
            
    def __str__(self):
        output = self.FSMType
        output += "\nInitial:" + str(self.initialState.getIdentifier())
        output += "\nallStates:" 
        
        for state in self.allStates:
            output += "\n" + str(state.getIdentifier()) + ":" + str(state.getChars()) + "," + str(state.getStates()) + "," + str(state.getDirections()) + "," + str(state.getAccepting()) 
        return output
    

    def processString(self, inputstring, debug=False, stepmode=False, limit=1000):
        
        validAlphabet = self.getAlphabet()

        #Check that all characters in the input string are valid, if not, dont process the input. (It will be rejecting anyway!)
        for char in inputstring:
            if char not in validAlphabet:
                print("Input string contains an unsupported symbol for this FSM, input rejected.")
                return False
        statesVisited = [self.initialState.identifier]
        iters = 0
        inputAccepted = False
        if (stepmode): 
            debug=True #Set debug to true, so that the user can see what is happening
            input("Press return to begin the FSM")
            
        #2DFA
        if(self.FSMType == "2DFA"):
            i=0
            #Terminates the process if an iteration limit is reached.
            if (iters > limit):
                print("Max iteration limit (" + limit + ") reached, input rejected.")
                return False
            while i < len(inputstring):
                if (debug): print("\nCurrent state: " + self.currentState.identifier)
                if (debug): print("Processing index: " + str(i))
                if (debug): print("Current Symbol: " + str(inputstring[i]))
                if(i>0): lastDirection = direction
                newstate_code, direction = self.currentState.process(inputstring[i])
                if(newstate_code not in statesVisited):
                    statesVisited.append(newstate_code)
                if (debug): print("Transitioning to: " + newstate_code + " with direction: " + direction)
                newstate = self.find(newstate_code)  
                if newstate is not None:
                    self.currentState = newstate
                else:
                    #No state found in state table
                    if (debug): print("No state found for code: " + newstate_code + " moving RIGHT and continuing in same state")
                #Continues in the same direction, used in Sweeping 2DFA
                if (direction=="C"):
                    direction = lastDirection
                    if(debug): print("Automata continuing in previous transition direction:", direction)
                #Returns to the beginning of the input string, used in Rotating 2DFA
                if (direction=="ROTATE"):
                    i = 0
                    if(debug): print("Index reset to 0 (rotate at endmarker)")
                #Left
                if (direction=="L"):
                    i-=1
                    if (debug): print("Index-1 (LEFT), now at index: " + str(i) + "/" + str(len(inputstring)))
                #Right
                else:
                    i+=1#Even if no direction is given (no transition to state) then move right to progress.
                    if (debug): print("Index+1 (RIGHT), now at index: " + str(i) + "/" + str(len(inputstring)))
                if (stepmode): input("Press return to proceed to the next step")
                iters += 1
            if(self.currentState.getAccepting() == True):
                inputAccepted=True
                

        #2NFA
        if(self.FSMType == "2NFA"):
            initialPath = (self.initialState.identifier, 0)
            currentPaths = []
            currentPaths.append(initialPath)
            inputAccepted = False
            
            while(currentPaths):
                stateID = currentPaths[0][0]
                state = self.find(stateID)
                currentCharIndex = currentPaths[0][1]
                nextCharIndex = currentCharIndex
                

                
                if (iters > limit):
                    print("Max iteration limit (" + limit + ") reached, input rejected.")
                    return False
                
                transitions = state.nfa_process(inputstring[currentCharIndex])
                
                currentTransition = transitions[0]
                
                
                if len(transitions) > 1:
                    for i in range(1,len(transitions)):
                        #Add all other potential paths
                        state= transitions[i][0]
                        direction = transitions[i][1]
                        if(direction == "L"):
                            charIndex = currentCharIndex-1
                        if(direction == "R"):
                            charIndex = currentCharIndex+1
                        if(direction == "ROTATE"):
                            charIndex = 0
                            
                        for path in currentPaths:
                            if path != (state,charIndex):                             
                                currentPaths.append((state,charIndex))
                
                transitionStateID = currentTransition[0]
                if(transitionStateID not in statesVisited):
                    statesVisited.append(transitionStateID)
                currentDirection = currentTransition[1]
                if(currentDirection == "L"):
                    nextCharIndex = currentCharIndex-1
                if(currentDirection == "R"):
                    nextCharIndex = currentCharIndex+1
                if(currentDirection == "ROTATE"):
                    nextCharIndex = 0
                
                transitionState = self.find(transitionStateID)
                if(transitionState.accepting and inputstring[currentCharIndex]==">" and currentDirection=="R"):
                    currentPaths = []
                    inputAccepted=True
                elif(currentCharIndex > len(inputstring) or (inputstring[currentCharIndex]==">" and currentDirection=="R")):
                     #Path has ended
                     currentPaths.remove(currentPaths[0])
                else:
                    currentPaths[0] = (transitionStateID, nextCharIndex)
                iters += 1
                
        #DFA
        elif(self.FSMType == "DFA"):
            for char in inputstring:
                if (debug): print("Current Symbol: " + char)
                newstate_code, direction = self.currentState.process(char)
                if(newstate_code not in statesVisited):
                    statesVisited.append(newstate_code)
                if (debug): print("Transitioning to: " + newstate_code)
                newstate = self.find(newstate_code) 
                #If no state is specified in the transition, stay in the same state
                if newstate is not None:
                    self.currentState = newstate
                else:
                    if (debug): print("No state found for code: " + newstate_code + " continuing in same state")
                if (stepmode): input("Press return to proceed to the next step")
                iters += 1
            if(self.currentState.getAccepting() == True):
                inputAccepted=True
                
        #NFA
        elif(self.FSMType == "NFA"):
            currentStates = []
            #Maintain a list of active paths, and what state(s) we are in at any given time
            currentStates.append(self.getInitialState())
            
            for char in inputstring:
                if (debug): print("Current Symbol: " + char)
                nextStates = []
                #Find the next transition on all paths
                for state in currentStates:
                    stateIdentifiers = state.nfa_process(char)
                    for ID in stateIdentifiers:
                        if(ID not in statesVisited):
                            statesVisited.append(ID)
                        nextState = self.find(ID)
                        if nextState not in nextStates: 
                            nextStates.append(nextState) 
                    iters += 1
                currentStates = nextStates
            for state in currentStates:
                self.setCurrentState(state)
                #If any states are accepting at the end of the input, then the input is accepting
                if self.currentState.getAccepting() == True:
                    inputAccepted=True

                      
        print("Total iterations:" + str(iters))
        print("States Visited:", len(statesVisited), "/", len(self.allStates))
        return inputAccepted, statesVisited, iters
        
    def save(self,filename):
        text = utils.FSMEncoder().encode(self)
        utils.writeToFile(filename, text=text, option="JSON")
    
    #Check that an FSM contains at least 1 accepting state, and that all states have atleast one outgoing transition
    def validate(self):
        accepting_state_count = 0
        missingTransitions = []
        missingTransition = False
        for state in self.allStates:
            if len(state.states) < 1:
                missingTransitions.append(state.identifier)
                missingTransition = True
            accepting_state_count += state.accepting
            
        if accepting_state_count < 1:
            print("FSM does not contain an accepting state")
        if missingTransitions:
            print("FSM has missing transitions for state IDs:")
            print(missingTransitions)
        
    #Remove exact duplicate states.
    def removeDuplicates(self):
        statesToCompare = self.getAllStates()
        for state1 in statesToCompare:
            for state2 in statesToCompare:
                if state1 != state2:
                    if state1.identifier == state2.identifier and state1.chars == state2.chars and state1.states == state2.states and state1.accepting == state2.accepting:
                        self.removeState(state2)
        return self
    
    #Get all supported characters across all states in the FSM                
    def getAlphabet(self):
       alphabet = []
       
       for state in self.allStates:
           for symbol in state.chars:
               if symbol not in alphabet:
                   alphabet.append(symbol)                  
       return alphabet
   
    #Automata Visualization - Not all combinations have been tested, it is likely tweaks in LaTeX are required for the desired output
    def visualize(self):
        distanceChosen = False
        distance = ""
        scaleChosen = False
        scale = 1
        arrowChosen = False
        arrowstyle = ""
        option = ""
        
        #Customization
        while(not distanceChosen):
            print("please specify the distance between nodes in centimeters (min: 0, max: 10, default: 3.5)")
            distanceChoice = input(">\t")           
            try:
                distance = float(distanceChoice)
            except ValueError:
                pass
            if(distance > 0 and distance <= 10): distanceChosen = True
                
                
        while(not arrowChosen):
            print("please specify a custom arrow style (default: 15 (Stealth)")
            print("Press ? to see options")  
            
            option = input(">\t")
            #Open help menu
            if (option == "?"):
                menuOption = ""
                while(menuOption != "G" and menuOption != "B" and menuOption != "M"):
                    print("B: Show barbed-type arrow heads")
                    print("G: Show geometric-type arrow heads")
                    print("M: Show mathematical-type arrow heads")
                    menuOption = input(">\t")     
                    menuOption = menuOption.upper()
                #Barb-type arrow heads
                if(menuOption == "B"):
                    print("1: Arc Barb[] - Half-circle barb")
                    print("2: Bar[] - Vertical bar barb '-|'")
                    print("3: Bracket[] - Right-bracket barb '-]'")
                    print("4: Hooks[] - double-hooked barb '-3'")
                    print("5: Parenthesis[] - Right-parenthesis barb '-)'")
                    print("6: Straight Barb[] - arrow-like straight barbs '->'")
                    print("7: Tee Barb[] - I-beam barb '-I'")
                #Geometric arrow heads
                if(menuOption == "G"):
                    print("8: Circle[] - Circular")
                    print("9: Diamond[] - Diamond Shaped")
                    print("10: Ellipse[] - Elliptical")
                    print("11: Kite[] - Kite shaped")
                    print("12: Latex[] - Latex default arrow, pointed tips")
                    print("13: Rectangle[] - Rectangular")
                    print("14: Square[] - Square shaped")
                    print("15: Stealth[] - Stealth bomber shaped, pointed tips")
                    print("16: Triangle[] - Triangular")
                    print("17: Turned Square[] - 45 degree turned square")
                #Mathematical arrowheads
                if(menuOption == "M"):
                    print("18: Classical TikZ Rightarrow[]")
                    print("19: Computer Modern Rightarrow[]")
                    print("20: Implies[] - double line")
                option = input(">\t")
            
            
                    
            #Resolve option
            try:
                intOption = int(option)
            except ValueError:
                pass
            if(intOption == 1): arrowstyle = "Arc Barb"
            if(intOption == 2): arrowstyle = "Bar"
            if(intOption == 3): arrowstyle = "Bracket"
            if(intOption == 4): arrowstyle = "Hooks"
            if(intOption == 5): arrowstyle = "Parenthesis"
            if(intOption == 6): arrowstyle = "Straight Barb"
            if(intOption == 7): arrowstyle = "Tee Barb"
            if(intOption == 8): arrowstyle = "Circle"
            if(intOption == 9): arrowstyle = "Diamond"
            if(intOption == 10): arrowstyle = "Ellipse"
            if(intOption == 11): arrowstyle = "Kite"
            if(intOption == 12): arrowstyle = "Latex"
            if(intOption == 13): arrowstyle = "Rectangle"
            if(intOption == 14): arrowstyle = "Square"
            if(intOption == 15): arrowstyle = "stealth"
            if(intOption == 16): arrowstyle = "Triangle"
            if(intOption == 17): arrowstyle = "Turned Square"
            if(intOption == 18): arrowstyle = "Classical TikZ Rightarrow"
            if(intOption == 19): arrowstyle = "Computer Modern Rightarrow"
            if(intOption == 20): arrowstyle = "Implies"
            
            if(arrowstyle != ""): arrowChosen = True

        while(not scaleChosen):
            print("please specify the scale of the FSM image (default: 1 (must be greater than 0))")
            scaleChoice = input(">\t")           
            try:
                scale = int(scaleChoice)
            except ValueError:
                pass
            if(scale > 0): scaleChosen = True
        
        fileString = "\\begin{tikzpicture}[->,>="
        fileString += arrowstyle
        fileString += ",shorten >=1pt,auto,node distance="
        fileString += str(distance)
        fileString += "cm,scale = "
        fileString += str(scale)
        fileString += ",transform shape]"
        fileString += "\n"
        stateCount = 0
        index = 0
        nodeString = ""
        
        stateEdges = []
        stateEdgeLabels = []
        edgeStateIDs = []
        connectedDirection = []
        connectedState_ID = ""
        connectedState_IDs = []
        edgeLabels = []
        edgeDirection = ""
        edgeDirections = []
        totalEdges = 0
        allConnections = {}
        
        pathString = "\path "
        
        
        #Define edges
        for y in range(len(self.allStates)):
            state = self.allStates[y]
            stateConnectionDict = {}            
            connectedStates = {}
            edgeLabels = []
            edgeLabel = ""
            for i in range(len(state.states)):            
                isConnected = (state.states[i] in connectedStates.keys()) 
                if(isConnected and (self.FSMType == "2DFA" or self.FSMType == "2NFA")):
                    isSameDirection = (state.directions[i] in connectedStates[state.states[i]])
                    direction = state.directions[i] 
                elif(isConnected and (self.FSMType != "2DFA" or self.FSMType != "2NFA")):
                    isSameDirection = True
                
                #Attempt to resolve overlapping connections - this only works if two states connect to eachother, overlaps are still entirely possible.
                #Please review and tweak TikZ code before use
                if(isConnected and isSameDirection):              
                    if(self.FSMType == "2DFA" or self.FSMType == "2NFA"): 
                        stateConnectionDict[(state.states[i]+"|"+state.directions[i])] += "," + state.chars[i]
                    else:
                        stateConnectionDict[state.states[i]] += "," + state.chars[i]
                else:
                    if(self.FSMType == "2DFA" or self.FSMType == "2NFA"):
                        stateConnectionDict[(state.states[i]+"|"+state.directions[i])] = state.chars[i]
                        connectedStates[state.states[i]] = [state.directions[i]]
                    else:
                        stateConnectionDict[state.states[i]] = state.chars[i]
                        connectedStates[state.states[i]] = True
                
                if(self.FSMType == "2DFA" or self.FSMType == "2NFA"):
                    edgeDirection = (": " + state.directions[i])  
                
                edgeLabels = list(stateConnectionDict.values())
                allConnections[state.identifier] = state.states

            edgesToAdd = len(stateConnectionDict)
            edges = list(stateConnectionDict.keys())
            for i in range(edgesToAdd):
                if(self.FSMType == "2DFA" or self.FSMType == "2NFA"):
                    pipeIndex = edges[i].index("|")
                    stateID = edges[i][0:pipeIndex]
                    direction = edges[i][pipeIndex+1:]
                else: stateID = edges[i]
                modifier = ""
                if(stateID == state.identifier):
                    #If it connects to itself, then create a looped arc
                    modifier = "[loop above]"
                elif(stateID in allConnections.keys()):
                    if(state.identifier in allConnections[stateID]):
                        modifier = "[bend left]"
                pathString += "(" + state.identifier + ")\t"
                pathString += "edge" + "\t" + modifier + "\t" + "node{$" 
                pathString += edgeLabels[i]
                if(self.FSMType == "2DFA" or self.FSMType == "2NFA"): pathString += ": " + direction
                pathString += "$} " + "(" + stateID + ")\n"
        pathString += ";"
        
        #Define nodes and positioning
        for y in range(len(self.allStates)):
            
            state = self.allStates[y]
            nodeString += "\\node[state"
            
            if state == self.initialState:
                nodeString +=  ",initial"
            if state.accepting == True:
                nodeString += ",accepting"
            if y==0: position = ""
            #Always move the next node to the right. Will result in a long line of states, manual tweaks required.
            else: position = "[right of=" + str((self.allStates[y-1].identifier)) + "]"
            nodeString += "] "+ position + "(" + state.identifier + ") {$" + state.identifier + "$};\n"
        
        
        fileString += nodeString + pathString + "\end{tikzpicture}"

        filename = input("Please enter the TikZ output filename\n>\t")

        utils.writeToFile(filename, fileString, "Visualize")
        return  
    
    #NFA to DFA conversion. Standard Scott-Rabin Powerset Construction method.
    def nfa_to_dfa(self):
        if self.FSMType != "NFA":
            print("This automata is not a one-way non-deterministic automaton. This function converts NFA to DFA only.")
            pass
        
        #For clarity
        NFA = self
        
        unresolvedStates = {}
        #List all chars in all states
        chars = self.initialState.getChars()
        initial = State(self.initialState.identifier, chars=[], states=[], directions=None, accepting=self.initialState.accepting)
        
        #Get a unique list of symbols the NFA accepts
        arrAlphabet = list(dict.fromkeys(chars).keys())
        
        
        #Create and empty DFA and add the initial state
        DFA = FSM("DFA", None, [])
        DFA.setInitialState(initial)
        DFA.setCurrentState(initial)
        DFA.addState(initial)
         
        #Resolve initial state + transitions
        for char in (arrAlphabet):
            acceptingState=False
            states = self.initialState.getResultStateByChar(char)
            identifier = ""
            uniqueStates = list(dict.fromkeys(states))
            uniqueStates.sort()
            for ndState in uniqueStates:
                if(NFA.find(ndState).getAccepting()):
                    acceptingState = True
                identifier += ndState 
            unresolvedStates[identifier] = states
            initial.addTransition(char, identifier)
            #NFA.find(identifier)
            newState = State(identifier, chars = [], states = [], accepting = acceptingState, directions=None)                                                      
            DFA.addState(newState)
            

        
        #All other states + transitions
        for state in DFA.allStates:
            #That are not the initial state
            if state is not DFA.initialState:
                #Resolve transition
                for char in (arrAlphabet): 
                    
                    states = []
                    #Find all potential state transitions in the original NFA
                    for stateID in unresolvedStates[state.identifier]:  
                        result = self.find(stateID)
                        resultState = result.getResultStateByChar(char)
                        
                        #If the result state is already in the list, don't add it again (avoids duplicate and "double" states (i.e. q0q0))
                        if(list(set(states).intersection(resultState)) != resultState):
                            #Add the state to the state to the DFA states list
                            states.extend(resultState)
                            
                    
                    #Link to an existing, or create a new state based on the union of all potential state transitions
                    identifier = ""
                    acceptingState=False
                    uniqueStates = list(dict.fromkeys(states))
                    uniqueStates.sort()
                    for ndState in uniqueStates:
                        #Check if any of the "sub-states" in the previous NFA were accepting, i.e. in q0q1, check both q0 and q1
                        if(NFA.find(ndState).getAccepting()):
                            acceptingState = True
                        identifier += ndState
                    if identifier not in unresolvedStates.keys() and identifier != DFA.initialState.identifier:
                        unresolvedStates[identifier] = states
                        newState = State(identifier, chars = [], states = [], accepting = acceptingState, directions=None)
                        DFA.addState(newState)
                    state.addTransition(char, identifier)
                    
        #Remove exact duplicates, for security, the algorithm should not allow duplicates anyway.            
        DFA = DFA.removeDuplicates()
       
        return DFA                                                                 

    #Union of automata requires a product construction of the state tables of both individual automata
    def operation(self, oper, automata=None):
        if (oper == "COMPLEMENT" and automata == None):
            newStates = []
            for state in self.allStates:                
                identifier = state.getIdentifier()
                chars = state.getChars()
                states = state.getStates()
                accepting = (not(state.getAccepting()))
                newState = State(identifier, chars=chars, states=states, accepting=accepting)
                newStates.append(newState)
            initialState = newStates[0]
            DFA = FSM(self.FSMType, initialState, newStates)
            return DFA
        #Check if FSMs are of the same type
        elif(self.FSMType != automata.FSMType and automata != None):
            print("FSMs are not of the same type: " + self.FSMType + " != " + automata.FSMType)
            return -1   
        #Check for same alphabet
        elif(sorted(self.getAlphabet()) != sorted(automata.getAlphabet()) and automata != None):
            print("FSMs use different alphabets")
            return -1   
        elif(self.FSMType != "DFA"):
            print("Only one-way deterministic finite automata are currently supported for this operation")
            return -1
        
        else:
            newStates = []

            for state1 in self.allStates:
                for state2 in automata.allStates:
                    
                    states = []
                    identifier = state1.getIdentifier() + state2.getIdentifier()
                    #Merge character sets.
                    chars = list(set(state1.getChars()) | set(state2.getChars()))
                    chars.sort()
                    for i in range(len(chars)):
                        states.append((state1.states[i]+state2.states[i]))
                    if (oper.upper() == "UNION"):
                        #If either is accepting, then mark as accepting
                        if(state1.getAccepting() == True or state2.getAccepting() == True):
                            #print(identifier, " - is accepting")
                            accepting = True
                        else:
                            accepting = False
                    elif (oper.upper() == "INTERSECTION"):
                        #If both are accepting, then mark as accepting
                        if(state1.getAccepting() == True and state2.getAccepting() == True):
                            #print(identifier, " - is accepting")
                            accepting = True
                        else:
                            accepting = False
                    productState = State(identifier, chars=chars, states=states, accepting=accepting)
                    newStates.append(productState)
            initialState = newStates[0]
            FA = FSM(self.FSMType, initialState, newStates)
            return FA
        


class State:
    def __init__(self, identifier, chars=None, states=None, directions = None, accepting = False):
        self.identifier = identifier
        self.chars = chars
        self.states = states
        self.directions = directions
        self.accepting = accepting
        
        
        
    def getIdentifier(self):
        return self.identifier        
    def getChars(self):
        return self.chars
    def getStates(self):
        return self.states
    def getAccepting(self):
        return self.accepting
    def getDirections(self):
        return self.directions
    
    def setIdentifier(self, identifier):
        self.identifier = identifier
        
    def setChars(self, chars):
        self.chars = chars
        
    def setStates(self, states):
        self.states = states
        
    def setAccepting(self, accepting):
        self.accepting = accepting
        
    def setDirections(self, directions):
        self.directions = directions
    
    def getTransitions(self):
        return list(zip(self.chars, self.states))
    
    #Override "copy" to easily copy a state by val not by ref.
    def __copy__(self):
        ID = self.getIdentifier().copy()
        chars = self.getChars().copy()
        states = self.getStates().copy()
        directions = self.getDirections().copy()
        accepting = self.getAccepting().copy()
        
        return State(ID, chars, states, directions, accepting)    
        
    def addTransition(self, char, state, direction = None):
        chars = self.getChars()
        states = self.getStates()
        directions = self.getDirections()
        
        if(chars):
            chars.append(char)
        else:
            chars = [char]
            
        self.setChars(chars)
        
        if(states):
            states.append(state)
        else:
            states = [state]        
            
            
        self.setStates(states)
        
        
        if directions != None: 
            directions.append(direction)
            self.setDirections(directions)
    
    def getResultStateByChar(self, char):
        chars = self.getChars()
        states = self.getStates()
        resultStates = []
        
        for i in range(len(chars)):
            if chars[i] == char:
                resultStates.append(states[i])
                
        return resultStates
    
    #This returns a single transition
    def process(self, input):
        if input in self.chars:
            direction = None
            newstate_i = self.chars.index(input)
            newstate_code = self.states[newstate_i]
            if(self.directions != None): direction = self.directions[newstate_i]
            return newstate_code, direction
        return None

    #This returns a list of tuples of potential transitions 
    def nfa_process(self,input):
        chars = self.getChars()
        states = self.getStates()
        directions = self.getDirections()       
        potentialTransitions = []
        
        for i in range(len(chars)):
            if input == chars[i]:
                if directions != None: potentialTransitions.append((states[i],directions[i]))
                else: potentialTransitions.append((states[i]))  
        return potentialTransitions
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
            