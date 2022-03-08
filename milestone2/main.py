import datetime
import time
import yaml
import threading
import csv

values={}

def TimeFunction(inp, excTime):
    time.sleep(int(excTime))

def DataLoad(fileName,path):
    with open(fileName,mode='r') as file:
        csvFile=csv.reader(file)
        temp=[]
        for lines in csvFile:
            temp.append(lines)
        temp.pop(0)
        # print(temp)

        values[path+".DataTable"]=temp
        values[path+".NoOfDefects"]=len(temp)

file1 = open("Milestone2B_Log.txt", "w")

with open('Milestone2B.yaml') as f:
    YAMLdata = yaml.load(f, Loader=yaml.FullLoader)

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
                
                for x in threads:
                    x.start()

                for x in threads:
                    x.join()
                # for key, value in data["Activities"].items():

                #     traverse(value, path+"."+key) 
                    
        else:
            flag=True
            if "Condition" in data:
                cond=data["Condition"]
                right=int(cond[-1])
                symb=cond[-3]

                temp=cond[2:-5]
                # while True:
                #     time.sleep(1)
                #     if temp in values:
                #         break
                # print(values)
                # print(temp)
                if temp in values:
                    temp=values[temp]

                # temp=values[temp]
                if symb=="<" and temp>=right or symb==">" and temp<=right:
                    flag=False

            if flag:
                if data["Function"]=="DataLoad":
                    curr_time = str(datetime.datetime.now())
                    new_line = curr_time+";"+path+" Executing DataLoad ("+data["Inputs"]["Filename"]+")\n"
                    file1.write(new_line)

                    DataLoad(data["Inputs"]["Filename"],path)
                else:
                    curr_time = str(datetime.datetime.now())
                    new_line = curr_time+";"+path+" Executing TimeFunction ("+data["Inputs"]["FunctionInput"]+", "+data["Inputs"]["ExecutionTime"]+")\n"
                    file1.write(new_line)

                    TimeFunction(data["Inputs"]["FunctionInput"],data["Inputs"]["ExecutionTime"])

            else:
                curr_time = str(datetime.datetime.now())
                new_line = curr_time+";"+path+" Skipped\n"
                file1.write(new_line)
                
                

        curr_time = str(datetime.datetime.now())
        new_line = curr_time+";"+path+" Exit\n"
        file1.write(new_line)

    traverse(YAMLdata[list(YAMLdata.keys())[0]], list(YAMLdata.keys())[0])

file1.close()
