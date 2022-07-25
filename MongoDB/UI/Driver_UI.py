# from pickle import TRUE
# from turtle import update
# from numpy import save, sort
from gc import callbacks
from numpy import mgrid
import pymongo
import tkinter as tk
from tkinter  import messagebox
from tkinter.ttk import *

from requests import delete

client = pymongo.MongoClient('localhost', 27017)
mydb = client['Test']
mycol2 = mydb['DriverD']

lst = [['DriverID','DriverName','Email','DrivingLicense','Contact','Rating']]

def callback(event):
    # global lstindex
    li =[]
    li=event.widget._values
    # lstindex=li[1]
    cid.set(lst[li[1]][0])
    cDriverName.set(lst[li[1]][1])
    cEmail.set(lst[li[1]][2])
    cmodel.set(lst[li[1]][3])
    cPurchase.set(lst[li[1]][4])
    cavail.set(lst[li[1]][5])
    


def creategrid(n):
    lst.clear()
    lst.append(["DriverID","DriverName","Email","DrivingLicense","Contact","Rating"])
    cursor = mycol2.find({})
    for text_fromdb in cursor:
        DriverID = str(text_fromdb['DriverID']) 
        DriverName = str(text_fromdb['DriverName'].encode('utf-8').decode("utf-8"))
        Email = str(text_fromdb['Email'].encode('utf-8').decode("utf-8"))
        DrivingLicense= str(text_fromdb['DrivingLicense'].encode('utf-8').decode("utf-8")) 
        Contact = str(text_fromdb['Contact'].encode('utf-8').decode("utf-8"))  
        Rating= str(text_fromdb['Rating'].encode('utf-8').decode("utf-8")) 
        lst.append([DriverID,DriverName,Email,DrivingLicense,Contact,Rating])  

    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid= tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(),i
            mgrid.grid(row=i+10,column=j+9)
            mgrid.bind("<Button-1>",callback)

    if n==1:
        for label in window.grid_slaves():
            if int (label.grid_info()["row"]) > 8:
                label.grid_forget()




def msgbox(msg,titlebar):
    result=messagebox.askokcancel(titlebar,message=msg)
    return result

def save1 ():
    r=msgbox("save record?","record")
    if r==True:
        newid=mycol2.count_documents({})
        if newid!=0:
            newid=mycol2.find_one(sort=[("DriverID",-1)])["DriverID"]
        id= newid+1
        cid.set(id)
        mydict={"DriverID": int(custid.get()),"DriverName": custDriverName.get(),"Email":custEmail.get(),"DrivingLicense": custmodel.get(),"Contact":custPurchase.get(),"Rating":custcavail.get()}    
        x = mycol2.insert_one(mydict)
        creategrid(1)
        creategrid(0)
        
def delete1():
    r=msgbox("delete record?","record")
    if r==True:
        myquery = {"DriverID": int(custid.get())}
        mycol2.delete_one(myquery)
        creategrid(1)
        creategrid(0)    


def update1():
    r=msgbox("update record?","record")
    if r==True:   
        myquery= {"DriverID": int(custid.get())}
        
        newvalues={"$set":{"DriverName":custDriverName.get()}}
        mycol2.update_one(myquery,newvalues)
        
        newvalues={"$set":{"Email": custEmail.get()}}
        mycol2.update_one(myquery,newvalues)
        
        newvalues={"$set":{"DrivingLicense":cmodel.get()}}
        mycol2.update_one(myquery,newvalues) 
        
        newvalues={"$set":{"Contact":custPurchase.get()}}
        mycol2.update_one(myquery,newvalues)
        
        
        newvalues={"$set":{"Rating":custcavail.get()}}
        mycol2.update_one(myquery,newvalues)
        
        creategrid(1)
        creategrid(0)    
        
    
    
window = tk.Tk()

window.title("Car Form")
window.geometry("1050x400")
window.configure(bg="cyan") 

label = tk.Label(window,text="    Car Entry Form!",width=30,borderwidth=2,relief="solid",height=2,bg="yellow",anchor="center")
label.config(font=("Courier" "Bold",20))
label.grid(column=2,row=1)

label = tk.Label(window,text="DriverID",borderwidth=1,relief="solid",width=20,height=2,bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=2)
cid=tk.StringVar()
custid=tk.Entry(window, textvariable=cid)
custid.grid(column=2,row=2)
custid.configure(state=tk.DISABLED)


label = tk.Label(window,text="DriverName",borderwidth=1,relief="solid",width=20,height=2,bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=3)
cDriverName=tk.StringVar()
custDriverName=tk.Entry(window, textvariable=cDriverName)
custDriverName.grid(column=2,row=3)


label = tk.Label(window,text="Email ",width=20,height=2,borderwidth=1,relief="solid",bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=4)
cEmail=tk.StringVar()
custEmail=tk.Entry(window, textvariable=cEmail)
custEmail.grid(column=2,row=4)

label = tk.Label(window,text="DrivingLicense: ",borderwidth=1,relief="solid",width=20,height=2,bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=5)
cmodel=tk.StringVar() 
custmodel=tk.Entry(window, textvariable=cmodel)
custmodel.grid(column=2,row=5)


label = tk.Label(window,text="Contact: ",borderwidth=1,relief="solid",width=20,height=2,bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=6)
cPurchase=tk.StringVar() 
custPurchase=tk.Entry(window, textvariable=cPurchase)
custPurchase.grid(column=2,row=6)

label = tk.Label(window,text="Rating: ",borderwidth=1,relief="solid",width=20,height=2,bg="yellow",anchor="center",font="arial" "bold")
label.grid(column=1,row=7)
cavail=tk.StringVar() 
custcavail=tk.Entry(window, textvariable=cavail)
custcavail.grid(column=2,row=7)





creategrid(0)

savebtn= tk.Button(text="Save",borderwidth=1,relief="solid",height =1,width = 10,command=save1)
savebtn.grid(column=1,row=8)
savebtn= tk.Button(text="Delete",height =1,width = 10,borderwidth=1,relief="solid",command=delete1)
savebtn.grid(column=2,row=8)
savebtn= tk.Button(text="Update",height =1,width = 10,borderwidth=1,relief="solid",command=update1)
savebtn.grid(column=3,row=8)



window.mainloop()
