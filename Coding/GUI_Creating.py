from tkinter import *
import json
import requests
import pandas as pd
from datetime import datetime

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Menu
        MainMenu(self)
        # Setup Frame

        container = Frame(self,bg = "#88cffa")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (StartPage, PageOne, PageTwo,PageThree, PageTwoA, PageTwoB,PageTwoC,PageTwoD,PageTwoE):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)

        label = Label(self, text="Menu")
        label.pack(padx=40, pady=10)
        page_one = Button(self, text="Build Data" ,command=lambda: controller.show_frame(PageOne), height=1, width=5, bg='black')
        page_one.bg = "red"
        page_one.place(x=450, y=180)
        page_two = Button(self, text="Search Movie", command=lambda: controller.show_frame(PageTwo), height=1, width=8)
        page_two.place(x=450, y=250)
        page_two = Button(self, text="Recommendation", command=lambda: controller.show_frame(PageThree), height=1, width=8)
        page_two.place(x=450, y=320)

class PageThree(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Movies Recommendation")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="SEARCH", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)

        label = Label(self, text="Based on year: Start from")
        label.place(x=150, y=150)
        label = Label(self, text="to")
        label.place(x=420, y=150)
        self.my_year1 = Entry(self, font=("Helvetica", 12),width=10)
        self.my_year1.place(x=320,y=150)
        self.my_year2 = Entry(self, font=("Helvetica", 12),width=10)
        self.my_year2.place(x=450, y=150)

        label = Label(self, text="Based on popularity:")
        label.place(x=150, y=200)
        label = Label(self, text="to:")
        label.place(x=420, y=200)
        #label = Label(self, text="3:")
        #label.place(x=550, y=200)
        self.my_popularity1 = Entry(self, font=("Helvetica", 12),width=10)
        self.my_popularity1.place(x=320, y=200)
        self.my_popularity2 = Entry(self, font=("Helvetica", 12),width=10)
        self.my_popularity2.place(x=450, y=200)
        #self.my_genre3 = Entry(self, font=("Helvetica", 5))
        #self.my_genre3.place(x=580, y=200)

        self.my_list = Listbox(self, bg="#ffffff", width=75, height=16)
        self.my_list.place(x=150,y=280)


        search1 = Button(self, text="Search Year", command=lambda: self.pmr_rangeyear())
        search1.place(x=700, y=150)
        search2 = Button(self, text="Search Popularity", command=lambda: self.pmr_popularity())
        search2.place(x=700, y=200)

    def pmr_rangeyear(self):
        low=self.my_year1.get()
        high=self.my_year2.get()
        base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/year"
        url = base + '.json?orderBy="$key"&startAt="' + str(low) + '"&endAt=' + '"' + str(high) + '"'
        r = requests.get(url)
        data = r.json()
        dlst = []
        for k, v in data.items():
            res = ""
            res += k + ":"
            for i in range(len(v)):
                if i == 0:
                    res += v[i]
                else:
                    res += "," + v[i]
            dlst.append(res)
        self.update(dlst)

    def pmr_popularity(self):
        low=self.my_popularity1.get()
        high=self.my_popularity2.get()
        base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/popularity"
        url = base + '.json?orderBy="$key"&startAt="' + str(low) + '"&endAt=' + '"' + str(high) + '"'
        r = requests.get(url)
        data = r.json()
        dlst = []
        for k, v in data.items():
            res = ""
            res += k + ":"
            for i in range(len(v)):
                if i == 0:
                    res += v[i]
                else:
                    res += "," + v[i]
            dlst.append(res)
        self.update(dlst)
    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)


class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Build your own movie database")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="SEARCH", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/"

        mkdir = Button(self,text = "Create File",command=lambda: self.mkdir())
        mkdir.place(x=150, y=100)
        self.nowlocation = "/.json"
        open = Button(self,text = "Open File",command = lambda: self.recordloc(self.my_entry.get()))
        open.place(x=280, y=100)
        back = Button(self,text = "Back",command=lambda:self.backloc())
        back.place(x=400, y=100)
        root = Button(self,text = "Desktop",command=lambda:self.reset())
        root.place(x=490, y=100)
        infor = Button(self,text = "Inforamation",command=lambda:self.cat())
        infor.place(x=600, y=100)
        remove = Button(self,text = "Delete File",command=lambda:self.rm())
        remove.place(x=740, y=100)
        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self,bg = "#ffffff" ,width=82,height=26)
        self.my_list.pack(pady=60)
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def rm(self):
        file = self.my_entry.get()
        if len(self.nowlocation)==6 and len(file)>0:
            path = file
            rm_dic = {"information": "information.json", "scores": "scores.json", "test": "test.json"}
            if path in rm_dic:
                new_path = rm_dic[path]
            else:
                new_path = path + self.nowlocation[-5:]
            rm_lnk = self.base + new_path
            requests.delete(rm_lnk)
            self.update(self.ls(self.nowlocation))
        elif len(self.nowlocation)>6 and len(file)>0:
            path = self.nowlocation[:-5]+file
            rm_dic = {"information": "information.json", "scores": "scores.json", "test": "test.json"}
            if path in rm_dic:
                new_path = rm_dic[path]
            else:
                new_path = path + "/.json"
            rm_lnk = self.base+new_path
            requests.delete(rm_lnk)
            self.update(self.ls(self.nowlocation))
        else:
            return

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i,":\t",str(d[i]))))
        self.update(res)

    def reset(self):
        self.nowlocation="/.json"
        self.update(self.ls(self.nowlocation))

    def recordloc(self,loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix,"/",loc,postfix))
        self.update(self.ls(self.nowlocation))

    def backloc(self):
        count = 0
        e = 0
        for j,i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count+=1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix,postfix))
        self.update(self.ls(self.nowlocation))

    def ls(self,name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def mkdir(self):
        url = self.base
        if len(self.nowlocation)>6 and self.my_entry.get()!="":
            path = self.nowlocation[:-5]+self.my_entry.get()+".json"
        if len(self.nowlocation)==6 and self.my_entry.get()!="":
            path = self.my_entry.get()+".json"
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        curr = now.strftime("%H:%M:%S")
        dic = {date: curr}
        data = json.dumps(dic, indent=4)
        link = url + path
        r = requests.put(link, data)
        self.update(self.ls(self.nowlocation))

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)


class PageTwo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        page_one = Button(self, text="Name", command=lambda: controller.show_frame(PageTwoA), height=1, width=7)
        page_one.place(x=150, y=120)
        page_two = Button(self, text="Genre", command=lambda: controller.show_frame(PageTwoB), height=1, width=3)
        page_two.place(x=290, y=120)
        page_three = Button(self, text="Year", command=lambda: controller.show_frame(PageTwoC), height=1, width=3)
        page_three.place(x=400, y=120)
        page_four = Button(self, text="Popularity", command=lambda: controller.show_frame(PageTwoD), height=1, width=5)
        page_four.place(x=510, y=120)
        page_five = Button(self, text="Language", command=lambda: controller.show_frame(PageTwoE), height=1, width=5)
        page_five.place(x=640, y=120)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)

        label_moviename = Label(self, text="Movie Name")
        label_moviename.place(x=150,y=280)
        self.moviename = Entry(self, font=("Helvetica", 20))
        self.moviename.place(x=250,y=280)

        label_genres = Label(self, text="Genres")
        label_genres.place(x=150, y=330)
        self.my_genres = Entry(self, font=("Helvetica", 20))
        self.my_genres.place(x=250,y=330)

        label_l = Label(self, text="Language")
        label_l.place(x=150, y=380)
        self.my_language = Entry(self, font=("Helvetica", 20))
        self.my_language.place(x=250,y=380)

        label_popularity = Label(self, text="Popularity")
        label_popularity.place(x=150, y=430)
        self.my_popularity = Entry(self, font=("Helvetica", 20))
        self.my_popularity.place(x=250,y=430)

        label_year = Label(self, text="year")
        label_year.place(x=150, y=480)
        self.my_year = Entry(self, font=("Helvetica", 20))
        self.my_year.place(x=250, y=480)
        putBtn = Button(self, text="Add Movie", command=lambda: self.addfile(), height=1, width=8)
        putBtn.place(x=600, y=380)
    def addfile(self):
        mv = self.moviename.get()
        year = self.my_year.get()
        genres = self.my_genres.get()
        popul = self.my_genres.get()
        lan = self.my_language.get()
        temp = {mv:{"new_genres":genres, "new_language":lan , "popularity": popul,"release_date":year}}
        try:

            self.put(temp)
        except:
            print("something wrong with the entry data.")

    def put(self,movie_dic):
        check = {"year": "release_date", "genres": "new_genres", "popularity": "popularity", "language": "new_language"}
        for i in movie_dic:
            base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/"
            link = base + "information/" + i + ".json"
            movie_content = movie_dic[i]  # type(movie_content): dictionary
            movie_json = json.dumps(movie_content)
            r = requests.put(link, movie_json)
            path = ["year", "genres", "popularity", "language"]
            for j in path:
                part = check[j]
                upload_part = movie_content[part]
                if type(upload_part) == int or type(upload_part) == float:
                    upload_part = round(upload_part)
                    upload_link = base + j + "/" + str(int(upload_part)) + ".json"
                    exist = requests.get(upload_link)
                    if exist.json() == None:
                        upload_lst = [i]
                    else:
                        upload_lst = exist.json()
                        upload_lst.append(i)
                    upload_json = json.dumps(upload_lst, indent=4)
                    db = requests.put(upload_link, data=upload_json)
                else:
                    tmp = upload_part.split(", ")
                    for k in tmp:
                        upload_link = base + j + "/" + k + ".json"
                        exist = requests.get(upload_link)
                        if exist.json() == None:
                            upload_lst = [i]
                        else:
                            upload_lst = exist.json()
                            upload_lst.append(i)
                        upload_json = json.dumps(upload_lst, indent=4)
                        db = requests.put(upload_link, data=upload_json)


class PageTwoA(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Search Movie Name")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="Back", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)


        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self, bg="#ffffff", width=82, height=26)
        self.my_list.pack(pady=60)
        open = Button(self, text="Open File", command=lambda: self.recordloc(self.my_entry.get()))
        open.place(x=320, y=100)
        back = Button(self, text="Back", command=lambda: self.backloc())
        back.place(x=450, y=100)
        infor = Button(self, text="Information", command=lambda: self.cat())
        infor.place(x=550, y=100)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/information"
        self.nowlocation = "/.json"
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def recordloc(self,loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix,"/",loc,postfix))
        self.update(self.ls(self.nowlocation))


    def backloc(self):
        count = 0
        e = 0
        for j,i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count+=1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix,postfix))
        self.update(self.ls(self.nowlocation))

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i, ":\t", str(d[i]))))
        self.update(res)

    def ls(self,name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)


class PageTwoB(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Genre")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="Back", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)
        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self, bg="#ffffff", width=82, height=26)
        self.my_list.pack(pady=60)
        open = Button(self, text="Open File", command=lambda: self.recordloc(self.my_entry.get()))
        open.place(x=380, y=100)
        back = Button(self, text="Back", command=lambda: self.backloc())
        back.place(x=520, y=100)
        #infor = Button(self, text="Infor", command=lambda: self.cat())
        #infor.place(x=670, y=100)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/genres"
        self.nowlocation = "/.json"
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def recordloc(self, loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, "/", loc, postfix))
        self.update(self.ls(self.nowlocation))

    def backloc(self):
        count = 0
        e = 0
        for j, i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count += 1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, postfix))
        self.update(self.ls(self.nowlocation))

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i, ":\t", str(d[i]))))
        self.update(res)

    def ls(self, name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)

class PageTwoC(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Year")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="Back", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)

        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self, bg="#ffffff", width=82, height=26)
        self.my_list.pack(pady=60)
        open = Button(self, text="Open File", command=lambda: self.recordloc(self.my_entry.get()))
        open.place(x=380, y=100)
        back = Button(self, text="Back", command=lambda: self.backloc())
        back.place(x=520, y=100)
        #infor = Button(self, text="Infor", command=lambda: self.cat())
        #infor.place(x=670, y=100)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/year"
        self.nowlocation = "/.json"
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def recordloc(self, loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, "/", loc, postfix))
        self.update(self.ls(self.nowlocation))

    def backloc(self):
        count = 0
        e = 0
        for j, i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count += 1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, postfix))
        self.update(self.ls(self.nowlocation))

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i, ":\t", str(d[i]))))
        self.update(res)

    def ls(self, name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)

class PageTwoD(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Popularity")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="Back", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)

        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self, bg="#ffffff", width=82, height=26)
        self.my_list.pack(pady=60)
        open = Button(self, text="Open File", command=lambda: self.recordloc(self.my_entry.get()))
        open.place(x=380, y=100)
        back = Button(self, text="Back", command=lambda: self.backloc())
        back.place(x=520, y=100)
        #infor = Button(self, text="Infor", command=lambda: self.cat())
        #infor.place(x=670, y=100)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/popularity"
        self.nowlocation = "/.json"
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def recordloc(self, loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, "/", loc, postfix))
        self.update(self.ls(self.nowlocation))

    def backloc(self):
        count = 0
        e = 0
        for j, i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count += 1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, postfix))
        self.update(self.ls(self.nowlocation))

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i, ":\t", str(d[i]))))
        self.update(res)

    def ls(self, name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)


class PageTwoE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_image = PhotoImage(file=r'images/new_bg_image.png')
        label = Label(self, image=bg_image)
        label.image = bg_image
        label.place(x=0, y=0, width=1000, height=700)
        label = Label(self, text="Language")
        label.pack(padx=10, pady=10)
        start_page = Button(self, text="HOME", command=lambda: controller.show_frame(StartPage), height=1, width=3)
        start_page.place(x=1, y=1)
        page_two = Button(self, text="Back", command=lambda: controller.show_frame(PageTwo), height=1, width=3)
        page_two.place(x=60, y=1)

        self.my_entry = Entry(self, font=("Helvetica", 20))
        self.my_entry.pack()
        self.my_list = Listbox(self, bg="#ffffff", width=82, height=26)
        self.my_list.pack(pady=60)
        open = Button(self, text="Open File", command=lambda: self.recordloc(self.my_entry.get()))
        open.place(x=380, y=100)
        back = Button(self, text="Back", command=lambda: self.backloc())
        back.place(x=520, y=100)
        #infor = Button(self, text="Infor", command=lambda: self.cat())
        #infor.place(x=670, y=100)
        self.base = "https://imdb-movies-d490a-default-rtdb.firebaseio.com/language"
        self.nowlocation = "/.json"
        toppings = self.ls(self.nowlocation)
        self.lastdata = toppings
        self.toppings = toppings
        self.update(self.lastdata)

        self.my_list.bind("<<ListboxSelect>>", self.fillout)
        self.my_entry.bind("<KeyRelease>", self.check)

    def recordloc(self, loc):
        prefix = self.nowlocation[:-6]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, "/", loc, postfix))
        self.update(self.ls(self.nowlocation))

    def backloc(self):
        count = 0
        e = 0
        for j, i in reversed(list(enumerate(self.nowlocation))):
            if i == "/":
                count += 1
            if count == 2:
                e = j
                break
        prefix = self.nowlocation[:e]
        postfix = self.nowlocation[-6:]
        self.nowlocation = "".join((prefix, postfix))
        self.update(self.ls(self.nowlocation))

    def cat(self):
        file = self.nowlocation[:-6]
        path = self.base + file + ".json"
        content = requests.get(path)
        d = content.json()
        res = []

        for i in d:
            if type(d[i]) == str and len(d[i]) == 0:
                continue
            else:
                res.append("".join((i, ":\t", str(d[i]))))
        self.update(res)

    def ls(self, name):
        directory = self.base + name
        r = requests.get(directory)
        dic = r.json()
        keys = []
        # dir_path = []
        for i in dic:
            keys.append(i)
        return keys

    def update(self, data):
        self.my_list.delete(0, END)
        for item in data:
            self.my_list.insert(END, item)

    def fillout(self, e):
        self.my_entry.delete(0, END)
        self.my_entry.insert(0, self.my_list.get(ACTIVE))

    def check(self, e):
        typed = self.my_entry.get()
        if typed == "":
            data = self.ls(self.nowlocation)
        else:
            data = []
            for item in self.ls(self.nowlocation):
                if typed.lower() in item.lower():
                    data.append(item)
        self.update(data)


class MainMenu:
    def __init__(self, master):
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)


app = App()

app.geometry('1000x700')

app.mainloop()
