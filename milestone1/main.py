from ast import arg
from asyncio import threads
import datetime
import time
import yaml
import threading

def TimeFunction(inp, excTime):
    time.sleep(int(excTime))

file1 = open("Milestone1B_Log.txt", "w")


with open('Milestone1B.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    # print(data)

    def traverse(data, path):
        curr_time = str(datetime.datetime.now())
        new_line = (curr_time)+";"+path+" Entry\n"
        file1.write(new_line)

        if data["Type"] == "Flow":
            if data["Execution"] == "Sequential":
                for key, value in data["Activities"].items():

                    traverse(value, path+"."+key)     
            else:
                threads=[]
                for key, value in data["Activities"].items():
                    threads.append(threading.Thread(target=traverse,args=(value, path+"."+key)))
                # traverse(value, path+"."+key)
                for x in threads:
                    x.start()

                for x in threads:
                    x.join()
        else:
            curr_time = str(datetime.datetime.now())
            new_line = curr_time+";"+path+" Executing " +data["Function"]+" ("+data["Inputs"]["FunctionInput"]+", "+data["Inputs"]["ExecutionTime"]+")\n"
            file1.write(new_line)

            globals()[data["Function"]](data["Inputs"]["FunctionInput"],data["Inputs"]["ExecutionTime"])

        curr_time = str(datetime.datetime.now())
        new_line = curr_time+";"+path+" Exit\n"
        file1.write(new_line)

    traverse(data[list(data.keys())[0]], list(data.keys())[0])


file1.close()
