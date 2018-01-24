from kernel import core
import threading

def do_thread(fun,console):
    console.log("do thread ...")
    console.log(fun())

if __name__ == "__main__":
    interfaces = core.mainjob()
    jobs = interfaces.getjobs()
    console = interfaces.getconsole()


    for j in jobs:
        if j.is_thread ==  "okay":
            t =threading.Thread(target=do_thread,args=(j.do_test,console,))
            t.start()
    for i in jobs:
        if i.is_thread !=  "okay":
            result = i.do_test()
            console.log(result)

   
