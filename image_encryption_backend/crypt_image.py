######################## IMPORTS #####################################
from PIL import Image
# import tkinter as tk
# from tkinter import filedialog
import hashlib
import binascii
import textwrap
import cv2
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from importlib import reload
from bisect import bisect_left as bsearch
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

dna={}
dna["00"]="A"
dna["01"]="T"
dna["10"]="G"
dna["11"]="C"
dna["A"]=[0,0]
dna["T"]=[0,1]
dna["G"]=[1,0]
dna["C"]=[1,1]
#DNA xor
dna["AA"]=dna["TT"]=dna["GG"]=dna["CC"]="A"
dna["AG"]=dna["GA"]=dna["TC"]=dna["CT"]="G"
dna["AC"]=dna["CA"]=dna["GT"]=dna["TG"]="C"
dna["AT"]=dna["TA"]=dna["CG"]=dna["GC"]="T"
# Maximum time point and total number of time points
tmax, N = 100, 10000

# import tkinter as tk
# from tkinter import filedialog

# def image_selector():
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window

#     file_path = filedialog.askopenfilename(title="Select an image file")
#     if file_path:
#         print("Image loaded:", file_path)
#         return file_path
#     else:
#         print("Error: No image selected!")
#         return None

# # Example usage:
# selected_image_path = image_selector()


def split_into_rgb_channels(image):
    red = image[:,:,2]
    green = image[:,:,1]
    blue = image[:,:,0]
    return red, green, blue

x0, y0, z0 = 0, 0, 0
def securekey(iname):
    img = Image.open(iname)
    m, n = img.size
    print("pixels: {0}  width: {2} height: {1} ".format(m * n, m, n))
    pix = img.load()
    plainimage = list()

    for y in range(n):
        for x in range(m):
            for k in range(0, 3):
                # Add random noise to pixel values
                pixel_value = pix[x, y][k]
                noise = random.randint(-10, 10)  # Adjust the range of noise as needed
                modified_pixel_value = max(0, min(255, pixel_value + noise))  # Ensure the pixel value is within [0, 255]
                plainimage.append(modified_pixel_value)

    # Introduce randomness by shuffling the list before hashing
    random.shuffle(plainimage)

    key = hashlib.sha256()
    key.update(bytearray(plainimage))
    return key.hexdigest(), m, n

x = 0.1
y = 0.1
z = 0.1

def baker_map(x, y, z):
    x_next = 2 * x if x < 0.5 else 2 * x - 1
    y_next = 0.5 * y if x < 0.5 else 0.5 * y + 0.5
    z_next = z  # Assuming z remains unchanged
    return x_next, y_next, z_next


def update_baker(key, x, y, z):
    key_bin = bin(int(key, 16))[2:].zfill(256)
    k = {}
    key_32_parts = textwrap.wrap(key_bin, 8)
    num = 1
    for i in key_32_parts:
        k["k{0}".format(num)] = i
        num = num + 1

    t1 = t2 = t3 = 0
    for i in range(1, 12):
        t1 = t1 ^ int(k["k{0}".format(i)], 2)
    for i in range(12, 23):
        t2 = t2 ^ int(k["k{0}".format(i)], 2)
    for i in range(23, 33):
        t3 = t3 ^ int(k["k{0}".format(i)], 2)

    x_next = x + t1 / 256
    y_next = y + t2 / 256
    z_next = z + t3 / 256

    return x_next, y_next, z_next

# Generate a key from an image
# key, width, height = securekey(selected_image_path)
# Assuming your update_baker function now accepts three arguments
# x = 0.1
# y = 0.1
# z = 0.1
# Update the Baker's map with the generated key
x_values = [x]
y_values = [y]
z_values = [z]

# for _ in range(width * height):
#     x, y, z = update_baker(key, x, y, z)  # Update x, y, and z
#     x_values.append(x)
#     y_values.append(y)
#     z_values.append(z)


# Now, x_values and y_values contain the trajectory of the Baker's map updated with the key
def decompose_matrix(iname):
    image = cv2.imread(iname)
    blue,green,red = split_into_rgb_channels(image)
    for values, channel in zip((red, green, blue), (2,1,0)):
        img = np.zeros((values.shape[0], values.shape[1]), dtype = np.uint8)
        img[:,:] = (values)
        if channel == 0:
            B = np.asmatrix(img)
        elif channel == 1:
            G = np.asmatrix(img)
        else:
            R = np.asmatrix(img)
    return B,G,R

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


def key_matrix_encode(key,b):
    #encoded key matrix
    b = np.unpackbits(b,axis=1)
    m,n = b.shape
    key_bin = bin(int(key, 16))[2:].zfill(256)
    Mk = np.zeros((m,n),dtype=np.uint8)
    x=0
    for j in range(0,m):
            for i in range(0,n):
                Mk[j,i]=key_bin[x%256]
                x+=1

    Mk_enc=np.chararray((m,int(n/2)))
    idx=0
    for j in range(0,m):
        for i in range(0,n,2):
            if idx==(n/2):
                idx=0
            Mk_enc[j,idx]=dna["{0}{1}".format(Mk[j,i],Mk[j,i+1])]
            idx+=1
    Mk_enc=Mk_enc.astype(str)
    return Mk_enc

def xor_operation(b,g,r,mk):
    m,n = b.shape
    bx=np.chararray((m,n))
    gx=np.chararray((m,n))
    rx=np.chararray((m,n))
    b=b.astype(str)
    g=g.astype(str)
    r=r.astype(str)
    for i in range(0,m):
        for j in range (0,n):
            bx[i,j] = dna["{0}{1}".format(b[i,j],mk[i,j])]
            gx[i,j] = dna["{0}{1}".format(g[i,j],mk[i,j])]
            rx[i,j] = dna["{0}{1}".format(r[i,j],mk[i,j])]

    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    return bx,gx,rx

def gen_chaos_seq(key,m, n):
    global x0, y0, z0
    N = m * n * 4
    x = np.zeros(N)
    y = np.zeros(N)
    z = np.zeros(N)

    for i in range(N):
        x0, y0, z0 = update_baker(key, x0, y0, z0)  # Assuming update_baker takes three arguments
        x[i] = x0
        y[i] = y0
        z[i] = z0

    return x, y, z
x0 = np.array([x0])
y0 = np.array([y0])
z0 = np.array([z0])


def parallel_sequence_indexing(x, y, z):
    n = len(x)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(np.argsort, arr) for arr in [x, y, z]]

    k2_x = np.empty(n, dtype=np.uint32)
    k2_y = np.empty(n, dtype=np.uint32)
    k2_z = np.empty(n, dtype=np.uint32)

    results = list(as_completed(futures))

    k2_x[results[0].result()] = np.arange(n, dtype=np.uint32)
    k2_y[results[1].result()] = np.arange(n, dtype=np.uint32)
    k2_z[results[2].result()] = np.arange(n, dtype=np.uint32)

    return k2_x, k2_y, k2_z


# Parameters for the Baker's map
x0 = 0.1
y0 = 0.1
z0 = 0.1  # Assuming your Baker's map now accepts three initial conditions

# Generate chaotic sequences using the Baker's map
# x_seq, y_seq, z_seq = gen_chaos_seq(10, 10)

# Index the sequences in parallel
# fx, fy, fz = parallel_sequence_indexing(x_seq, y_seq, z_seq)

# Now you can use fx, fy, and fz for further processing or analysis
def scramble(fx,fy,fz,b,r,g):
    p,q=b.shape
    size = p*q
    bx=b.reshape(size).astype(str)
    gx=g.reshape(size).astype(str)
    rx=r.reshape(size).astype(str)
    bx_s=np.chararray((size))
    gx_s=np.chararray((size))
    rx_s=np.chararray((size))

    for i in range(size):
            idx = fz[i]
            bx_s[i] = bx[idx]
    for i in range(size):
            idx = fy[i]
            gx_s[i] = gx[idx]
    for i in range(size):
            idx = fx[i]
            rx_s[i] = rx[idx]
    bx_s=bx_s.astype(str)
    gx_s=gx_s.astype(str)
    rx_s=rx_s.astype(str)

    b_s=np.chararray((p,q))
    g_s=np.chararray((p,q))
    r_s=np.chararray((p,q))

    b_s=bx_s.reshape(p,q)
    g_s=gx_s.reshape(p,q)
    r_s=rx_s.reshape(p,q)
    return b_s,g_s,r_s

def scramble_new(fx,fy,fz,b,g,r):
    p,q=b.shape
    size = p*q
    bx=b.reshape(size)
    gx=g.reshape(size)
    rx=r.reshape(size)

    bx_s=b.reshape(size)
    gx_s=g.reshape(size)
    rx_s=r.reshape(size)

    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    bx_s=bx_s.astype(str)
    gx_s=gx_s.astype(str)
    rx_s=rx_s.astype(str)

    for i in range(size):
            idx = fz[i]
            bx_s[idx] = bx[i]
    for i in range(size):
            idx = fy[i]
            gx_s[idx] = gx[i]
    for i in range(size):
            idx = fx[i]
            rx_s[idx] = rx[i]

    b_s=np.chararray((p,q))
    g_s=np.chararray((p,q))
    r_s=np.chararray((p,q))

    b_s=bx_s.reshape(p,q)
    g_s=gx_s.reshape(p,q)
    r_s=rx_s.reshape(p,q)

    return b_s,g_s,r_s

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

def xor_operation_new(b,g,r,mk):
    m,n = b.shape
    bx=np.chararray((m,n))
    gx=np.chararray((m,n))
    rx=np.chararray((m,n))
    b=b.astype(str)
    g=g.astype(str)
    r=r.astype(str)
    for i in range(0,m):
        for j in range (0,n):
            bx[i,j] = dna["{0}{1}".format(b[i,j],mk[i,j])]
            gx[i,j] = dna["{0}{1}".format(g[i,j],mk[i,j])]
            rx[i,j] = dna["{0}{1}".format(r[i,j],mk[i,j])]

    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    return bx,gx,rx

def recover_image(b,g,r,iname):
    img = cv2.imread(iname)
    img[:,:,2] = r
    img[:,:,1] = g
    img[:,:,0] = b
    cv2.imwrite(("enc.jpg"), img)
    print("saved ecrypted image as enc.jpg")
    return img

def decrypt(img,fx,fy,fz,fp,Mk,bt,gt,rt):
    r,g,b=split_into_rgb_channels(img)
    p,q = rt.shape
    benc,genc,renc=dna_encode(b,g,r)
    bs,gs,rs=scramble_new(fx,fy,fz,benc,genc,renc)
    bx,rx,gx=xor_operation_new(bs,gs,rs,Mk)
    blue,green,red=dna_decode(bx,gx,rx)
    green,red = red, green
    img=np.zeros((p,q,3),dtype=np.uint8)
    img[:,:,0] = red
    img[:,:,1] = green
    img[:,:,2] = blue
    cv2.imwrite(("Recovered.jpg"), img)

#program exec9
def image_encrypt(image_path):
    print(image_path)
    key,m,n = securekey(image_path)
    x,y,z=gen_chaos_seq(key,m,n)
    update_baker(key,x,y,z)
    blue,green,red=decompose_matrix(image_path)
    blue_e,green_e,red_e=dna_encode(blue,green,red)
    Mk_e = key_matrix_encode(key,blue)
    blue_final, green_final, red_final = xor_operation(blue_e,green_e,red_e,Mk_e)
    fx,fy,fz=parallel_sequence_indexing(x,y,z)
    blue_scrambled,green_scrambled,red_scrambled = scramble(fx,fy,fz,blue_final,red_final,green_final)
    b,g,r=dna_decode(blue_scrambled,green_scrambled,red_scrambled)
    image=recover_image(b,g,r,image_path)
    return image, key

def image_decrypt(decrypt_image, image_path, key):
    print(image_path)
    # key,m,n = securekey(image_path)
    m,n = Image.open(image_path).size
    x,y,z=gen_chaos_seq(key,m,n)
    update_baker(key,x,y,z)
    blue,green,red=decompose_matrix(image_path)
    blue_e,green_e,red_e=dna_encode(blue,green,red)
    Mk_e = key_matrix_encode(key,blue)
    blue_final, green_final, red_final = xor_operation(blue_e,green_e,red_e,Mk_e)
    
    fx,fy,fz=parallel_sequence_indexing(x,y,z)
    blue_scrambled,green_scrambled,red_scrambled = scramble(fx,fy,fz,blue_final,red_final,green_final)
    # b,g,r=dna_decode(blue_scrambled,green_scrambled,red_scrambled)
    
    image = decrypt(decrypt_image,fx,fy,fz,image_path,Mk_e,blue,green,red)
    return image
