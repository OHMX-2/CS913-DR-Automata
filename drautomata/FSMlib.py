import utils     
            
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
    
    def processString(self, inputstring, debug=False, stepmode=False):
        if (stepmode): 
            debug=True #Set debug to true, so that the user can see what is happening
            input("Press return to begin the FSM")
        if(self.FSMType == "2DFA"):
            i=0
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
                if (direction=="C"):
                    direction = lastDirection
                    if(debug): print("Automata continuing in previous transition direction:", direction)
                if (direction=="ROTATE"):
                    i = 0
                    if(debug): print("Index reset to 0 (rotate at endmarker)")
                if (direction=="L"):
                    i-=1
                    if (debug): print("Index-1 (LEFT), now at index: " + str(i) + "/" + str(len(inputstring)))
                else:
                    i+=1#Even if no direction is given (no transition to state) then move right to progress.
                    if (debug): print("Index+1 (RIGHT), now at index: " + str(i) + "/" + str(len(inputstring)))
                if (stepmode): input("Press return to proceed to the next step")
        elif(self.FSMType == "DFA"):
            for char in inputstring:
                if (debug): print("Current Symbol: " + char)
                newstate_code, direction = self.currentState.process(char)
                if (debug): print("Transitioning to: " + newstate_code)
                newstate = self.find(newstate_code)   
                if newstate is not None:
                    self.currentState = newstate
                else:
                    if (debug): print("No state found for code: " + newstate_code + " continuing in same state")
                if (stepmode): input("Press return to proceed to the next step")
        if (self.currentState.accepting):
            if (debug): print("Input string: '" + inputstring  + "' accepted!")
            return True;
        
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
        fileString = "\\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=3.5cm,scale = 1,transform shape]"
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
            print("Checking state: ", state)
            print("accepting?:" , state.accepting)
            
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
        
    def addTransition(self, char, state, directions = None):
        chars = self.getChars()
        states = self.getStates()
        directions = self.getDirections()
        
        chars.append(char)
        states.append(state)
        directions.append(direction)
        
        self.setChars(chars)
        self.setStates(states)
        self.setDirections(directions)
    
    def process(self, input):
        if input in self.chars:
            direction = None
            newstate_i = self.chars.index(input)
            newstate_code = self.states[newstate_i]
            if(self.directions != None): direction = self.directions[newstate_i]
            return newstate_code, direction
        return None

            