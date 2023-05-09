from tkinter import *
from PIL import ImageTk, Image
import random
#import counter
import sqlLitebase as sql2
import datetime

w=Tk()
w.geometry('900x500')
w.configure(bg='#d93d04')
w.resizable(0,0)
w.title('Sistema de gestion')
number_of_inputs = 5
lst = list(range(6,61))
lst2 = list(range(66,80))
lst3 = list(range(83,98))
last4 = lst+lst2+lst3
gen_park = 100
vip0 = 0
discapacitado0 = 0
ambulance0 = 0
proveedores0 = 0
normalc0 = 0
za = 0
zb = 0
zc = 0
zone_aa = 30
zone_bb = 30
zone_cc = 40
time_aa = 0
time_bb = 0
time_cc = 0
dinero_total_recolectado = 0
enumerated_parking = list(range(1,101))
vip = [1,2,3,4,5]
discapacitado = [61,62,63,64,65]
ambulance = [80,81,82]
proveedores = [98,99,100]
normalc = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, \
            36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, \
                77, 78, 79, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97]


############ DESITION OF THE PARKNUMBER AND BASED ON THIS THE ZONE ############

def parkingdesition():
    global parknum
    global vip
    if int(e2.get()) == 1:
        parknum = int(random.choice(vip))
        enumerated_parking.remove(parknum)
        vip.remove(parknum)
        
    elif int(e2.get()) == 2:
        parknum = int(random.choice(discapacitado))
        enumerated_parking.remove(parknum)
        discapacitado.remove(parknum)
        
    elif int(e2.get()) == 3:
        parknum = int(random.choice(ambulance))
        enumerated_parking.remove(parknum)
        ambulance.remove(parknum)
        
    elif int(e2.get()) == 4:
        parknum = int(random.choice(proveedores))
        enumerated_parking.remove(parknum)
        proveedores.remove(parknum)
        
    elif int(e2.get()) == 5:
        parknum = int(random.choice(normalc))
        enumerated_parking.remove(parknum)
        normalc.remove(parknum)

def zonedestination():
    if 1 <= parknum <= 30:
        zone = 'A'
    elif 31 <= parknum <= 60:
        zone = 'B'
    elif 61 <= parknum <= 100:
        zone = 'C'
    return zone

############ HOME INFORMATION ############
def default_home():
    f2=Frame(w,width=900,height=455,bg='#d93d04')
    f2.place(x=0,y=45)
    l2=Label(w,text="INFO ABOUT",fg='#000000',bg='#d93d04')
    l2.config(font=('Comic Sans MS', 30))
    l2.place(x=310,y=40)
    button26 = Button(w,text='ADD A CAR',command=addcarinfo,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button26.place(x=340,y=210)
    button28 = Button(w,text='REMOVE A CAR', command=removecarinfo,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button28.place(x=340,y=280)
    button29 = Button(w,text='STATISTICS',command=historicalinfo,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button29.place(x=340,y=350)

def addcarinfo():
    global button30
    global faddcar
    global faddcarl
    faddcar = Frame(w,width=900,height=455,bg='#d93d04')
    faddcar.place(x=0,y=45)
    button30 = Button(w,text='BACK', command=backhome,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button30.place(x=340,y=350)
    faddcarl = Label(w,text="At the moment to introduce Car type:",fg='#000000',bg='#d93d04')
    faddcarl.config(font=('Comic Sans MS', 10))
    faddcarl.place(x=320,y=80)
    faddcarl2 = Label(w,text="1 is VIP",fg='#000000',bg='#d93d04')
    faddcarl2.config(font=('Comic Sans MS', 10))
    faddcarl2.place(x=320,y=100)
    faddcarl3 = Label(w,text="2 is for Discapacitados",fg='#000000',bg='#d93d04')
    faddcarl3.config(font=('Comic Sans MS', 10))
    faddcarl3.place(x=320,y=120)
    faddcarl4 = Label(w,text="3 is for Ambulance",fg='#000000',bg='#d93d04')
    faddcarl4.config(font=('Comic Sans MS', 10))
    faddcarl4.place(x=320,y=140)
    faddcarl5 = Label(w,text="4 is for proveedores",fg='#000000',bg='#d93d04')
    faddcarl5.config(font=('Comic Sans MS', 10))
    faddcarl5.place(x=320,y=160)
    faddcarl6 = Label(w,text="5 is for normal cars",fg='#000000',bg='#d93d04')
    faddcarl6.config(font=('Comic Sans MS', 10))
    faddcarl6.place(x=320,y=180)
    
def removecarinfo():
    global button30
    global faddcar
    faddcar = Frame(w,width=900,height=455,bg='#d93d04')
    faddcar.place(x=0,y=45)
    button30 = Button(w,text='BACK', command=backhome,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button30.place(x=340,y=350)
    faddcarl = Label(w,text="In here only introduce the plate and search for it",fg='#000000',bg='#d93d04')
    faddcarl.config(font=('Comic Sans MS', 10))
    faddcarl.place(x=320,y=80)

def historicalinfo():
    global button30
    global faddcar
    faddcar = Frame(w,width=900,height=455,bg='#d93d04')
    faddcar.place(x=0,y=45)
    button30 = Button(w,text='BACK', command=backhome,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button30.place(x=340,y=350)
    faddcarl = Label(w,text="Here you can check the type of statistics you may like",fg='#000000',bg='#d93d04')
    faddcarl.config(font=('Comic Sans MS', 10))
    faddcarl.place(x=320,y=80)

def backhome():
    faddcar.destroy()
    button30.destroy()
    default_home()

def home():
    f1.destroy()
    default_home()

############statistics WINDOW ############
def statistics():
    f1.destroy()
    f2=Frame(w,width=900,height=455,bg='#d93d04')
    f2.place(x=0,y=45)
    l2=Label(w,text="Choose a data type",fg='#000000',bg='#d93d04')
    l2.config(font=('Comic Sans MS', 15))
    l2.place(x=290,y=105)
    button7 = Button(w,text='Real time', command=removecardata,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button7.place(x=200,y=200)
    button7 = Button(w,text='Historical', command=historicaldata,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button7.place(x=500,y=200)

def historicaldata():
    global f11
    global button17
    global l57
    global l58
    global l59
    global l60
    global l61
    global l62
    global l63
    global l64
    global l65
    global l66
    global l67
    global l68
    f11=Frame(w,width=400,height=300,bg='#ec6c31')
    f11.place(x=300,y=100)
    button17 = Button(w,text='OK', command=removee3,width=5,font=('ARIAL',24), bg='#f27405',activebackground='#f2ab05')
    button17.place(x=450, y=300)
    l57 =Label(w,text=f"Ingresados en VIP: {vip0}",fg='#000000',bg='#ec6c31')
    l57.config(font=('Comic Sans MS', 10))
    l57.place(x=320,y=105)
    l58 =Label(w,text=f"Ingresados en Discapacitados: {discapacitado0}",fg='#000000',bg='#ec6c31')
    l58.config(font=('Comic Sans MS', 10))
    l58.place(x=320,y=125)
    l59 =Label(w,text=f"Ingresados en Ambulancia: {ambulance0}",fg='#000000',bg='#ec6c31')
    l59.config(font=('Comic Sans MS', 10))
    l59.place(x=320,y=145)
    l60 =Label(w,text=f"Ingresados en Proveedores: {proveedores0}",fg='#000000',bg='#ec6c31')
    l60.config(font=('Comic Sans MS', 10))
    l60.place(x=320,y=165)
    l61 =Label(w,text=f"Ingresados en Normal: {normalc0}",fg='#000000',bg='#ec6c31')
    l61.config(font=('Comic Sans MS', 10))
    l61.place(x=320,y=185)
    l62 =Label(w,text=f"Ingresados en Zona A: {za}",fg='#000000',bg='#ec6c31')
    l62.config(font=('Comic Sans MS', 10))
    l62.place(x=320,y=205)
    l63 =Label(w,text=f"Ingresados en Zona B: {zb}",fg='#000000',bg='#ec6c31')
    l63.config(font=('Comic Sans MS', 10))
    l63.place(x=320,y=225)
    l64 =Label(w,text=f"Ingresados en Zona C: {zc}",fg='#000000',bg='#ec6c31')
    l64.config(font=('Comic Sans MS', 10))
    l64.place(x=320,y=245)
    l65 =Label(w,text=f"Dinero recolectado por proveedores: {dinero_total_recolectado}",fg='#000000',bg='#ec6c31')
    l65.config(font=('Comic Sans MS', 10))
    l65.place(x=320,y=265)
    l66 =Label(w,text=f"Tiempo Zona A: {time_aa}",fg='#000000',bg='#ec6c31')
    l66.config(font=('Comic Sans MS', 10))
    l66.place(x=320,y=285)
    l67 =Label(w,text=f"Tiempo Zona B: {time_bb}",fg='#000000',bg='#ec6c31')
    l67.config(font=('Comic Sans MS', 10))
    l67.place(x=320,y=305)
    l68 =Label(w,text=f"Tiempo Zona C: {time_cc}",fg='#000000',bg='#ec6c31')
    l68.config(font=('Comic Sans MS', 10))
    l68.place(x=320,y=325)
    
def removee3():
    f11.destroy()
    button17.destroy()
    l57.destroy()
    l58.destroy()
    l59.destroy()
    l60.destroy()
    l61.destroy()
    l62.destroy()
    l63.destroy()
    l64.destroy()
    l65.destroy()
    l66.destroy()
    l67.destroy()
    l68.destroy()

def removecardata():
    global f10
    global button16
    global l48
    global l49
    global l50
    global l51
    global l52
    global l53
    global l54
    global l55
    global l56
    f10=Frame(w,width=400,height=300,bg='#ec6c31')
    f10.place(x=300,y=100)
    l48 =Label(w,text=f"Bahias ocupadas en total: {100-gen_park}/100",fg='#000000',bg='#ec6c31')
    l48.config(font=('Comic Sans MS', 10))
    l48.place(x=320,y=105)
    l49 =Label(w,text=f"Bahias ocupadas Zona A: {30-zone_aa}/30",fg='#000000',bg='#ec6c31')
    l49.config(font=('Comic Sans MS', 10))
    l49.place(x=320,y=125)
    l50 =Label(w,text=f"Bahias ocupadas Zona B: {30-zone_bb}/30",fg='#000000',bg='#ec6c31')
    l50.config(font=('Comic Sans MS', 10))
    l50.place(x=320,y=145)
    l51 =Label(w,text=f"Bahias ocupadas Zona C: {40-zone_cc}/40",fg='#000000',bg='#ec6c31')
    l51.config(font=('Comic Sans MS', 10))
    l51.place(x=320,y=165)
    l52 =Label(w,text=f"Bahias ocupadas VIP: {5-len(vip)}/5",fg='#000000',bg='#ec6c31')
    l52.config(font=('Comic Sans MS', 10))
    l52.place(x=320,y=185)
    l53 =Label(w,text=f"Bahias ocupadas Discapacitados: {5-len(discapacitado)}/3",fg='#000000',bg='#ec6c31')
    l53.config(font=('Comic Sans MS', 10))
    l53.place(x=320,y=205)
    l54 =Label(w,text=f"Bahias ocupadas Ambulancias: {3-len(ambulance)}/3",fg='#000000',bg='#ec6c31')
    l54.config(font=('Comic Sans MS', 10))
    l54.place(x=320,y=225)
    l55 =Label(w,text=f"Bahias ocupadas Proveedors: {3-len(proveedores)}/3",fg='#000000',bg='#ec6c31')
    l55.config(font=('Comic Sans MS', 10))
    l55.place(x=320,y=245)
    l56 =Label(w,text=f"Bahias ocupadas Normales: {84-len(normalc)}/86",fg='#000000',bg='#ec6c31')
    l56.config(font=('Comic Sans MS', 10))
    l56.place(x=320,y=265)
    button16 = Button(w,text='OK', command=removee2,width=5,font=('ARIAL',24), bg='#f27405',activebackground='#f2ab05')
    button16.place(x=400, y=300)

def removee2():
    f10.destroy()
    button16.destroy()
    l48.destroy()
    l49.destroy()
    l50.destroy()
    l51.destroy()
    l52.destroy()
    l53.destroy()
    l54.destroy()
    l55.destroy()
    l56.destroy()

def removecar1():
    global e5
    f1.destroy()
    f2=Frame(w,width=900,height=455,bg='#d93d04')
    f2.place(x=0,y=45)
    l7=Label(w,text="Search for the plate of the car that you want to remove in the database",fg='#000000',bg='#d93d04')
    l7.config(font=('Comic Sans MS', 14))
    l7.place(x=80,y=100)
    e5 = Entry(w,width=20,font=('Arial', 24))
    e5.place(x=80,y=150)
    button7 = Button(w,text='Search',command=searchcar,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
    button7.place(x=500,y=150)

############ SEARCHING A CAR ############

def searchcar():
    global ci
    ci = sql2.search(e5.get())
    #print(ci)
    if e5.get() == '':
        global l7
        l7=Label(w,text="please enter a value",fg='#000000',bg='#d93d04')
        l7.config(font=('Comic Sans MS', 14))
        l7.place(x=290,y=300)
    elif ci == []:
        l9=Label(w,text="Car not found",fg='#000000',bg='#d93d04')
        l9.config(font=('Comic Sans MS', 14))
        l9.place(x=290,y=300)
    else:
        global l8
        global l10
        global l11
        global l12
        global l13
        global l14
        global button21
        global ci2
        global vip
        ci2 = ci[0]
        l8=Label(w,text=f"Placa: {ci2[0]} {ci2[1]}, {ci2[3]}, {ci2[4]}, {ci2[5]}, {ci2[6]}, {ci2[7]}",fg='#000000',bg='#d93d04')
        l8.config(font=('Comic Sans MS', 12))
        l8.place(x=200,y=250)
        l10=Label(w,text=f"Placa: {ci2[1]}",fg='#000000',bg='#d93d04')
        l10.config(font=('Comic Sans MS', 12))
        l10.place(x=200,y=280)
        l11=Label(w,text=f"Parknumber: {ci2[3]}",fg='#000000',bg='#d93d04')
        l11.config(font=('Comic Sans MS', 12))
        l11.place(x=200,y=310)
        l12=Label(w,text=f"Owner: {ci2[4]}",fg='#000000',bg='#d93d04')
        l12.config(font=('Comic Sans MS', 12))
        l12.place(x=200,y=340)
        l13=Label(w,text=f"Zone: {ci2[5]}",fg='#000000',bg='#d93d04')
        l13.config(font=('Comic Sans MS', 12))
        l13.place(x=200,y=370)
        l14=Label(w,text=f"Arrive Hour: {ci2[6]}:{ci2[7]}",fg='#000000',bg='#d93d04')
        l14.config(font=('Comic Sans MS', 12))
        l14.place(x=200,y=400)
        button21 = Button(w,text='Remove',command= removecar,width=15,font=('Poor Richard',18), bg='#f27405',activebackground='#f2ab05')
        button21.place(x=600,y=250)
        
############ REMOVING A CAR BASED ON THE SEARCH ############

def removecar():
    global f16
    global l31
    global l32
    global l33
    global button88
    global total_time
    q = ci2[5]
    l8.destroy()
    l10.destroy()
    l11.destroy()
    l12.destroy()
    l13.destroy()
    l14.destroy()
    button21.destroy()
    
    
    day = datetime.datetime.now().strftime("%d")
    month = datetime.datetime.now().strftime("%m")
    year = datetime.datetime.now().strftime("%Y")
    date = f"{day} / {month} / {year}"
    entry_hourplusmnutes = int(ci2[6]) * 60 + int(ci2[7])
    exit_hourplusminutes = int(datetime.datetime.now().strftime("%H")) * 60 + int(datetime.datetime.now().strftime("%M"))
    total_time = int(exit_hourplusminutes - entry_hourplusmnutes)
    
    calculateprice()
    
    f16=Frame(w,width=400,height=300,bg='#ec6c31')
    f16.place(x=300,y=100)
    button88 = Button(w,text='OK', command=removee4,width=5,font=('ARIAL',24), bg='#f27405',activebackground='#f2ab05')
    button88.place(x=400, y=300)
    l31=Label(w,text=f"Placa: {ci2[1]}",fg='#000000',bg='#ec6c31')
    l31.config(font=('Comic Sans MS', 12))
    l31.place(x=380, y=150)
    l32=Label(w,text=f"Tiempo total que duró: {total_time} minutos",fg='#000000',bg='#ec6c31')
    l32.config(font=('Comic Sans MS', 12))
    l32.place(x=380, y=180)
    l33=Label(w,text=f"Pago: {valor}",fg='#000000',bg='#ec6c31')
    l33.config(font=('Comic Sans MS', 12))
    l33.place(x=380, y=210)
    
    sql2.deleterow(ci2[1])
    sql2.insertrow2(ci2[0], ci2[1], ci2[2], ci2[3], ci2[4], q, ci2[6], ci2[7],datetime.datetime.now().strftime("%H"), datetime.datetime.now().strftime("%M"), date, total_time, 1)
    global gen_park
    global zone_aa
    global zone_bb
    global zone_cc
    global time_aa
    global time_bb
    global time_cc
    global vip
    global discapacitado
    global ambulance
    global proveedores
    global normalc
    gen_park += 1
    if ci2[0] == 1:
        vip.append(ci2[3])
    if ci2[0] == 2:
        discapacitado.append(ci2[3])
    if ci2[0] == 3:
        ambulance.append(ci2[3])
    if ci2[0] == 4:
        proveedores.append(ci2[3])
    if ci2[0] == 5:
        normalc.append(ci2[3])
    if q == 'A':
        zone_aa+=1
        time_aa+=total_time
    if q == 'B':
        zone_bb+=1
        time_bb+=total_time
    if q == 'C':
        zone_cc+=1
        time_cc+=total_time

def removee4():
    f16.destroy()
    l31.destroy()
    l32.destroy()
    l33.destroy()
    button88.destroy()

def calculateprice():
    global valor
    global dinero_total_recolectado
    valor = 0
    if ci2[0] == 4 and total_time>=2:
        valor += 5000
        dinero_total_recolectado += 5000
        

def calctime():
    global q2
    q2 = sql2.search2(e5.get())
    print(q2)

############ ADD A CAR WINDOW ############

def addigcar():
    global e1
    global e2
    global e3
    global e4
    f1.destroy()
    f2=Frame(w,width=900,height=500,bg='#d93d04')
    f2.place(x=0,y=45)
    l2=Label(w,text='Plate: ',fg='#000000',bg='#d93d04')
    l2.config(font=('Comic Sans MS',30))
    l2.place(x=90,y=110)
    e1=Entry(w,width=10,font=('Arial', 24))
    e1.place(x=346,y=120)
    #
    l3=Label(w,text='Car Type: ',fg='#000000',bg='#d93d04')
    l3.config(font=('Comic Sans MS',30))
    l3.place(x=80,y=160)
    e2=Entry(w,width=10,font=('Arial', 24))
    e2.place(x=346,y=170)
    #
    l4=Label(w,text='Model: ',fg='#000000',bg='#d93d04')
    l4.config(font=('Comic Sans MS',30))
    l4.place(x=80,y=210)
    e3=Entry(w,width=10,font=('Arial', 24))
    e3.place(x=346,y=220)
    #
    l5=Label(w,text='Owner Name: ',fg='#000000',bg='#d93d04')
    l5.config(font=('Comic Sans MS',30))
    l5.place(x=80,y=260)
    e4=Entry(w,width=10,font=('Arial', 24))
    e4.place(x=346,y=270)
    #
    button2 = Button(w,text='SUBMIT',command=myClick,width=15,font=('Poor Richard',15), bg='#f27405',activebackground='#f2ab05')
    button2.place(x=200,y=330)


############ ADD CAR TO THE DATA BASE BASED ON THE ENTRYS INFORMATION ############
def myClick():
    global vip
    global label
    global button4
    en = e1.get()
    en2 = e2.get()
    en3 = e3.get()
    en4 = e4.get()
    label=Label(w, text='Car added succesfully to system', bg='#d93d04',font=('Lucida Console', 20),fg='#cff07b')
    label2=Label(w, text='Please fill in all the fields', bg='#d93d04',font=('Lucida Console', 20),fg='#ffffff')
    label3= Label(w, text='This color is full', bg='#d93d04',font=('Lucida Console', 20),fg='#ffffff')
    if en == '':
        label2.place(x=250, y=450)
    if en2 == '':
        label2.place(x=250, y=450)
    if en3 == '':
        label2.place(x=250, y=450)
    if en4 == '':
        label2.place(x=250, y=450)
    elif vip == []:
        label3.place(x=250,y=450)
    elif discapacitado == []:
        label3.place(x=250,y=450)
    elif ambulance == []:
        label3.place(x=250,y=450)
    elif proveedores == []:
        label3.place(x=250,y=450)
    elif normalc == []:
        label3.place(x=250,y=450)
    else:
        global q
        day = datetime.datetime.now().strftime("%d")
        month = datetime.datetime.now().strftime("%m")
        year = datetime.datetime.now().strftime("%Y")
        date = f"{day} / {month} / {year}"
        label.place(x=100,y=400)
        parkingdesition()
        q = zonedestination()
        sql2.insertrow(int(e2.get()), e1.get(), e3.get(), parknum,e4.get(), q, datetime.datetime.now().strftime("%H"), datetime.datetime.now().strftime("%M"), date, 0)
        button4 = Button(w,text='RECIBO',command=receipt,width=15,font=('Poor Richard',15), bg='#f27405',activebackground='#f2ab05')
        button4.place(x=400,y=330)
        actuli()

############ ACTUALIZE ALL THE DATA VARIABLES ############

def actuli():
    global vip0
    global discapacitado0
    global ambulance0
    global proveedores0
    global normalc0
    global gen_park
    global zone_aa
    global zone_bb
    global zone_cc
    global za
    global zb
    global zc
    global time_aa
    gen_park -= 1
    if q == 'A':
        zone_aa-=1
        za+=1
        if int(e2.get()) == 1:
            vip0+=1
        if int(e2.get()) == 5:
            normalc0+=1
    if q == 'B':
        zone_bb-=1
        zb+=1
        if int(e2.get()) == 5:
            normalc0+=1
    if q == 'C':
        zone_cc-=1
        zc+=1
        if int(e2.get()) == 2:
            discapacitado0+=1
        if int(e2.get()) == 3:
            ambulance0+=1
        if int(e2.get()) == 4:
            proveedores0+=1
        if int(e2.get()) == 5:
            normalc0+=1 
############ PRINT A RECEIPT WITH THE DATA ############

def receipt():
    global f5
    global l6
    global l17
    global l18
    global l19
    global button5
    f5 = Frame(w, width=200, height=400, bg='#f7d141')
    f5.place(x=640,y=40)
    l6 = Label(w,text=f'Bahía a ocupar: {parknum}',fg='#000000',bg='#f7d141')
    l6.config(font=('Comic Sans MS',15))
    l6.place(x=650, y=60)
    l17 = Label(w,text=f'Tipo: {int(e2.get())}',fg='#000000',bg='#f7d141')
    l17.config(font=('Comic Sans MS',15))
    l17.place(x=700, y=120)
    l18 = Label(w,text=f'Zona: {q}',fg='#000000',bg='#f7d141')
    l18.config(font=('Comic Sans MS',15))
    l18.place(x=700,y=180)
    l19 = Label(w,text=f'Hora llegada: {datetime.datetime.now().strftime("%H")}:{datetime.datetime.now().strftime("%M")}',fg='#000000',bg='#f7d141')
    l19.config(font=('Comic Sans MS',15))
    l19.place(x=650, y=240)
    button5 = Button(w,text='OK', command=removee,width=5,font=('ARIAL',24), bg='#f27405',activebackground='#f2ab05')
    button5.place(x=680, y=300)

def removee():
        f5.destroy()
        l6.destroy()
        l17.destroy()
        l18.destroy()
        l19.destroy()
        button5.destroy()
        button4.destroy()
        label.destroy()

############ TOOGLE WINDOW ############

def toogle_win():
    global f1
    f1 = Frame(w, width=300,height=500, bg='#f27405')
    f1.place(x=0,y=0)
    
    def bttn(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#ffffff'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= '#000000'

        myButton1 = Button(f1,text=text,
                       width=42,
                       height=2,
                       fg='#000000',
                       border=0,
                       bg=fcolor,
                       activeforeground='#d93d04',
                       activebackground=bcolor,
                       font=('Poor Richard',10),           
                        command=cmd)
                      
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)

    bttn(0,80,'HOME','#d92804','#f27405',home)
    bttn(0,117,'ADD CAR','#d92804','#f27405',addigcar)
    bttn(0,154,'STATISTICS','#d92804','#f27405',statistics)
    bttn(0,191,'REMOVE CAR','#d92804','#f27405',removecar1)
    
    
    def dele():
        f1.destroy()
        
    global img2
    img2=ImageTk.PhotoImage(Image.open('close.png'))
    
    Button(f1,image=img2,command=dele,border=0,activebackground='#f27405',bg='#f27405').place(x=5, y=10)
        
default_home()

img1=ImageTk.PhotoImage(Image.open('open.png'))
Button(w,command=toogle_win,image=img1,border=0,bg='#d93d04',activebackground='#d93d04').place(x=5,y=10)

w.mainloop()