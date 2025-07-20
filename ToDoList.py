import customtkinter as ctk
import functools


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.geometry("650x800")
app.title("To-Do List")
app.resizable(False, False)

#dictionary 
kategorien_daten = {} 
sidebar_festgestellt = False



#Tasks hinzufügen eingabefeld und input 
add_aufgabe = ctk.CTkEntry(app,width=200, placeholder_text="Neue Aufgabe eingeben...")
add_aufgabe.place(x=170, y=65,) 



def toggle_sidebar_fixierung():
    global sidebar_festgestellt
    if sidebar_festgestellt:
     sidebar_festgestellt = False
    else:
     sidebar_festgestellt = True

    
    if sidebar_festgestellt:
        frame_sidebar.place(x=0, y=0)
        print("Sidebar fixiert")
    else:
        frame_sidebar.place_forget()
        print("Sidebar nicht fixiert")




def hide_sidebar(event):
  if not sidebar_festgestellt:
     frame_sidebar.place_forget()
     print("bar weg")

def show_sidebar(event):
    if not sidebar_festgestellt:
     frame_sidebar.place(x=0,y=0)

     print("Sidebar gezeigt")


frame_slide = ctk.CTkFrame(app, width=100, height=800, fg_color="transparent")
frame_slide.place(x=0, y=0)
frame_slide.bind("<Enter>", show_sidebar)

# Sidebar Frame
frame_sidebar = ctk.CTkFrame(app, width=150 ,height=800)
frame_sidebar.place(x=0,y=0)
frame_sidebar.place_forget()  
frame_sidebar.bind("<Leave>", hide_sidebar)

#fixierung button
sidebar_fixierung = ctk.CTkButton(frame_sidebar,text="📌", command=toggle_sidebar_fixierung, width=135, height=4,)
sidebar_fixierung.place(x=5,y=5)


#Aufgaben frame

frame_tasks =  ctk.CTkFrame(app, width=500 ,height=800)
frame_tasks.place(x=170, y=100)


##unterframe

frame_aufgaben_liste = ctk.CTkFrame(frame_tasks, fg_color="transparent", width=480, height=700)
frame_aufgaben_liste.pack(fill="both", expand=True, padx=20, pady=10)


#neue kategorien

aktive_kategorie = None 

global aufgabe

def dynamic_dictionary(kategorie_name):
   global aktive_kategorie
   #for widget in frame_aufgaben_liste.winfo_children(): widget.destroy()

   kategorien_daten[kategorie_name]

   aktive_kategorie = kategorie_name
   
   print("dic funktioniert")
   print(kategorien_daten)
   print("aktive kat;", aktive_kategorie)
   titel_top()
   aufgabe_anzeigen()





titel_label = ctk.CTkLabel(app, text="",width=50,height=30,font=("Arial", 25),fg_color="transparent")
titel_label.place(x=170, y=30)

def titel_top():
 titel_label.configure(text=aktive_kategorie)
  


kategorien_daten["Mein Tag"] = []
button_kat1 = ctk.CTkButton(frame_sidebar,text="Mein Tag" , width=135, height=4, font=('Arial', 16),command=functools.partial(dynamic_dictionary, "Mein Tag"))
button_kat1.place(x=5 ,y=90)

kategorien = []
kategorie_index = 0
kategorien.append(button_kat1)
  

kategorien_daten["Wichtig"] = []  
button_kat3 = ctk.CTkButton(frame_sidebar,text="★ Wichtig" , width=135, height=4, font=('Arial', 16),command=functools.partial(dynamic_dictionary, "Wichtig"))
button_kat3.place(x=5 ,y=120)

kategorie_index = 0 + 1
kategorien.append(button_kat3)


def erstellen():

 global kategorie_index
 global kategorien
 global kategorie_id


 name_kat = ctk.CTkInputDialog(text="Neue Kategorie:", title="Test")
 name = name_kat.get_input()
 if name in kategorien_daten:
  label = ctk.CTkLabel(app, text="ERROR=Der Name wird bereits verwendet",fg_color="transparent",font=('Arial', 20),text_color= 'red')
  label.place(relx=0.5, rely=0.5, anchor="center")
  label.after(2400, label.destroy)
 if name not in kategorien_daten:

  if name:
   kategorien_daten[name] = []
   button = ctk.CTkButton(frame_sidebar,text = (name) , width=135, height=4, font=('Arial', 16),command=functools.partial(dynamic_dictionary, name))
   button.place(x=5 ,y = 120 + kategorie_index * 30)

   kategorien.append(button)
   kategorien.append(name)
   kategorie_index += 1
   kategorie_id += 1
 


def aufgabe_add():
  aufgabe = add_aufgabe.get()
  if aufgabe.strip() and aktive_kategorie:
     kategorien_daten[aktive_kategorie].append({"text": aufgabe,"erledigt": False})
     add_aufgabe.delete(0, 'end')  
     aufgabe_anzeigen()

  else:
       label2 = ctk.CTkLabel(app, text="ERROR=Keine Kategorie gewählt oder fehlerhafte Eingabe",fg_color="transparent",font=('Arial', 20),text_color= 'red')
       label2.place(relx=0.5, rely=0.5, anchor="center") 
     

add_button = ctk.CTkButton(app, text="Bestätigen", command=aufgabe_add)
add_button.place(x=380, y=65)



###tasks auflisten

def aufgabe_anzeigen():

    for widget in frame_aufgaben_liste.winfo_children():
        widget.destroy()

    if aktive_kategorie:
        for i,aufgabe in enumerate (kategorien_daten[aktive_kategorie]):
            var = ctk.BooleanVar(value=aufgabe["erledigt"])

            def checkbox_command(aufgabe=aufgabe, var=var):
                aufgabe["erledigt"] = var.get()

            

            def löschen_command(index=i):
                del kategorien_daten[aktive_kategorie][index]
                aufgabe_anzeigen()

            def wichtig_command(index=i):
               aufgabe = kategorien_daten[aktive_kategorie][index]

               if aufgabe in kategorien_daten["Wichtig"]:
                 kategorien_daten["Wichtig"].remove(aufgabe)
               else:
                  kategorien_daten["Wichtig"].append(aufgabe)

               aufgabe_anzeigen()

    
            lösch_frame = ctk.CTkFrame(frame_aufgaben_liste, fg_color="transparent")
            lösch_frame.pack(fill="x",padx=10,pady=0)

            checkbox = ctk.CTkCheckBox(frame_aufgaben_liste,text=aufgabe["text"],variable=var,command=checkbox_command,font=("Arial", 18),height=30,width=400)
            checkbox.pack(anchor="w", padx=5,pady=0 )

            delete_button = ctk.CTkButton(lösch_frame,text= "🗑",width=30, height=30, command= löschen_command,hover_color="darkred")
            delete_button.pack(side="right",padx=0,pady=0 )
            #wichtig button
            wichtig_button = ctk.CTkButton(lösch_frame,text= "★",width=30, height=30, command= wichtig_command,hover_color="green")
            wichtig_button.pack(side="right",padx=5,pady=0 )

  

button_kat2 = ctk.CTkButton(frame_sidebar,text="➕ Hinzufügen" , width=135, height=4, font=('Arial', 16),command = erstellen)
button_kat2.place(x=5 ,y=770)
   
app.mainloop()
