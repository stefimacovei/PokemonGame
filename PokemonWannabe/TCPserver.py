import socket, threading, struct
from Pikachu import Pikachu
from Clefairy import Clefairy
from Steelix import Steelix
from Squirtle import Squirtle
from Psyduck import Psyduck
import string, threading
def gamestate(pokemon1, pokemon2):
    return pokemon1.currenthp>0 and pokemon2.currenthp>0

def receiveints(cs):
    buf = b''  # Initialize as a byte string
    while len(buf) < 4:
        data = cs.recv(8)
        buf += data
    num = struct.unpack('!i', buf[:4])[0]
    return num

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 12345
s.bind(("0.0.0.0", port) )
#s.bind(("192.168.43.49", port) )
#s.bind(("127.0.0.1", port) )

host="192.168.43.49"
def wait_for_clients(s):
    while True:
        print(f"Server is running on {host}:{port}")
        s.listen(1024)
        cs1, addr1 = s.accept()
        print(f"Connection from {addr1} as first player")

        s.listen(1024)
        cs2, addr2 = s.accept()
        print(f"Connection from {addr2} as second player")

        thread = threading.Thread(target=game, args=(cs1, cs2, addr1, addr2))
        thread.start()

def game(cs1, cs2, addr1, addr2):

    print("Player 1 selecting a pokemon")
    msg = b"Player 1 selecting a pokemon\n"
    cs2.send(msg)

    pikachu1 = Pikachu('tcp')
    clefairy1 = Clefairy('tcp')
    squirtle1 = Squirtle('tcp')
    steelix1 = Steelix('tcp')
    psyduck1 = Psyduck('tcp')

    pikachu2 = Pikachu('tcp')
    clefairy2 = Clefairy('tcp')
    squirtle2 = Squirtle('tcp')
    steelix2 = Steelix('tcp')
    psyduck2 = Psyduck('tcp')
    # Group them into two separate lists
    pokelist1 = [pikachu1, clefairy1, squirtle1, steelix1, psyduck1]
    pokelist2 = [pikachu2, clefairy2, squirtle2, steelix2, psyduck2]

    cs1.send(b"1. Pikachu\n2. Clefairy  3.Squirtle 4.Steelix 5.Psyduck\nPlease choose your pokemon: \n")
    option = receiveints(cs1)  # pokemonul primului
    try:
        player1 = pokelist2[int(option) - 1]
        p = f"You chose: {player1} \n"
        cs1.send(p.encode())
        print(f"Player 1 chose: {player1}")
    except (ValueError, IndexError):
        cs1.send("Invalid selection. Please choose 1 or 2.")

    cs1.send(b"player 2 selecting a pokemon\n")
    print("Player 2 selecting a pokemon")
    cs2.send(b"1. Pikachu\n2. Clefairy  3.Squirtle 4.Steelix 5.Psyduck\nPlease choose your pokemon: \n")

    option = receiveints(cs2)  # pokemonul al doilea
    print("test")
    try:
        player2 = pokelist1[int(option) - 1]
        p = f"You chose: {player2} \n"
        cs2.send(p.encode())
        print(f"Player 2 chose: {player2}")
    except (ValueError, IndexError):
        cs2.send(b"Invalid selection. Please choose a number between 1 and 4.\n")

    print(gamestate(player2, player1))

    attacklist1 = [
        player1.attack1,
        player1.attack2,
        player1.attack3,
        player1.attack4
    ]

    attacklist2 = [
        player2.attack1,
        player2.attack2,
        player2.attack3,
        player2.attack4
    ]
    while (gamestate(player2, player1)):
        index_player1 = receiveints(cs1)
        if 1 <= index_player1 <= len(attacklist1):
            attacklist1[index_player1 - 1](player2, cs1, cs2)
        else:
            print("Invalid index for Player 1's attack.")
        if not gamestate(player1, player2):
            cs1.close()
            cs2.close()
            print("its  over.")
        index_player2 = receiveints(cs2)
        if 1 <= index_player2 <= len(attacklist2):
            attacklist2[index_player2 - 1](player1, cs1, cs2)
        else:
            print("Invalid index for Player 2's attack.")

    cs1.close()
    cs2.close()
wait_for_clients(s)