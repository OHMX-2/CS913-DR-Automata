import utils     
 
#TODO: Create child classes for each automata type - code is becoming messy with more FSM classes being added.        
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
            
    def __str__(self):
        output = self.FSMType
        output += "\nInitial:" + str(self.initialState.getIdentifier())
        output += "\nallStates:" 
        
        for state in self.allStates:
            output += "\n" + str(state.getIdentifier()) + ":" + str(state.getChars()) + "," + str(state.getStates()) + "," + str(state.getDirections()) 
        return output
    

    def processString(self, inputstring, debug=False, stepmode=False, limit=1000):
        iters = 0
        if (stepmode): 
            debug=True #Set debug to true, so that the user can see what is happening
            input("Press return to begin the FSM")
            
        #2DFA
        if(self.FSMType == "2DFA"):
            i=0
            #TODO: Explore other termination conditions
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
                
        #DFA
        elif(self.FSMType == "DFA"):
            for char in inputstring:
                if (debug): print("Current Symbol: " + char)
                newstate_code, direction = self.currentState.process(char)
                if (debug): print("Transitioning to: " + newstate_code)
                newstate = self.find(newstate_code) 
                #If no state is specified in the transition, stay in the same state
                if newstate is not None:
                    self.currentState = newstate
                else:
                    if (debug): print("No state found for code: " + newstate_code + " continuing in same state")
                if (stepmode): input("Press return to proceed to the next step")
                iters += 1
                
        #NFA
        elif(self.FSMType == "NFA"):
            currentStates = []
            currentStates.append(self.getInitialState())
            
            for char in inputstring:
                nextStates = []
                for state in currentStates:
                    stateIdentifiers = state.nfa_process(char)
                    for ID in stateIdentifiers:
                        nextState = self.find(ID)
                        if nextState not in nextStates: 
                            nextStates.append(nextState)    
                currentStates = nextStates
            for state in currentStates:
                if state.getAccepting() == True:
                    return True
            return False
           
                
        print("Total iterations:" + str(iters))
        if (self.currentState.accepting):
            if (debug): print("Input string: '" + inputstring  + "' accepted!")
            return True
        
    def save(self,filename):
        text = utils.FSMEncoder().encode(self)
        utils.writeToFile(filename, text=text, option="JSON")
    
    
    def validate(self):
        valid_ids = []
        accepting_state_count = 0
        for state in self.allStates:
            valid_ids.append(state.identifier)
            accepting_state_count += state.accepting
            print("dirs:" + str(state.directions))
            print(("L" in state.directions or "R" in state.directions) or not state.direction)
        print(valid_ids)
        print(accepting_state_count)
        
     
    def visualize(self):
        distanceChosen = False
        distance = ""
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
            print("please specify a custom arrow style (default: 16 (Stealth)")
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
            if(intOption == 15): arrowstyle = "Stealth"
            if(intOption == 16): arrowstyle = "Triangle"
            if(intOption == 17): arrowstyle = "Turned Square"
            if(intOption == 18): arrowstyle = "Classical TikZ Rightarrow"
            if(intOption == 19): arrowstyle = "Computer Modern Rightarrow"
            if(intOption == 20): arrowstyle = "Implies"
            
            if(arrowstyle != ""): arrowChosen = True

        
        fileString = "\\begin{tikzpicture}[->,>="
        fileString += arrowstyle
        fileString += ",shorten >=1pt,auto,node distance="
        fileString += str(distance)
        fileString += "cm,scale = 1,transform shape]"
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
                if(isConnected and self.FSMType == "2DFA"):
                    isSameDirection = (state.directions[i] in connectedStates[state.states[i]])
                    direction = state.directions[i] 
                elif(isConnected and self.FSMType != "2DFA"):
                    isSameDirection = True
                
                if(isConnected and isSameDirection):              
                    if(self.FSMType == "2DFA"): 
                        stateConnectionDict[(state.states[i]+"|"+state.directions[i])] += "," + state.chars[i]
                    else:
                        stateConnectionDict[state.states[i]] += "," + state.chars[i]
                else:
                    if(self.FSMType == "2DFA"):
                        stateConnectionDict[(state.states[i]+"|"+state.directions[i])] = state.chars[i]
                        connectedStates[state.states[i]] = [state.directions[i]]
                    else:
                        stateConnectionDict[state.states[i]] = state.chars[i]
                        connectedStates[state.states[i]] = True
                
                if(self.FSMType == "2DFA"):
                    edgeDirection = (": " + state.directions[i])  
                
                edgeLabels = list(stateConnectionDict.values())
                allConnections[state.identifier] = state.states

            edgesToAdd = len(stateConnectionDict)
            edges = list(stateConnectionDict.keys())
            for i in range(edgesToAdd):
                if(self.FSMType == "2DFA"):
                    pipeIndex = edges[i].index("|")
                    stateID = edges[i][0:pipeIndex]
                    direction = edges[i][pipeIndex+1:]
                else: stateID = edges[i]
                modifier = ""
                if(stateID == state.identifier):
                    modifier = "[loop above]"
                elif(stateID in allConnections.keys()):
                    if(state.identifier in allConnections[stateID]):
                        modifier = "[bend left]"
                pathString += "(" + state.identifier + ")\t"
                pathString += "edge" + "\t" + modifier + "\t" + "node{$" 
                pathString += edgeLabels[i]
                if(self.FSMType == "2DFA"): pathString += ": " + direction
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
            else: position = "[right of=" + str((self.allStates[y-1].identifier)) + "]"
            nodeString += "] "+ position + "(" + state.identifier + ") {$" + state.identifier + "$};\n"
        
        
        fileString += nodeString + pathString + "\end{tikzpicture}"

        filename = input("Please enter the TikZ output filename\n>\t")

        utils.writeToFile(filename, fileString, "Visualize")
        return  
    

    #Union of automata requires a product construction of the state tables of both individual automata
    def operation(self, oper, automata=None):
        
        if (oper == "COMPLEMENT" and automata == None):
            newStates = []
            for state in self.allStates:                
                identifier = state.getIdentifier()
                chars = state.getChars()
                states = state.getStates()
                accepting = (not(state.getAccepting()))
                print("States:")
                print(state.getAccepting())
                print(accepting)
                newState = State(identifier, chars=chars, states=states, accepting=accepting)
                newStates.append(newState)
            initialState = newStates[0]
            DFA = FSM(self.FSMType, initialState, newStates)
            return DFA
        #Check if FSMs are of the same type
        elif(self.FSMType != automata.FSMType):
            print("FSMs are not of the same type: " + self.FSMType + " != " + automata.FSMType)
            return -1
        #TODO: allow for non-matching sets, and add error states for non-shared symbol transitions
        #Check if they contain the same symbol set      
        elif(sorted(self.initialState.getChars()) != sorted(self.initialState.getChars())):
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
                    print("processing state:", identifier)
                    print("is it accepting?:", (state1.getAccepting() == True or state2.getAccepting() == True))
                    chars = list(set(state1.getChars()) | set(state2.getChars()))
                    chars.sort()
                    for i in range(len(chars)):
                        print("DFA 1 (even ones) transitions to:", state1.states[i], "upon receiving:",chars[i])
                        print("DFA 2 (ends in one) transitions to:", state2.states[i], "upon receiving:",chars[i])
                        print("so combined state is:", (state1.states[i]+state2.states[i]) )
                        states.append((state1.states[i]+state2.states[i]))
                    if (oper.upper() == "UNION"):
                        if(state1.getAccepting() == True or state2.getAccepting() == True):
                            print(identifier, " - is accepting")
                            accepting = True
                        else:
                            accepting = False
                    elif (oper.upper() == "INTERSECTION"):
                        if(state1.getAccepting() == True and state2.getAccepting() == True):
                            print(identifier, " - is accepting")
                            accepting = True
                        else:
                            accepting = False
                    productState = State(identifier, chars=chars, states=states, accepting=accepting)
                    print("adding state:", productState.getIdentifier())
                    newStates.append(productState)
            initialState = newStates[0]
            DFA = FSM(self.FSMType, initialState, newStates)
            return DFA
        
                    
                    
            
            
                        
                        
                        
           
        

class State:
    def __init__(self, identifier, chars=None, states=None, directions = None, accepting = False):
        self.identifier = identifier
        self.chars = chars
        self.states = states
        self.accepting = accepting
        self.directions = directions
        
        
        
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
        
    def addTransition(self, char, state, direction = None):
        chars = self.getChars()
        states = self.getStates()
        directions = self.getDirections()
        
        chars.append(char)
        self.setChars(chars)
        
        
        states.append(state)
        self.setStates(states)
        
        
        if directions != None: 
            directions.append(direction)
            self.setDirections(directions)
    
    def process(self, input):
        if input in self.chars:
            direction = None
            newstate_i = self.chars.index(input)
            newstate_code = self.states[newstate_i]
            if(self.directions != None): direction = self.directions[newstate_i]
            return newstate_code, direction
        return None


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
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
                           
            