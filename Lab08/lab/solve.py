import angr
import sys

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d

class my_printf(angr.SimProcedure):
    def run(self, _):
        return 0

class my_scanf(angr.SimProcedure):
    def run(self, _, s):
        simfd = self.state.posix.get_fd(sys.stdin.fileno())
        data, ret_size = simfd.read_data(10)
        self.state.memory.store(s, int(data))
        return ret_size

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('printf', my_printf(), replace=True)

state = proj.factory.blank_state(addr=main_addr)
simgr = proj.factory.simulation_manager(state)

simgr.explore(find=find_addr, avoid=avoid_addr)

if simgr.found:
    ans_input = simgr.one_found.posix.dumps(sys.stdin.fileno())

    with open('solve_input', 'w') as f:
        for i in range(0, 150, 10):
            ans = ans_input[i:i+10].decode()
            f.write(f'{ans}\n')
else:
    print('Failed')
