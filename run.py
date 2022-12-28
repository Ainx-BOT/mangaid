import os,sys,re,json,random
from time import sleep
try:
    import requests
    from bs4 import BeautifulSoup as bs
    from concurrent.futures import ThreadPoolExecutor
    from colorama import init, Fore
except ImportError:
    exit(f"[!] Install module dulu : python -m pip install -r requirements.txt")

#Warna
init(autoreset=True)
B = Fore.BLUE
W = Fore.WHITE
C = Fore.CYAN
G = Fore.GREEN
Y = Fore.YELLOW
R = Fore.RED
rgb=random.choice([B,C,G,Y])
ab="\033[90m"
pr=f"{W}[{rgb}?{W}]"
fr=f"{W}[{rgb}*{W}]"
er=f"{W}[{rgb}!{W}]"

#pemanis
def clear():
    os.system("clear")

def loading():
    for i in list("|/-\\•"):
        sys.stdout.write(f"\r{pr} Download...{W}({rgb}{i}{W})")
        sleep(0.2)

def baner():
    clear()
    print(f"""
      {rgb}[ {W}Mangaid Downloader{rgb} ]

{W}By       : {rgb}FahmiApz
{W}Facebook : {rgb}@Kadang Nolep Kadang Henteu
{R}---------------------------------------""")

#Parsing
def find_manga(title):
    result=[]
    req=requests.get(f"https://mangaid.click/search?query={title}",headers=ua).text
    js=json.loads(req)["suggestions"]
    for x in js:
        result.append(x["value"]+"|"+x["data"])
    return result

def get_chapter(manga):
    result=[]
    req=requests.get(f"https://mangaid.click/manga/{manga}",headers=ua).text
    parsing=bs(req,"html.parser").find_all("h5", class_="chapter-title-rtl")
    for data in parsing:
        data=data.find("a", href=lambda x: x and "manga" in x)
        result.append(data["href"]+"|"+data["title"]+"|"+data.text)
    return result[::-1]

def download(url,dir1,dir2):
    req=requests.get(url,headers=ua).text
    parsing=bs(req,"html.parser").find_all("div", {"id":"all","style":""})
    parsing=re.findall(r'<img alt="(.*?)" class="img-responsive" data-src="(.*?)"',str(parsing))
    for x in parsing:
        page=x[0]
        img=x[1]
        path=f"/sdcard/maid/{dir1}/{dir2}/{page}.jpg"
        if not "https:" in img:
           img="https:"+img
        res=requests.get(img,headers=ua)
        with open(path,"wb") as sv:
             sv.write(res.content)
        loading()


#MainMenu
def menu(manga):
    data=[]
    for i,x in enumerate(manga):
        result=x.split("|")
        print(f"{W}({rgb}{i+1}{W}) {rgb}{result[0]}")
        data.append(result[1])
    print(f"{R}---------------------------------------")
    try:
        pilih=int(input(f"{W}>>> {rgb}"))
        print(f"{R}---------------------------------------")
        folder1=data[pilih-1]
        list_ch=get_chapter(data[pilih-1])
        if pilih == 0:
           exit(f"{er} Exit : Thanks for using my tools")
    except IndexError:
        exit(f"{er} Pilih yang bener")
    except ValueError:
        exit(f"{er} Pilih sesuai nomor")
    print(f"{fr} Total chapter :{rgb} {len(list_ch)}")
    print(f"{R}---------------------------------------")
    try:
        from_ch=int(input(f"{pr}Download From Chapter : {rgb}"))
        to_ch=int(input(f"{pr}Download To Chapter   : {rgb}"))
        print(f"{R}---------------------------------------")
    except ValueError:
        exit(f"{er} Wrong!")
    try:
        os.mkdir(os.path.join("/sdcard/maid",folder1))
    except FileExistsError:
        with open(f"/sdcard/maid/{folder1}/plugin.txt","w") as sv:
             sv.write("Cuma file tambahan")
    with ThreadPoolExecutor(max_workers=99) as ex:
         for x in list_ch[from_ch-1:to_ch]:
             x=x.split("|")
             folder2=x[2]
             try:
                os.mkdir(os.path.join("/sdcard/maid/"+folder1,folder2))
             except FileExistsError:
                with open(f"/sdcard/maid/{folder1}/{folder2}/plugin.txt","w") as sv:
                     sv.write("Cuma file tambahan")
             ex.submit(download,(x[0]),(folder1),(folder2))
    print(f"\r{pr} Download...{W}({rgb}✓{W})",end=" ")
    print(f"\n{R}---------------------------------------")
    exit(f"{W}[{rgb}+{W}] Result : {rgb}/sdcard/maid/{folder1}")






if __name__=="__main__":
    ua={"user-agent":"Mozilla/5.0 (Linux; Android 9; Redmi 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"}
    baner()
    try:
       os.mkdir(os.path.join("/sdcard","maid"))
    except FileExistsError:
       with open("/sdcard/maid/plugin.txt","w") as sv:
           sv.write("Cuma file tambahan")
    title=input(f"{pr} Title : {rgb}")
    print(f"{R}---------------------------------------")
    search=find_manga(title)
    if len(search) <= 0:
       exit(f"{er} Manga tidak tersedia")
    menu(search)
