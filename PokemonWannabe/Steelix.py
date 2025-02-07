import random

def receiveints(cs):
    buf = b''  # Initialize as a byte string
    while len(buf) < 4:
        data = cs.recv(8)
        buf += data
    # Unpack the first 4 bytes as a big-endian signed integer
    num = struct.unpack('!i', buf[:4])[0]
    return num
class Steelix:
    def __init__(self, protocol):
        self.basehp=220
        self.currenthp=220
        self.basedodge=7
        self.ultimatecooldown=1
        if protocol.lower() == "tcp":
            self.broadcast_method = self.broadcast_tcp
        elif protocol.lower() == "udp":
            self.broadcast_method = self.broadcast_udp

    def broadcast_tcp(self, text, cs1, cs2):
        cs1.send(text.encode())
        cs2.send(text.encode())

    def broadcast_udp(self, text, cs1, addr1, cs2, addr2):
        cs1.sendto(text.encode(), addr1)
        cs2.sendto(text.encode(), addr2)

    def broadcast(self, text, *args):
        self.broadcast_method(text, *args)

    def __str__(self):
        return "Steelix"
    def calculatedamage(self, power, pp):
        damage = power+int(random.uniform(-pp, pp))
        return damage;

    def attack1(self, Enemy, cs1, cs2, *broadcast_args):
        print("Steelix uses Tackle!")
        self.broadcast("Steelix uses Rock Throw!\n", cs1, cs2, *broadcast_args)
        power = 35
        pp = 35
        if (self.ultimatecooldown != 0):
            self.ultimatecooldown = self.ultimatecooldown - 1
        damage = self.calculatedamage(power, pp)
        Enemy.getattacked(self, damage, cs1, cs2, *broadcast_args)
        self.broadcast("\n", cs1, cs2, *broadcast_args)

    def attack2(self, Enemy, cs1, cs2, *broadcast_args):
        print("Steelix uses Rock Throw!")
        self.broadcast("Steelix uses Rock Throw!\n", cs1, cs2, *broadcast_args)
        power=50
        pp=15
        if (self.ultimatecooldown != 0):
            self.ultimatecooldown = self.ultimatecooldown - 1
        damage = self.calculatedamage(power, pp)
        Enemy.getattacked(self, damage, cs1, cs2, *broadcast_args)
        self.broadcast("\n", cs1, cs2, *broadcast_args)

    def attack3(self, Enemy, cs1, cs2, *broadcast_args):
        print("Steelix uses Crunch!")
        self.broadcast("Steelix uses Crunch!\n", cs1, cs2, *broadcast_args)
        power=80
        pp=15
        if(self.ultimatecooldown!=0):
            self.ultimatecooldown=self.ultimatecooldown-1
        damage=self.calculatedamage(power,pp)
        Enemy.getattacked(self, damage, cs1, cs2, *broadcast_args)
        self.broadcast("\n", cs1, cs2, *broadcast_args)



    def attack4(self, Enemy, cs1,cs2, *broadcast_args):
        power=80
        pp=20
        acc=80
        if (self.ultimatecooldown == 0):
            print("Steelix uses Slam!")
            self.broadcast("Steelix uses Slam!\n", cs1, cs2, *broadcast_args)
            chance=random.randint(1,101)
            if(chance<acc):
                damage = self.calculatedamage(power, pp)
                print("Attack successful!")
                self.broadcast("Attack successful!\n", cs1, cs2, *broadcast_args)
                Enemy.getattacked(Pikachu, damage, cs1, cs2, *broadcast_args)
            else:
                print("Miss!")
                self.broadcast("Miss!\n", cs1, cs2, *broadcast_args)
        else:
            text = "You can't use this yet!\n"
            self.broadcast(text, cs1, cs2, *broadcast_args)
            self.broadcast("\n", cs1, cs2, *broadcast_args)
            self.attack4(self, Enemy, cs1, cs2, *broadcast_args)

    def getattacked(self, Enemy, damage, cs1, cs2, *broadcast_args):
        dodge=random.randint(1, 101)
        if(dodge<=self.basedodge):
            print(f"{self} has dodged {Enemy}'s attack! ")
            self.broadcast(f"{self} has dodged {Enemy}'s attack! \n", cs1, cs2, *broadcast_args)
        else:
            print(f'{self} has taken {damage} damage. Hp left: {self.currenthp-damage}.')
            self.broadcast(f'{self} has taken {damage} damage. Hp left: {self.currenthp-damage}.\n', cs1, cs2, *broadcast_args)
            self.currenthp=self.currenthp-damage
            if(self.currenthp<0):
                print(f'{self} has been defeated by {Enemy}!')
                self.broadcast(f'{self} has been defeated by {Enemy}!\n', cs1, cs2, *broadcast_args)

            else: self.broadcast("\n", cs1, cs2, *broadcast_args)
        self.broadcast("\n", cs1, cs2, *broadcast_args)


