# BabyBoi writeup - 50pts

## What we have
This chall provide us the following binary:

    $ file baby_boi
    baby_boi: ELF 64-bit LSB executable, x86-64, dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, not stripped

And a copy of libc-2.27, probably the same version used on the server.

First of all, I launched a [checksec](https://github.com/slimm609/checksec.sh) to have a better idea:

    $ checksec baby_boi
    [*] './baby_boi'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

## Disassembling
Then I loaded the binary into IDA Pro:

![Screenshot of the binary decompiled with IDA Pro](https://raw.githubusercontent.com/jacopotediosi/Writeups/master/CSAW-Quals-2019/Baby_Boi/Screenshots/1.jpg)

As we can see at line 10, there is an input using the gets function, which is notoriously vulnerable because it doesn't check the size of the input.

Our arbitrary input goes into the stack, because the variable v4 is a local variable.
After v4, which has a size of 32 bytes, there are on the stack 8 bytes of saved registers and 8 bytes containing the return address of the main function.

So it's obvious that **we can control RIP** (Instruction Pointer Register) and jump to any point of the program as we want, simply injecting as input 32+8=40 random chars and then the address (in little-endian) we want to jump to.

## Where to jump to?
Using the tool [one_gadget](https://github.com/david942j/one_gadget) on libc-2.27, I found some interesting points of libc to which we can jump to obtain a shell (this technique is called "[Ret2Libc](https://0x00sec.org/t/exploiting-techniques-000-ret2libc/1833)"):

    $ one_gadget libc-2.27.so 
	0x4f2c5 execve("/bin/sh", rsp+0x40, environ)
	constraints:
	  rcx == NULL

	0x4f322 execve("/bin/sh", rsp+0x40, environ)
	constraints:
	  [rsp+0x40] == NULL

	0x10a38c execve("/bin/sh", rsp+0x70, environ)
	constraints:
	  [rsp+0x70] == NULL

Libc is loaded dynamically, so we couldn't know the exact address to jump to (in fact, those indicated above are fixed offsets relative to the beginning of the Libc); but we have the leak of the printf function address at line 9.

We can use it to calculate the effective runtime address of the beginning of the libc, subtracting the printf offset (that it's fixed and can be found opening the Libc with IDA or pwntools) from the leaked address.

Adding one of the one_gadget offsets to the beginning of the libc address that that we have just obtained, we got the address to which we weant to jump to. Voilà!

## Finally
Putting it all together (you can see the final exploit in the [exploit.py](https://github.com/jacopotediosi/Writeups/blob/master/CSAW-Quals-2019/Baby_Boi/exploit.py) file) we finally got our shell and cat the flag.
I had to try the third one_gadget offset, because the others weren't working because of the value of the other registers :P

    $ python2 exploit.py [+] Opening connection to pwn.chal.csaw.io on port 1005:
	Printf offset: 0x64e80
	Actual addr: 0x7f265aba1e80
	Actual gadget: 0x7f265ac4738c
	[*] Switching to interactive mode
	$ cat flag.txt
	flag{baby_boi_dodooo_doo_doo_dooo}
