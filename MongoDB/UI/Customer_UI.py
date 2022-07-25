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
mycol = mydb['CustomerD']



lst = [['ID','Name','Email','Contact']]

def callback(event):
    # global lstindex
    li =[]
    li=event.widget._values
    # lstindex=li[1]
    cid.set(lst[li[1]][0])
    cname.set(lst[li[1]][1])
    cemail.set(lst[li[1]][2])
    cContact.set(lst[li[1]][3])
    


def creategrid(n):
    lst.clear()
    lst.append(["ID","Name","Email","Contact"])
    cursor = mycol.find({})
    for text_fromdb in cursor:
        CustomerID = str(text_fromdb['CustomerID'])  
        CustomerName = str(text_fromdb['CustomerName'].encode('utf-8').decode("utf-8"))
        Email = str(text_fromdb['Email'].encode('utf-8').decode("utf-8"))  
        Contact= str(text_fromdb['Contact'].encode('utf-8').decode("utf-8")) 
        lst.append([CustomerID,CustomerName,Email,Contact])  

    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mgrid= tk.Entry(window,width=15)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(),i
            mgrid.grid(row=i+7,column=j+6)
            mgrid.bind("<Button-1>",callback)

    if n==1:
        for label in window.grid_slaves():
            if int (label.grid_info()["row"]) > 6:
                label.grid_forget()




def msgbox(msg,titlebar):
    result=messagebox.askokcancel(titlebar,message=msg)
    return result

def save1 ():
    r=msgbox("save record?","record")
    if r==True:
        newid=mycol.count_documents({})
        if newid!=0:
            newid=mycol.find_one(sort=[("CustomerID",-1)])["CustomerID"]
        id= newid+1
        cid.set(id)
        mydict={"CustomerID": int(custid.get()),"CustomerName":custname.get(),"Email": custemail.get(),"Contact":custContact.get()}    
        x = mycol.insert_one(mydict)
        creategrid(1)
        creategrid(0)
        
def delete1():
    r=msgbox("delete record?","record")
    if r==True:
        myquery = {"CustomerID": int(custid.get())}
        mycol.delete_one(myquery)
        creategrid(1)
        creategrid(0)    


def update1():
    r=msgbox("update record?","record")
    if r==True:   
        myquery= {"CustomerID": int(custid.get())}
        newvalues={"$set":{"CustomerName":custname.get()}}
        mycol.update_one(myquery,newvalues)
        
        newvalues={"$set":{"Email": custemail.get()}}
        mycol.update_one(myquery,newvalues)
        
        newvalues={"$set":{"Contact":custContact.get()}}
        mycol.update_one(myquery,newvalues)
        creategrid(1)
        creategrid(0)    
        
    
    
window = tk.Tk()

window.title("Customer Form")
window.geometry("1050x400")
window.configure(bg="light cyan") 

label = tk.Label(window,text="    Customer Entry Form!",width=30,borderwidth=2,relief="solid",height=2,bg="dark orange",anchor="center")
label.config(font=("Courier" "Bold",20))
label.grid(column=2,row=1)

label = tk.Label(window,text="CustomerID: ",borderwidth=1,relief="solid",width=20,height=2,bg="dark orange",anchor="center",font="arial" "bold")
label.grid(column=1,row=2)
cid=tk.StringVar()
custid=tk.Entry(window, textvariable=cid)
custid.grid(column=2,row=2)
custid.configure(state=tk.DISABLED)


label = tk.Label(window,text="CustomerName: ",width=20,height=2,borderwidth=1,relief="solid",bg="dark orange",anchor="center",font="arial" "bold")
label.grid(column=1,row=3)
cname=tk.StringVar()
custname=tk.Entry(window, textvariable=cname)
custname.grid(column=2,row=3)

label = tk.Label(window,text="CustomerEmail: ",borderwidth=1,relief="solid",width=20,height=2,bg="dark orange",anchor="center",font="arial" "bold")
label.grid(column=1,row=4)
cemail=tk.StringVar() 
custemail=tk.Entry(window, textvariable=cemail)
custemail.grid(column=2,row=4)


label = tk.Label(window,text="CustomerContact: ",borderwidth=1,relief="solid",width=20,height=2,bg="dark orange",anchor="center",font="arial" "bold")
label.grid(column=1,row=5)
cContact=tk.StringVar() 
custContact=tk.Entry(window, textvariable=cContact)
custContact.grid(column=2,row=5)

creategrid(0)

savebtn= tk.Button(text="Save",borderwidth=1,relief="solid",height =1,width = 10,command=save1)
savebtn.grid(column=1,row=6)
savebtn= tk.Button(text="Delete",height =1,width = 10,borderwidth=1,relief="solid",command=delete1)
savebtn.grid(column=2,row=6)
savebtn= tk.Button(text="Update",height =1,width = 10,borderwidth=1,relief="solid",command=update1)
savebtn.grid(column=3,row=6)



window.mainloop()
