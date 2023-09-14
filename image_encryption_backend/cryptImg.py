from PIL import Image
import tkinter as tk
from tkinter import filedialog
import hashlib
import numpy as np

dna={}
dna["00"]="A"
dna["01"]="T"
dna["10"]="G"
dna["11"]="C"
dna["A"]=[0,0]
dna["T"]=[0,1]
dna["G"]=[1,0]
dna["C"]=[1,1]

dna["AA"]=dna["TT"]=dna["GG"]=dna["CC"]="A"
dna["AG"]=dna["GA"]=dna["TC"]=dna["CT"]="G"
dna["AC"]=dna["CA"]=dna["GT"]=dna["TG"]="C"
dna["AT"]=dna["TA"]=dna["CG"]=dna["GC"]="T"

tmax, N = 100, 10000

def image_selector():
    path = "NULL"
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    if path!="NULL":
        print("Image loaded!") 
    else:
        print("Error Image not loaded!")
    return path

def split_into_rgb_channels(image):
    red = image[:,:,2]
    green = image[:,:,1]
    blue = image[:,:,0]
    return red, green, blue

def securekey (iname):
    img = Image.open(iname)
    m, n = img.size
    print("pixels: {0}  width: {2} height: {1} ".format(m*n, m, n))
    pix = img.load()          
    plainimage = list()
    for y in range(n):
        for x in range(m):
            for k in range(0,3):
                plainimage.append(pix[x,y][k])    
    key = hashlib.sha256()
    key.update(bytearray(plainimage))
    return key.hexdigest() ,m ,n

def dna_encode(b,g,r):
    
    b = np.unpackbits(b,axis=1)
    g = np.unpackbits(g,axis=1)
    r = np.unpackbits(r,axis=1)
    m,n = b.shape
    r_enc= np.chararray((m,int(n/2)))
    g_enc= np.chararray((m,int(n/2)))
    b_enc= np.chararray((m,int(n/2)))
    
    for color,enc in zip((b,g,r),(b_enc,g_enc,r_enc)):
        idx=0
        for j in range(0,m):
            for i in range(0,n,2):
                enc[j,idx]=dna["{0}{1}".format(color[j,i],color[j,i+1])]
                idx+=1
                if (i==n-2):
                    idx=0
                    break
    
    b_enc=b_enc.astype(str)
    g_enc=g_enc.astype(str)
    r_enc=r_enc.astype(str)
    return b_enc,g_enc,r_enc

def dna_decode(b,g,r):
    m,n = b.shape
    r_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    g_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    b_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    for color,dec in zip((b,g,r),(b_dec,g_dec,r_dec)):
        for j in range(0,m):
            for i in range(0,n):
                dec[j,2*i]=dna["{0}".format(color[j,i])][0]
                dec[j,2*i+1]=dna["{0}".format(color[j,i])][1]
    b_dec=(np.packbits(b_dec,axis=-1))
    g_dec=(np.packbits(g_dec,axis=-1))
    r_dec=(np.packbits(r_dec,axis=-1))
    return b_dec,g_dec,r_dec

if (__name__ == "__main__"):
    file_path = image_selector()
    print(file_path)
    blue_e,green_e,red_e=dna_encode(blue,green,red)
