from tkinter import *
from tkinter import font
import tkinter.messagebox
g_Tk = Tk()
g_Tk.geometry("1000x720+280+40")
DataList = []

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='normal', family = 'Helvetica ')
    MainText = Label(g_Tk, font = TempFont, text="SEOUL SUBWAY INFORMATION")
    MainText.pack()
    MainText.place(x=310, y = 20)


def InitSearchListBox():
    global SearchListBox
    scrollbar = Scrollbar(g_Tk)
    scrollbar.pack(side=RIGHT, fill=Y)

    photo = PhotoImage(file="sub.gif")  # 디폴트 이미지 파일
    imageLabel = Label(g_Tk, image=photo)
    imageLabel.place(x=100, y=70)

    myList = Label(g_Tk, image=photo)
    scrollbar.config(command=myList.yview)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=155)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=160)    # 검색 박스

def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)  # ?댁쟾 異쒕젰 ?띿뒪??紐⑤몢 ??젣
    iSearchIndex = SearchListBox.curselection()[0]  # 由ъ뒪?몃컯???몃뜳??媛?몄삤湲?
    if iSearchIndex == 0:  # ?꾩꽌愿
        SearchLibrary()
    elif iSearchIndex == 1:  # 紐⑤쾾?뚯떇
        pass#SearchGoodFoodService()
    elif iSearchIndex == 2:  # 留덉폆
        pass#SearchMarket()
    elif iSearchIndex == 3:
        pass#SearchCultural()

    RenderText.configure(state='disabled')

def SearchLibrary():
    import http.client
    from xml.dom.minidom import parse, parseString
    conn = http.client.HTTPConnection("openAPI.seoul.go.kr:8088")
    conn.request("GET", "/6b4f54647867696c3932474d68794c/xml/GeoInfoLibrary/1/800")
    req = conn.getresponse()

    global DataList
    DataList.clear()

    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            row = GeoInfoLibrary[0].childNodes

            for item in row:
                if item.nodeName == "row":
                    subitems = item.childNodes

                    if subitems[3].firstChild.nodeValue == InputLabel.get():  # 援??대쫫??媛숈쓣 寃쎌슦
                        pass
                    elif subitems[5].firstChild.nodeValue == InputLabel.get():  # ???대쫫??媛숈쓣 寃쎌슦
                        pass
                    else:
                        continue

                    # ?곗씠???쎌엯 援ш컙. ?곕씫泥섍? ?놁쓣 ?뚯뿉??"-"???ｋ뒗??
                    if subitems[29].firstChild is not None:
                        tel = str(subitems[29].firstChild.nodeValue)
                        pass  # ?꾩떆
                        if tel[0] is not '0':
                            tel = "02-" + tel
                            pass
                        DataList.append((subitems[15].firstChild.nodeValue, subitems[13].firstChild.nodeValue, tel))
                    else:
                        DataList.append((subitems[15].firstChild.nodeValue, subitems[13].firstChild.nodeValue, "-"))

            for i in range(len(DataList)):
                RenderText.insert(INSERT, "[")
                RenderText.insert(INSERT, i + 1)
                RenderText.insert(INSERT, "] ")
                RenderText.insert(INSERT, "시설명: ")
                RenderText.insert(INSERT, DataList[i][0])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "주소: ")
                RenderText.insert(INSERT, DataList[i][1])
                RenderText.insert(INSERT, "\n")
                RenderText.insert(INSERT, "전화번호: ")
                RenderText.insert(INSERT, DataList[i][2])
                RenderText.insert(INSERT, "\n\n")

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=775, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

InitTopText()
InitSearchListBox()



#InitInputLabel()
#InitSearchButton()
#InitRenderText()
#InitSendEmailButton()
#InitSortListBox()
#InitSortButton()

g_Tk.mainloop()