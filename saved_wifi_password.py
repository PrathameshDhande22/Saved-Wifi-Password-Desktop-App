from tkinter import *
import subprocess
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

'''
Made by:- Prathamesh Dhande
Version : 1.0
Since :-20/03/2022
if you get any error contact email me on prathameshdhande534@gmail.com
Distributed by: prathameshcode.blogspot.com
'''


class wifi(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Saved Wifi Password")
        self.config(bg="white")
        self.resizable(width=False,height=False)

    def gui(self):
        Label(text="SAVED WIFI PASSWORD",font="arial 25 bold",bg='white').pack(pady=10,side=TOP,anchor=N)
        
        # creating button when user clicks the button all saved password must be visible
        self.generate_password=Button(self,text="Generate",font="calibri 12 bold",bg="orange",relief="ridge",bd=3,command=self.generate).place(x=20,y=360)
        Button(self,text="EXIT",font="calibri 12 bold",bg="orange",relief="ridge",bd=3,command=self.destroy).place(x=175,y=360)
        self.clear_button=Button(self,text="CLEAR",font="calibri 12 bold",bg="orange",relief="ridge",bd=3,command=self.clear_output).place(x=110,y=360)
        Label(text="Device Names \t\t   -   Password",font=["segoe UI Semibold","12"]).place(x=6,y=70)
        Label(text="Click on Generate Button to get the Saved Wifi Password from Your Device",font="Calibri 10").place(x=6,y=330)
        Label(text="Developed By Prathamesh Dhande",bg='white',font="Arial 10 bold").place(x=270,y=380)

        # creating the message box to display the output of the password
        self.output=Text(self,width=48,height=10,bd=2,relief='solid',font=["Times New Roman","15"])
        self.output.place(x=6,y=100)

        # button for saving the output in txt file
        self.save=Button(text="Save it in File",font="calibri 12 bold",command=self.savefile,bg="yellow",relief="groove")
        self.save.place(x=390,y=65)
        self.save.place_forget()
        


    def generate(self):
        self.save.place(x=390,y=65)
        data=subprocess.check_output("netsh wlan show profile")
        data=data.decode("utf-8").split("\n")
        
        wifinames=[]

        for profile in data:
            if "All User Profile" in  profile:
                profile=profile.split(":")
                
                profile=profile[1]
                profile=profile[1:-1]
                wifinames.append(profile)
        
        passwordlist=[]
        for name in wifinames:
            data=subprocess.check_output(['netsh','wlan','show','profile',name,'key=clear'])
            data=data.decode("utf-8").split("\n")
            
            for passw in data:
                if "Key Content" in passw:
                    password=passw.split(":")
                    
                    password=password[1]
                    password=password[1:-1]
                    passwordlist.append(password)
        
        a=len(wifinames)
        self.output.delete(1.0,END)
        for i in range(a):
            pas="{:<30} - \t{:}\n".format(wifinames[i],passwordlist[i])
            
            self.output.insert(END,pas)
            print(pas)
        self.output["state"]="disabled"
        messagebox.showinfo("Done","Password Extracted Successfully")

    def clear_output(self):
        self.output["state"]="normal"
        if len(self.output.get(1.0,END))==1:
            messagebox.showwarning("Warning","There is no Output To clear, Click ON Generate Button")
        else:
            a=messagebox.askyesno("Confirmation","Are You sure, You want To clear the Output Window")
            if a==True:
                self.output.delete(1.0,END)
                self.save.place_forget()
            else:
                self.output["state"]="disabled"

    def savefile(self):
        try:
            self.filename=asksaveasfilename(initialfile='Password.txt',defaultextension='.txt',filetypes=[('Text Files Only','*.txt')])
            with open(self.filename,'w') as f:
                f.write(self.output.get(1.0,END))
        except:
            pass

if __name__ == "__main__":
    wf=wifi()
    wf.gui()
    
    wf.mainloop()

