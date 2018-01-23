from kernel import core

if __name__ == "__main__":
    interfaces = core.mainjob
    jobs = interfaces.getjobs()

    for j in jobs:
        result = j.do_test()
        print(j.description+" "+result)
