import virtualbox

vbox = virtualbox.VirtualBox()



def list_machine():
    for m in vbox.machines:
        print(m)

def launch_machine(vm_name):
    session = virtualbox.Session()
    machine = vbox.find_machine(vm_name)
    progress = machine.launch_vm_process(session,"gui",[])
    progress.wait_for_completion()

def pause_machine(vm_name):
    machine = vbox.find_machine(vm_name)
    session = machine.create_session()
    session.console.pause()

def resume_machine(vm_name):
    machine = vbox.find_machine(vm_name)
    session = machine.create_session()
    session.console.resume()

