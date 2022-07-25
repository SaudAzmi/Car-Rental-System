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
mycol1 = mydb['CarD']




lst = [['CarID','RegNo','Manufacturer','CarModel','YearOfPurchase','Availability']]

def callback(event):
    # global lstindex
    li =[]
    li=event.widget._values
    # lstindex=li[1]
    cid.set(lst[li[1]][0])
    cRegNo.set(lst[li[1]][1])
    cManufacturer.set(lst[li[1]][2])
    cmodel.set(lst[li[1]][3])
    cPurchase.set(lst[li[1]][4])
    cavail.set(lst[li[1]][5])
    


def creategrid(n):
    lst.clear()
    lst.append(["CarID","RegNo","Manufacturer","CarModel","YearOfPurchase","Availability"])
    cursor = mycol1.find({})
    for text_fromdb in cursor:
        CarID = str(text_fromdb['CarID']) 
        RegNo = str(text_fromdb['RegNo'].encode('utf-8').decode("utf-8"))
        Manufacturer = str(text_fromdb['Manufacturer'].encode('utf-8').decode("utf-8"))
        CarModel= str(text_fromdb['CarModel'].encode('utf-8').decode("utf-8")) 
        YearOfPurchase = str(text_fromdb['YearOfPurchase'])  
        Availability= str(text_fromdb['Availability'].encode('utf-8').decode("utf-8")) 
        lst.append([CarID,RegNo,Manufacturer,CarModel,YearOfPurchase,Availability])  

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
        newid=mycol1.count_documents({})
        if newid!=0:
            newid=mycol1.find_one(sort=[("CarID",-1)])["CarID"]
        id= newid+1
        cid.set(id)
        mydict={"CarID": int(custid.get()),"RegNo": custRegNo.get(),"Manufacturer":custManufacturer.get(),"CarModel": custmodel.get(),"YearOfPurchase":custPurchase.get(),"Availability":custcavail.get()}    
        x = mycol1.insert_one(mydict)
        creategrid(1)
        creategrid(0)
        
def delete1():
    r=msgbox("delete record?","record")
    if r==True:
        myquery = {"CarID": int(custid.get())}
        mycol1.delete_one(myquery)
        creategrid(1)
        creategrid(0)    


def update1():
    r=msgbox("update record?","record")
    if r==True:   
        myquery= {"CarID": int(custid.get())}
        
        newvalues={"$set":{"RegNo":custRegNo.get()}}
        mycol1.update_one(myquery,newvalues)
        
        newvalues={"$set":{"Manufacturer": custManufacturer.get()}}
        mycol1.update_one(myquery,newvalues)
        
        newvalues={"$set":{"CarModel":cmodel.get()}}
        mycol1.update_one(myquery,newvalues) 
        
        newvalues={"$set":{"YearOfPurchase":custPurchase.get()}}
        mycol1.update_one(myquery,newvalues)
        
        
        newvalues={"$set":{"Availability":custcavail.get()}}
        mycol1.update_one(myquery,newvalues)
        
        creategrid(1)
        creategrid(0)    
        
    
    
window = tk.Tk()

window.title("Car Form")
window.geometry("1050x400")
window.configure(bg="snow3") 

label = tk.Label(window,text="    Car Entry Form!",width=30,borderwidth=2,relief="solid",height=2,bg="light coral",anchor="center")
label.config(font=("Courier" "Bold",20))
label.grid(column=2,row=1)

label = tk.Label(window,text="CarID",borderwidth=1,relief="solid",width=20,height=2,bg="light coral",anchor="center",font="arial" "bold")
label.grid(column=1,row=2)
cid=tk.StringVar()
custid=tk.Entry(window, textvariable=cid)
custid.grid(column=2,row=2)
custid.configure(state=tk.DISABLED)


label = tk.Label(window,text="RegNo",borderwidth=1,relief="solid",width=20,height=2,bg="light coral",anchor="center",font="arial" "bold")
label.grid(column=1,row=3)
cRegNo=tk.StringVar()
custRegNo=tk.Entry(window, textvariable=cRegNo)
custRegNo.grid(column=2,row=3)


label = tk.Label(window,text="Manufacturer ",width=20,height=2,borderwidth=1,relief="solid",bg="light coral",anchor="center",font="arial" "bold")
label.grid(column=1,row=4)
cManufacturer=tk.StringVar()
custManufacturer=tk.Entry(window, textvariable=cManufacturer)
custManufacturer.grid(column=2,row=4)

label = tk.Label(window,text="CarModel: ",borderwidth=1,relief="solid",width=20,height=2,bg="light coral",anchor="center",font="arial" "bold")
label.grid(column=1,row=5)
cmodel=tk.StringVar() 
custmodel=tk.Entry(window, textvariable=cmodel)
custmodel.grid(column=2,row=5)


label = tk.Label(window,text="YearOfPurchase: ",borderwidth=1,relief="solid",width=20,height=2,bg="light coral",anchor="center",font="arial" "bold")
label.grid(column=1,row=6)
cPurchase=tk.StringVar() 
custPurchase=tk.Entry(window, textvariable=cPurchase)
custPurchase.grid(column=2,row=6)

label = tk.Label(window,text="Availability: ",borderwidth=1,relief="solid",width=20,height=2,bg="light coral",anchor="center",font="arial" "bold")
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
