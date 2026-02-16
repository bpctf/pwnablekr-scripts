from pwn import *

if __name__ == '__main__':
    # SSH into the machine to do the ctf.
    my_ssh = ssh("random", "pwnable.kr", password="guest", port=2222)
    # Run the executable.
    p = my_ssh.process(executable="./random")
    # There is no input, just a blank line so we can just send our value.
    p.send('2708864985')
    # Send a new line - simulates pressing the enter button on the keyboard.
    p.send(b'\n')
    # Recv all the text that comes after our input.
    flag = p.recvall()
    # Split it by the new line byte indicator.
    flag_arr = flag.split(b'\n')
    for recv_text in flag_arr:
        # Print it all so it's all on new lines and easier to look at.
        print(recv_text)
