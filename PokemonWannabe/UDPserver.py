import socket
from Pikachu import Pikachu
from Clefairy import Clefairy
from Steelix import Steelix
from Squirtle import Squirtle
from Psyduck import Psyduck

def gamestate(pokemon1, pokemon2):
    return pokemon1.currenthp > 0 and pokemon2.currenthp > 0

def receive_choice(cs):
    data, addr = cs.recvfrom(1024)
    choice_str = data.decode().strip()
    try:
        choice = int(choice_str)
    except ValueError:
        choice = None
    return choice, addr

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 12345
s.bind(("192.168.43.49", port))

print(f"Server is running on 192.168.43.49:{port}")

pikachu = Pikachu('udp')
clefairy = Clefairy('udp')
squirtle = Squirtle('udp')
steelix = Steelix('udp')
psyduck = Psyduck('udp')
pokelist = [pikachu, clefairy, squirtle, steelix, psyduck]

confirmare, addr1=s.recvfrom(1024)
print(confirmare.decode())

print("Waiting for Player 1 to select a Pokémon")
choice1, addr1 = receive_choice(s)
s.sendto(b"1. Pikachu 2. Clefairy 3. Squirtle 4. Steelix 5. Psyduck Please choose your Pokemon: ", ("192.168.43.49", port))


choice1, addr1 = receive_choice(s)
if choice1 and 1 <= choice1 <= len(pokelist):
    player1 = pokelist[choice1 - 1]
    s.sendto(f"You chose: {player1}\n".encode(), addr1)
    print(f"Player 1 chose: {player1}")
else:
    s.sendto(b"Invalid selection. Please choose a number between 1 and 5.\n", addr1)

# Player 2 selection
print("Waiting for Player 2 to select a Pokémon")
s.sendto(b"1. Pikachu\n2. Clefairy\n3. Squirtle\n4. Steelix\n5. Psyduck\nPlease choose your Pokemon: ", ("192.168.43.49", port))

# Receive choice for Player 2
choice2, addr2 = receive_choice(s)
if choice2 and 1 <= choice2 <= len(pokelist):
    player2 = pokelist[choice2 - 1]
    s.sendto(f"You chose: {player2}\n".encode(), addr2)
    print(f"Player 2 chose: {player2}")
else:
    s.sendto(b"Invalid selection. Please choose a number between 1 and 5.\n", addr2)

# Start the battle loop
attacklist1 = [player1.attack1, player1.attack2, player1.attack3, player1.attack4]
attacklist2 = [player2.attack1, player2.attack2, player2.attack3, player2.attack4]

while gamestate(player1, player2):
    # Receive Player 1's attack choice
    index_player1, _ = receive_choice(s)
    if index_player1 and 1 <= index_player1 <= len(attacklist1):
        attacklist1[index_player1 - 1](player2, s, addr1, addr2)
    else:
        print("Invalid index for Player 1's attack.")

    # Check game state before Player 2 attacks
    if not gamestate(player1, player2):
        s.sendto(b"Game over! Player 1 wins!", addr1)
        s.sendto(b"Game over! Player 1 wins!", addr2)
        break

    # Receive Player 2's attack choice
    index_player2, _ = receive_choice(s)
    if index_player2 and 1 <= index_player2 <= len(attacklist2):
        attacklist2[index_player2 - 1](player1, s, addr1, addr2)
    else:
        print("Invalid index for Player 2's attack.")

    # Check game state after Player 2 attacks
    if not gamestate(player1, player2):
        s.sendto(b"Game over! Player 2 wins!", addr1)
        s.sendto(b"Game over! Player 2 wins!", addr2)
        break
