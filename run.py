import os,sys,time,requests,json
from bs4 import BeautifulSoup as bs
from time import sleep
from colorama import init, Fore, Back
url="https://mangaid.click/"
ses=requests.Session()
ses.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10; Redmi 4A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.50 Mobile Safari/537.36"
result=[]
ch_result=[]
B = Fore.BLUE
W = Fore.WHITE
R = Fore.RED
G = Fore.GREEN
BL = Fore.BLACK
def clear():
    os.system("cls" if os.name == "nt" else "clear")
def baner():
    print(f"\t\t\033[00mManga {R}ID \033[00mDownloader")
    print("\t"+Back.WHITE+Fore.BLACK+"https://ainxbot-id.herokuapp.com/\033[00m")
def search(judul: str) -> list:
    temp=[]
    req=ses.get(url+"search?query="+judul).text
    js=json.loads(req)
    for x in js["suggestions"]:
        jud=x["value"]
        dat=x["data"]
        temp.append((jud,dat))
    return temp
def manga(title: str) -> list:
    temp=[]
    req=ses.get(url+"manga/"+title).text
    res=bs(req,"html.parser").find_all("h5", class_="chapter-title-rtl")
    for data in res:
        manga=data.find("a",href=lambda x: x and "manga" in x)
        name=manga["title"]
        ur=manga["href"]
        total=manga["href"].split("/")[5]
        temp.append((name,ur,total))
    return temp

def lihat(param):
     temp=[]
     req=ses.get(param).text
     res=bs(req,"html.parser").find_all("div", {"id":"all","style":""})
     for data in res:
         img=data.find_all('img')
         for x in img:
             temp.append((x["alt"],x["data-src"]))
     return temp
if __name__=="__main__":
     clear()
     baner()
     print()
     que=input(f"{W}[{G}TITLE{W}]\033[00mKata Kunci? : {G}")
     id=search(que)
     if len(id) <= 0:
        print(f"{W}[{R}INFO{W}]\033[00mtidak dapat menemukan apapun{R}!!\033[00m")
        sleep(2)
        os.system("python run.py")
     print(f"{B}==================================================\033[00m")
     for i,user in enumerate(id):
         result.append((user[0],user[1]))
         print(f"{G}{i+1}{W}. \033[00m{user[0]}")
     print(f"{B}==================================================\033[00m")
     try:
         select=input(f"{W}[{G}ANIME{W}]\033[00mPilih : {G}")
         select=int(select)
     except ValueError:
         print(f"{W}[{R}INFO{W}]\033[00mPilih sesuai nomor{R}!!\033[00m")
         sleep(2)
         os.system("python run.py")
     dir=result[select-1][0]
     tot=manga(result[select-1][1])
     print(f"{B}==================================================\033[00m")
     for i,user in enumerate(tot):
         ch_result.append((user[1],user[2]))
         print(f"{G}{i+1}{W}. \033[00m{user[0]}")
     print(f"{W}[{G}INFO{W}]\033[00mTotal Chapter :{G} {tot[0][2]}")
     print(f"{B}==================================================\033[00m")
     try:
         ch=input(f"{W}[{G}CHAPTER{W}]\033[00mPilih nomor : {G}")
         ch=int(ch)
     except ValueError:
         print(f"{W}[{R}INFO{W}]\033[00mPilih sesuai nomor{R}!!\033[00m")
         sleep(2)
         os.system("python run.py")
     print(f"{B}==================================================\033[00m")
     chdir="Chapter "+ch_result[ch-1][1]
     try:
         f=open("/sdcard/maid/plugins.txt","w")
         f.write("biar ga error!")
     except FileNotFoundError:
         os.system("termux-setup-storage")
         os.mkdir(os.path.join("/sdcard","maid"))
     try:
         f=open("/sdcard/maid/"+dir+"/plugins.txt","w")
         f.write("biar ga error!")
     except FileNotFoundError:
         os.mkdir(os.path.join("/sdcard/maid",dir))
     try:
         f=open("/sdcard/maid/"+dir+"/"+chdir+"/plugins.txt","w")
         f.write("biar ga error!")
     except FileNotFoundError:
         os.mkdir(os.path.join("/sdcard/maid/"+dir,chdir))
     end=lihat(ch_result[ch-1][0])
     for x in end:
         strg=["\033[90m.","\033[90m..","\033[90m...","\033[91m.","\033[91m..","\033[91m..."]
         for o in strg:
             print(f"\r{W}[{G}*{W}]\033[00mWaiting{o}",end="")
             sleep(0.2)
         urls=x[1]
         name=x[0]
         if not "https:" in urls:
              urls="https:"+urls
         resp=requests.get(urls) 
         size=round(int(resp.headers.get("Content-Length"))/1024)   
         with open(f"/sdcard/maid/{dir}/{chdir}/{name}.jpg", 'wb') as f: 
              for data in resp.iter_content(chunk_size=1024):        
                  f.write(data)
     print(f"\n{W}[{G}DONE{W}]\033[00mManga tersimpan di, \n\033[00m-> {G}/sdcard/maid/{dir}/{chdir}.")
     print(f"{B}==================================================\033[00m")
     cblg=input(f"{W}[{G}?{W}]\033[00mCoba Lagi? {W}({G}y{W}/{G}n{W}): {G}")
     if cblg == "y" or cblg == "Y":
        sleep(2)
        os.system("python run.py")
     else:
        sys.exit(f"{W}[{R}EXIT{W}]Dah kontol{R}!!{W}")
