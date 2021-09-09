import utils
import FSMlib
from FSMlib import State
from FSMlib import FSM
from more_itertools import locate
from itertools import product

def generateStrings(chars, length, path=""):
    text = ""
    
    chars = ''.join(chars)    

    for item in itertools.product(chars, repeat=length):
        text += ("".join(item)) + "\n"
        
    print(text)
    
    
    filename = chars + "_Len" + str(length) + ".txt"
    
    save_path = path 
    
    filename = save_path + filename   
    
    f = open(str(filename), "w")
    f.write(text)
    f.close()
    

def generateNFAs(alphabet=["0", "1"], statecount=3, saveNFA=False, saveDFA=False,DFAConversion=False, saveStats=False, processMultiple=False, processFilename=""):
    FSMType = "NFA"    
    binary = ["0","1"]

    
    permutations = []
    states = {}
    allStates = []
    stateIDs = []
    
    #Define all states depending on required statecount
    for i in range(statecount):
        ID = "q"+str(i)
        stateIDs.append(ID)
        states[ID] = []
    
    #Find all possible state configurations
    i = statecount*len(alphabet)
    for perm in product(binary, repeat=i):
        permutations.append(''.join(perm))

    if len(alphabet) == 2:
        ##Strict 2-symbol alphabet case (All states must contain a transition for each input symbol)
        toRemove = []
        for i in range(0, len(permutations)-1):
            hasEven = False
            hasOdd = False
            
            config = permutations[i]         
            lstConfig = list(config)
            if (lstConfig.count("1") < 2):
                if config not in toRemove:
                    toRemove.append(config)
            print("lstconfig:", lstConfig)
            for e in list(locate(lstConfig, lambda x: x == "1")):
                if e%2 == 0:
                    hasEven = True
                elif e%2 != 0:
                    hasOdd = True
            if hasOdd and hasEven:
                pass
            else:
                if config not in toRemove:
                    toRemove.append(config)
    
    #Relaxed case. (Can potentially yield non-fully defined states (no transition for a particular input symbol))
    else:
        pass
                    
                    
    for item in toRemove:
        permutations.remove(item)
    
    
    
    for ID in stateIDs:
        for perm in permutations:
            stateID = ID
            newState = State(stateID)        
            configuration = list(perm)
            for i in range(len(configuration)):
                
                destID = stateIDs[i%(len(stateIDs))]
                
    
                char = alphabet[i%(len(alphabet))]
    
                if configuration[i] == "1":                
                    newState.addTransition(char, destID)
            allStates.append(newState)
            states[ID].append(newState)
    
    
    
    
    
    
    
    configurations = list(range(0,len(states[ID])))

    count=0
    permutations2 = []
    print("configs:", len(configurations))
    print("states:", len(states))
    permutationcount = len(conifgurations)^len(states)
    input("This will generate " + str(permutationcount) + " if you are sure you wish to continue, please press <ENTER>")
    
    #Generate all permutations for all previously generated state configurations using cartesian product
    for perm2 in product(configurations, repeat=len(states)):
        #Loop decides which state is classed as the accepting state, arguably this could generate another FSM for every configuration of accepting states, it is ommitted here as the additional data would serve no purpose.
        #for j in range(len(states)):
        NFAtransitionscount = 0
        DFAtransitionscount = 0
        allStates = [] 
        for i in range(len(states)):  
            constState = states[stateIDs[i]][perm2[i]]
            state = State(constState.getIdentifier(), constState.getChars(), constState.getStates(), constState.getDirections())
            
            #See j loop above.
            #With this commented out, no state(s) will be marked as accepting.
            # if (i==j):
            #     state.setAccepting(True)
            # else:
            #     state.setAccepting(False)
            
            
            
            
            allStates.append(state)
        
        #Mark first state defined as the inital state
        initialState = allStates[0]
        
        #Mark a single (random) state as accepting, required for some data analysis.
        #acceptingIndex = randint(0,len(allStates)-1)
        #allStates[acceptingIndex].setAccepting(True)
        
        #Create the NFA
        NFA = FSM("NFA", initialState, allStates)
        
        #Generate the equivalent DFA
        if (DFAConversion):
            DFA = NFA.nfa_to_dfa()
        
        #Processing results for a list of strings. This process can get *very* long, depending on configuration settings. 
        if(processMultiple):
            while(stringFilename == ""):
                stringFilename = input("Please enter the name of the file you wish to read input strings from \n>\t")
            _, _, text = utils.processMultipleStrings(stringFilename, NFA, rtn=True)
            name = processFilename + "_" + str(len(alphabet)) + "_" + str(statecount)
            writeToFile(name, text=text, folder="NFA_string_processing", mode="a", ext=".csv")
         
        
        if (saveStats and DFAConversion):
            for state in NFA.allStates:
                NFAtransitionscount += len(state.states)
            
            for state in DFA.allStates:
                DFAtransitionscount += len(state.states)
                
                
            #Statistics on state count and transition count change during conversion process
            NFATransitions = NFAtransitionscount
            DFATransitions = DFAtransitionscount
            
            NFAStates = len(NFA.allStates)
            DFAStates = len(DFA.allStates)
            
            filename = "state_complexityNFAtoDFA_" + str(len(alphabet)) + "sym_" + statecount + "states"
            
            if count == 0:
                header = "type1" + "," + "type1_states" + "," + "type1_transitions"
                header += ","
                header += "type2" + "," + "type2_states" + "," + "type2_transitions"
                header += "\n"
                writeToFile(filename, text=header, mode="a", ext=".csv", folder="NFAtoDFA")
            
            data = ""
            data += "NFA," + str(NFAStates) + "," + str(NFATransitions) 
            data += ","
            data += "DFA," + str(DFAStates) + "," + str(DFATransitions)
            data += "\n"
            writeToFile(filename, text=data, mode="a", ext=".csv", folder="NFAtoDFA")
        
        if(saveNFA):
            #Write encoded NFA
            text = utils.FSMEncoder().encode(NFA)
            name = "NFA_#" + str(count)
            writeToFile(name, text=text)
        if(saveDFA and DFAConversion):
            #Write encoded DFA
            text = utils.FSMEncoder().encode(DFA)
            name = "DFA_#" + str(count)
            writeToFile(name, text=text)
        
        #Progress
        if count%10000 == 0: 
            print(count + "/" + permutationcount)

        count+=1
    

def writeToFile(filename, text=None, mode="w", ext=".json", folder="temp"):  

    #Add extension
    if(ext not in filename):
        filename += ext
    
    save_path = 'test\\Data\\' + folder + '\\'
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    

    filename = save_path + filename   

    f = open(str(filename), mode)
    f.write(text)
    f.close()

    




