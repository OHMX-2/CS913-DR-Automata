#Step-wise creation of automata

from FSMlib import FSM, State


inputAlphabet = ""
FSMType = ""
option = "Y"



states = {}
pending_states = []
directions = None

    


inputAlphabet = input("Please enter the input alphabet, with characters separated by a vertical bar \"|\" \nNOTE: '<' and '>' are reserved for 2DFA end-markers \n>\t")
arrAlphabet = inputAlphabet.split('|')
arrAlphabet.sort()


while(FSMType != 'DFA' and FSMType != '2DFA' and FSMType != 'NFA'):
    FSMType = input("Please enter the FSM type:\nCurrently Supported Types: 'DFA', '2DFA', 'NFA'\n>\t")
    

if(FSMType == '2DFA'):
    #Add the end markers as part of the input alphabet
    
    print("Please enter the 2DFA restriction mode:")
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

initial_state = State(state_id, [], [], directions, accepting)
states[state_id] = initial_state
pending_states.append(state_id)
#transitionType = ""




while(pending_states):
    currentState = pending_states[0]
    symbolIndex=0
    
    print()
    print("--- Transition information ---")
    for key in states.keys():
        print("State:",key)
        for i in range(len(states[key].getStates())):
            print("Upon receiving", states[key].getChars()[i], "transition into state", states[key].getStates()[i])
        if(len(states[key].getStates()) == 0):
            print("No transitions defined yet\n")

    while symbolIndex in range(len(arrAlphabet)):
            print("i = ", symbolIndex, " arrAlphabet = ", arrAlphabet, " length:", len(arrAlphabet))
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
                    
                
                
                newState = State(new_state_id, [], [], directions.copy(), accepting)

                states[new_state_id] = newState
                
                transition_state_id = new_state_id   
                
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
                existing_state_id = input("\n>\t")
                
                
                
                transition_state_id = existing_state_id

                
               
            #Add directions for 2DFA  
            if(FSMType == '2DFA' or FSMType == '2NFA'):
                direction = ""
                
                if(_2dfa_restriction == "0"):
                    while(direction.upper() != 'L' and direction.upper() != 'R'):
                        direction = input("Upon transitioning, which direction should the read-head move (L/R)\n>\t")
                        
                if(_2dfa_restriction == "1"):      
                    if(symbol == ">"):
                        print("Rotating automata selected, upon reaching the right endmarker, the automata may return to the beginning of the string and scan again (L->R only)")
                        print("Upon reading the end marker in state", currentState, "should the system move back to the beginning of the input? (Y/N)(Rotate)\n")
                        choice = input(">\t")
                        if(choice.upper() == "Y"): direction = "ROTATE"
                        else: direction = "R"
                    else:
                        direction = "R"
                    
                if(_2dfa_restriction == "2"):
                    if(symbol == "<" or symbol == ">"):
                        while(direction.upper() != 'L' and direction.upper() != 'R'):
                            direction = input("Upon transitioning, which direction should the read-head move (L/R)\n>\t")
                    else:
                        print("Sweeping automata selected, reversal is not possible on non-endmarker symbols, if this symbol (" + str(symbol) + ") is read whilst in State:", currentState, "traversal will continue in the same direction.")
                        direction = "C"
              
            if(FSMType == 'DFA' or FSMType == '2DFA'):
                symbolIndex+=1
                
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
                      
    print("removing pending state", currentState)           
    pending_states.remove(currentState)

allStates =  list(states.values())

FiniteStateMachine = FSM(FSMType ,allStates[0], allStates)

print(FiniteStateMachine)
filename = "stepwise-test2DFA"
FiniteStateMachine.save(filename);

        

                
                
def printCurrentStates(states):
    for key in states.keys():
        print(key, ":", states[key])
