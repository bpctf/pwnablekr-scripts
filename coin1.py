from pwn import *
import re

if __name__ == '__main__':
    # SSH into the machine to do the ctf. Uncomment this line if you can use this from your machine, otherwise keep it commented and run the code on the pwnable.kr machine.
    # my_ssh = ssh("coin1", "pwnable.kr", password="guest", port=2222)
    # Remote into the coin game.
    rem = my_ssh.remote("0", 9007)
    # Print the text we receive.
    print(rem.recv())
    # Since we only need 100 fake coins, loop 100 times.
    for x in range(100):
        # Extract the Number of coins and the chances every loop.
        N, C = re.findall(r"^N=([0-9]+) C=([0-9]+)", rem.recv().decode('utf-8'))[0]
        N = int(N)
        C = int(C)
        # Print them after we've got the numbers.
        print(N, C)
        # Start is 0 and because start is 0 we can subtract 1 from N to get the end.
        start, end = 0, N-1
        # While our start is less than or equal to end and while we still have chances, guess.
        while start <= end and C > 0:
            # Find the middle. // is used to get a whole number.
            mid = start + (end - start) // 2
            # Send the first half of the numbers from 0 to mid + 1.
            guess = " ".join(str(num) for num in range(start, mid+1))
            # Send the guess.
            rem.sendline(guess)
            # Receive what is sent back as an int.
            resp = int(rem.recvline()[:-1])
            # If the response from the server is divisible by 10 with no remainder, then the fake coin is in the next half.
            if resp % 10 == 0:
                # Set the start to the second half of the total numbers.
                start = mid + 1
            # Otherwise if there is a remainder then we have a fake here and we need to stay in this half.
            else:
                end = mid - 1
            # Subtract one of our chances like the game does.
            C -= 1
        # Use the remainder of our chances. We need to do this 100 times, each counterfeit coin is a new game.
        while C > 0:
            # Send 0
            rem.sendline("0")
            # Receive the line
            print(rem.recvline(1024))
            # Remove 1 chance.
            C -= 1
        # Send the start value as our counterfeit.
        rem.sendline(str(start))
        # Print what we receive.
        print(rem.recv())
    # Print the flag after we've found 100 coins.
    print(rem.recv())


