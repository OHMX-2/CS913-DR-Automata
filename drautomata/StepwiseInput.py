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


while(FSMType != 'DFA' and FSMType != '2DFA'):
    FSMType = input("Please enter the FSM type:\nCurrently Supported Types: 'DFA', '2DFA'\n>\t")
    directions = None
    

if(FSMType == '2DFA'):
    #Add the end markers as part of the input alphabet
    
    print("Please enter the 2DFA restriction mode:")
    print("0: None")
    print("1: Rotating")
    print("2: Sweeping")
    _2dfa_restriction = input()
    
    arrAlphabet.append("<")
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

initial_state = State(state_id, arrAlphabet, [], directions, accepting)
states[state_id] = initial_state
pending_states.append(state_id)
transitionType = ""


currentStateid = state_id
next_state = None
#for state in pending_states:
while(pending_states):
    state = pending_states[0]
    #print("begin state:",state)
    
    print()
    print("--- Transition information ---")
    for key in states.keys():
        print("State:",key)
        for i in range(len(states[key].getStates())):
            print("Upon receiving", arrAlphabet[i], "transition into state", states[key].getStates()[i])
            #print(states[key].getDirections())
            #print(states[key].getStates())
        if(len(states[key].getStates()) == 0):
            print("No transitions defined yet")
        print()
    
    for symbol in arrAlphabet:
    
        transitionType = ""
        while(transitionType.upper() != "N" and transitionType.upper() != "E"):
            print("Where should state", state, "transition to, upon recieving symbol:", symbol)
            print("N: New state")
            print("E: Existing State")
            transitionType = input(">\t")
            
        if(transitionType.upper() == 'N'):
            new_state_id = input("Please enter the identifier for the new state:\n>\t")
            acceptingInput = ""
            while(acceptingInput.upper() != "Y" and acceptingInput.upper() != "N"):
                acceptingInput = input("Is this state an accepting state? (Y/N)\n>\t")
            if(acceptingInput.upper() == 'Y'):
                accepting=True
            elif(acceptingInput.upper() == 'N'):
                accepting=False
                    
            new_state = State(new_state_id, arrAlphabet, [], directions, accepting)
            

            currentStates = states[state].getStates()
            states[new_state_id] = new_state
            
            currentStates.append(new_state_id)

            pending_states.append(new_state_id)
                
        if(transitionType.upper() == 'E'):
            print("Choose an existing state to transition to:")
            
            for key in states.keys():
                print("State:",key)
                for i in range(len(states[key].getStates())):
                    print("Upon receiving", arrAlphabet[i], "transition into state", states[key].getStates()[i])
                    #print(states[key].getDirections())
                    #print(states[key].getStates())
                if(len(states[key].getStates()) == 0):
                    print("No transitions defined yet")
            print()
            
            existing_state_id = input("\n>\t")
            currentStates = states[state].getStates()
            
            
            currentStates.append(existing_state_id)
            
        if(FSMType == '2DFA'):
            currentDirections = states[state].getDirections()
            direction = ""
            
            if(_2dfa_restriction == 0):
                while(direction.upper() != 'L' and direction.upper() != 'R'):
                    direction = input("Upon transitioning, which direction should the read-head move (L/R)\n>\t")
                    
            if(_2dfa_restriction == 2):
                if(symbol != "<" or symbol != ">"):
                    print("Sweeping automata selected, reversal is not possible on non-endmarker symbols, if this symbol is read whilst in State:", state, "traversal will continue in the same direction.")
                    direction = "C"
            currentDirections.append(direction)    
            states[state].setDirections(currentDirections)
        
        states[state].setStates(currentStates)
                
    #print("removing pending state", state)           
    pending_states.remove(state)

allStates =  list(states.values())

DFA_2 = FSM(FSMType ,allStates[0], allStates)

print(DFA_2)
filename = "stepwise-test2DFA"
DFA_2.save(filename);

        

                
                
def printCurrentStates(states):
    for key in states.keys():
        print(key, ":", states[key])
