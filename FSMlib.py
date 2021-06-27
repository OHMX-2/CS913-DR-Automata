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
    
    def find(self,newstate_code):
        for state in self.allStates:
            if(state.getIdentifier() == newstate_code):
                #print("Found State!:" , newstate_code)
                return state
            
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
                newstate_code, direction = self.currentState.process(inputstring[i])
                if (debug): print("Transitioning to: " + newstate_code + " with direction: " + direction)
                newstate = self.find(newstate_code)  
                if newstate is not None:
                    self.currentState = newstate
                else:
                    #No state found in state table
                    if (debug): print("No state found for code: " + newstate_code + " moving RIGHT and continuing in same state")
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
        jsontxt = utils.FSMEncoder().encode(self)
        exists = utils.checkExists(filename + ".json")
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
                exists = utils.checkExists(filename + ".json")
            if(option.upper() == "C"):
                print("Save cancelled")
                return -1
        f = open(str(filename) + ".json", "w")
        f.write(jsontxt)
        f.close()
        if(utils.checkExists(filename + ".json") == True):
            print("FSM saved successfully: " + filename + ".json")
        return 1
    
    
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
                if isConnected:
                    isSameDirection = (state.directions[i] in connectedStates[state.states[i]])
                direction = state.directions[i] 
                
                if(isConnected and isSameDirection):                
                    stateConnectionDict[(state.states[i]+"|"+state.directions[i])] += "," + state.chars[i]
                else:
                    stateConnectionDict[(state.states[i]+"|"+state.directions[i])] = state.chars[i]
                    connectedStates[state.states[i]] = [state.directions[i]]
                
                print("Dict:", stateConnectionDict)
                if(self.FSMType == "2DFA"):
                    edgeDirection = (": " + state.directions[i])  
                
                edgeLabels = list(stateConnectionDict.values())
                allConnections[state.identifier] = state.states

            print("ALL CONNECTIONS: ", allConnections)
            edgesToAdd = len(stateConnectionDict)
            print("count:", edgesToAdd)
            print("edge labels:", edgeLabels)
            edges = list(stateConnectionDict.keys())
            for i in range(edgesToAdd):
                pipeIndex = edges[i].index("|")
                stateID = edges[i][0:pipeIndex]
                direction = edges[i][pipeIndex+1:]
                modifier = ""
                if(stateID == state.identifier):
                    modifier = "[loop above]"
                elif(stateID in allConnections.keys()):
                    if(state.identifier in allConnections[stateID]):
                        modifier = "[bend left]"
                pathString += "(" + state.identifier + ")\t"
                pathString += "edge" + "\t" + modifier + "\t" + "node{$" 
                pathString += edgeLabels[i] + ": " + direction + "$} " + "(" + stateID + ")\n"
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

        f = open("demofile2.txt", "a")
        f.write("Now the file has more content!")
        f.close()

        print(fileString)
        return  
    

      
    def union(self, automata):
        if(self.FSMType != automata.FSMType):
            print("FSMs are not of the same type: " + self.FSMType + " != " + automata.FSMType)
            return -1;
        else:
            startState = self.initialState
            unionStates = []
            for state in self.allStates:
                unionStates.append(state)
            for state in automata.allStates:
                unionStates.append(state)
            
            
        
            
#def createFSM():            
        

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
    
    def process(self, input):
        if input in self.chars:
            direction = None
            newstate_i = self.chars.index(input)
            newstate_code = self.states[newstate_i]
            if(self.directions != None): direction = self.directions[newstate_i]
            return newstate_code, direction
        return None

            