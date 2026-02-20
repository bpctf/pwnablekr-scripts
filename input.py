from pwn import *
import os

if __name__ == '__main__':
    # Our first arg is the file we're executing because pwn requires this as an arg.
    args = ["./input2"]
    # Loop through 99 times and append "A" to our args.
    # This is because we need to pass 99 A's to the executable.
    # Our ./input2 arg is the 100th arg.    for x in range(1, 100):
    for x in range(1, 100):    
        args.append("A")
    # The code in this ctf says that argv['A'] needs to be \x00.
    # argv['A'] is equal to argv[65] because A's int value is 65.
    args[65]="\x00"
    # Argv['B'] = argv[66] and it needs to be \x20\x0a\x0d.
    args[66]="\x20\x0a\x0d"
    # Argv['C'] = argv[67] and it needs to be a string for our port.
    # because the C code calls atoi it will convert it to an int.
    args[67]='4444'
    # We need to write to the stdin and stderr so we create readers and writers.
    r1, w1 = os.pipe()
    r2, w2 = os.pipe()
    # Write to the stdin and stderr which is awaiting these specific values.
    os.write(w1, b"\x00\x0a\x00\xff")
    os.write(w2, b"\x00\x0a\x02\xff")
    # The executable is going to look for an environment variable
    # We pass it to the process so it will create the environment variable
    # for us.
    myenv = {"\xde\xad\xbe\xef": "\xca\xfe\xba\xbe"}
    # Run the input2 executable and pass it the necessary params.
    p = process(executable="./input2", argv=args, env=myenv, stdin=r1, stderr=r2)
    # Create a file as the executable will try to read this
    with open("\x0a", "w") as f:
        # Fill it with the required data
        f.write("\x00\x00\x00\x00")
    # Since I'm using pwn I might as well keep using it.
    # Use pwn's remote to connect to a socket and send it the required data.
    # Then close it because we clean up after ourselves here.
    conn = remote('localhost', args[67])
    conn.send(b"\xde\xad\xbe\xef")
    conn.close()
    # So we can receive the flag.
    p.interactive()


