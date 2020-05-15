import tkinter as tk
from tkinter import filedialog
import tkinter.font as font

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import plotly.graph_objects as go
import plotly.express as px
import calendar

from datetime import datetime


root= tk.Tk()
root.title("Digitzing home expenses")
root.geometry("757x1037+832+67")
root.configure(background="#C1CDCD",highlightbackground="#d9d9d9",highlightcolor="black")

def destroy():
    global df,import_file_path,date,amount,df1,canvas,sender,month,year
    df=None
    df1=None
    import_file_path=None
    Text1.delete('1.0', tk.END)
    date=None
    amount=None
    canvas=tk.Canvas(root)
    canvas.place(relx=0.04, rely=0.46, relheight=0.53, relwidth=0.92)
    canvas.configure(background="white",borderwidth="2",highlightbackground="#d9d9d9",highlightcolor="black",width=695)

def getExcel ():
    global df,import_file_path,date,amount,df1,sender,month,year,month_year,monthyear
    destroy()
    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel (import_file_path)
    
    df.rename(columns={'amount_total_tax':'amount_total'},inplace=True)
    df1=pd.DataFrame(df,columns=['date_issue','amount_total','sender_name'])

    
    df['date_issue']=pd.to_datetime(df['date_issue'])
    date=list(df['date_issue'])


    amount=list(df['amount_total'])
    sender=list(df['sender_name'])
    ##month number nikalne and usko corresponding string
    df['year']=df['date_issue'].dt.year
    df['monthabb']=df['date_issue'].dt.month
    df['month']=df['monthabb'].apply(lambda x:calendar.month_abbr[x])


    monthabb=list(df['monthabb'])
    month=list(df['month'])
    year=list(df['year'])
    NaN = float("NaN")
    print(monthabb)
    '''for i in range(len(month)):
        if str(month[i])=='nan' or str(year[i])=='nan':
            month[i]=0
            year[i]= 0
            amount[i]= 0
            sender[i]= "unknown"
            date[i]= 0'''
 
    for i in range(len(monthabb)):
        month_year.append( str(int(year[i])) + '-' + str(int(monthabb[i])))
    
   

        ##monthyear=list(df['month_year']) 
    print (monthabb)
    print (year)
    print(date)
    print(month_year) 
    
    
    print("{} {}".format(date,amount,sender))
    print(df)
    Text1.insert(tk.END,str(df[['invoice_id','order_id','date_issue','amount_total']]))


def generate():
    global date,amount,df,Canvas,df1,month,year,month_year,monthyear
    ##Code for plotting Bar Graph
    if(var.get()==1 and date!=None):
        ##Following is the code for removing same months in the graph and adding same month expenses to total expenses of that month
        month1=[]
        amount1=[]
        
        '''length=len(date)
        for i in range(length):
            temp=month[i]
            
            
            if temp not in month1 :
                month1.append(temp)
                amount1.append(amount[i])
            elif temp in month1:
                pos=month1.index(temp)
                amount1[pos]+=amount[i]'''
        ##Code ends here
                
        ##last 6 months
        last_x_mnths = []
        current_month = datetime.today().month 
        current_year =  datetime.today().year

        
    
        #last 6 month
        tempo = 0
        flag=0
        #change this variable for defining the plot of last x months graph
        how_many_months = 6
        for i in range(1,how_many_months + 1):
            tempm = current_month - i
        
            if tempm == 0 and flag==0:
                tempo+= 1
                current_year-= 1
                flag=1
            if flag==1:
                
                tempm = current_month - i + 12*tempo
                if tempm == 0:
                    tempo+=1
                    current_year-= 1
                    tempm = current_month - i + 12*tempo
                    
            tempy = current_year
                
            last_x_mnths.append(str(tempy) + '-' + str(tempm))
        month_year1=[]
        amount1=[]
        print("This is months year "+str(last_x_mnths))
        print("All the month year in data: " +str(month_year))
        length=len(month_year)
        for i in range(length):
            if str(month_year[i]) in last_x_mnths:
                
                temp = month_year[i]
                
                
                if temp not in month_year1 :
                    month_year1.append(temp)
                    amount1.append(amount[i])
                elif temp in month_year1:
                    pos=month_year1.index(temp)
                    amount1[pos]+=amount[i]
        
        ##last 6 months end
        
        

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.bar(month_year1,amount1,width=0.5)
        
        f.suptitle("Amount spend on each day",fontsize=12)
        a.set_xlabel('Month',fontsize=10)
        a.set_ylabel('Amount',fontsize=10)
   

    
    
        canvas = FigureCanvasTkAgg(f,root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.04, rely=0.46, relheight=0.53, relwidth=0.92)

        #print("Option bar data {}{}".format(month,amount))
        print("Option bar data {}{}".format(month_year1,amount1))
    ##Code for plotting Line Graph
    elif(var.get()==2 and date!=None):
        #Following is the code for removing same dates in the graph
        date1=[]
        amount1=[]
        length=len(date)
        for i in range(length):
            temp=date[i]
            if temp not in date1:
                date1.append(temp)
                amount1.append(amount[i])
            elif temp in date1:
                pos=date1.index(temp)
                amount1[pos]+=amount[i]
        ##Code ends here



            
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(date1,amount1)
        f.suptitle("Amount spend on each day",fontsize=12)
        a.set_xlabel('Month',fontsize=10)
        a.set_ylabel('Amount',fontsize=10)

        
        canvas = FigureCanvasTkAgg(f,root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.04, rely=0.46, relheight=0.53, relwidth=0.92)
        print("Option line data {}{}".format(date,amount))
        print("Option line data {}{}".format(date1,amount1))
    ##Code for plotting Pie Chart
    elif(var.get()==3 and date!=None):

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.axis('equal')
        amount1=[]
        senders1=[]

        amount=list(df1['amount_total'])
        senders=list(df1['sender_name'])
        length=len(senders)
        
        for i in range(length):
            temp=senders[i]
            if temp not in senders1:
                senders1.append(temp)
                amount1.append(amount[i])
            elif temp in senders1:
                pos=senders1.index(temp)
                amount1[pos]+=amount[i]        
            
        a.pie(amount1,labels=senders1,autopct='%1.2f%%')

        
        canvas = FigureCanvasTkAgg(f,root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.04, rely=0.46, relheight=0.53, relwidth=0.92)
        
        print("Option pie data {}{}".format(date,amount))

def generare1():
    global date,amount,df,Canvas,df1,count,month,year,month_year
    ##Code for plotting Bar Graph

    if(var.get()==1 ):

        fig = px.bar(df, x='month', y='amount_total',color='month')##,width=[10])
        fig.write_html('tmp.html', auto_open=True)
        ##plot ly shit ends
    

##        print("Option bar data {}{}".format(date,amount))
##        print("Option bar data {}{}".format(date1,amount1))
    ##Code for plotting Line Graph
    elif(var.get()==2 ):

        #plot ly shit
        fig = px.line(df1, x='date_issue', y='amount_total')

        fig.update_layout(
        xaxis_title="Month",
        )
        fig.write_html('tmp.html', auto_open=True)
        ##plotly shit ends

    ##Code for plotting Histogram
    elif(var.get()==3):

        ##plot ly shit
        fig = px.pie(df, values='amount_total', names='sender_name')
        fig.write_html('tmp.html', auto_open=True)
        
        ##plot ly shit ends
        
        print("Option pie data {}{}".format(date,amount))

##Globals
df=None
import_file_path=None
date=None
amount=None
df1=None
sender=None
count=0
month=None
year=None
month_year= []
monthyear=None


## importing excel file and placing it in the box    
browseButton_Excel = tk.Button(text='Browse',background="#C0D9D9",foreground="#000000",activebackground="#d9d9d9",highlightbackground="#d9d9d9",command=getExcel)
myFont=font.Font(size=10)
browseButton_Excel['font']=myFont
browseButton_Excel.place(relx=0.18,rely=0.02,height=42,width=122)

label1=tk.Label(root)
label1.place(relx=0.04,rely=0.03,height=33,width=100)
label1.configure(background="#C1CDCD",highlightbackground="#d9d9d9",text='''Upload File:''')

label2=tk.Label(root)
label2.place(relx=0.04,rely=0.09,height=31,width=90)
label2.configure(text="Your Data:",background="#C1CDCD",highlightbackground="#d9d9d9",foreground="#000000")

Text1=tk.Text(root)
Text1.place(relx=0.04, rely=0.13, relheight=0.21, relwidth=0.9)
Text1.configure(background="white")
Text1.configure(foreground="black")

##scrollar for text box
s=tk.Scrollbar(Text1,orient=tk.VERTICAL)
s.config(command=Text1.yview)
Text1.config(yscrollcommand=s.set)
s.pack(side=tk.RIGHT,fill=tk.Y)



##graph section
##Selecting type of graph

label3=tk.Label(root)
label3.place(relx=0.05, rely=0.35, relheight=0.09, relwidth=0.40)
label3.configure(disabledforeground="#a3a3a3",borderwidth=2, relief="groove",background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black",foreground="black",width=330)
label3.configure(justify=tk.LEFT,padx = 10, )

label4=tk.Label(root)
label4.place(relx=0.09, rely=0.35)
label4.configure(text="Type of Graph")
label4.configure(justify=tk.LEFT,padx = 10, )


##options for type of graph

var = tk.IntVar()


bar = tk.Radiobutton(root, variable=var, value=1,command=generate)
bar.place(relx=0.06,rely=0.40)
bar.configure(text="Bar Graph",background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black")

line = tk.Radiobutton(root, variable=var, value=2,command=generate)
line.place(relx=0.18,rely=0.40)
line.configure(text="Line Graph",background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black")

histo = tk.Radiobutton(root,  variable=var, value=3, command=generate)
histo.place(relx=0.30,rely=0.40)
histo.configure(text="Pie Chart",background="#d9d9d9",highlightbackground="#d9d9d9",highlightcolor="black")




##plotting graph space

canvas=tk.Canvas(root)
canvas.place(relx=0.04, rely=0.46, relheight=0.53, relwidth=0.92)
canvas.configure(background="white",borderwidth="2",highlightbackground="#d9d9d9",highlightcolor="black",width=695)



##refreshing
generate = tk.Button(text='Vizualize data')
generate.place(relx=0.75,rely=0.37,height=42,width=138)
generate.configure(background="#5F9EA0",foreground="#000000",activebackground="#d9d9d9",highlightbackground="#d9d9d9",command=generare1)


root.mainloop()
