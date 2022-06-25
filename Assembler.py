# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:33:53 2021

@author: Mohammad Saleh
"""
import numpy as np
import pandas as pd
import math
import os

data = pd.read_excel (r'AppendixA.xlsx')
Mnemonic = pd.DataFrame(data, columns= ['Mnemonic'])
Mnemonic =np.asarray(Mnemonic)
Opcode = pd.DataFrame(data, columns= ['Opcode'])
Opcode = np.asarray(Opcode)



def isTheMnemonicIsExist(x):
    exist=np.where(Mnemonic==x)
    if(len(exist[0])==0):
       return False
    else:
        return True



def isTheLabelIsExist(symTab,x):
    exist=np.where(symTab==x)
    if(len(exist[0])==0):
       return False
    else:
        return True
def isTheLitralIsExist(literals,x):
    exist=np.where(literals==x)
    if(len(exist[0])==0):
       return False
    else:
        return True
           
def star(symTab):
    exist=np.where(symTab=='*')
    if(len(exist[0])==0):
       return -1
    else:
        return exist[0][0]
def toDecimal(x):
    x=str(x)
    value=x[::-1]
    sum=0
    for i in range(len(value)):
        if(value[i]=='A'):
            sum+=pow(16,i)*10
        elif(value[i]=='B'):
            sum+=pow(16,i)*11
        elif (value[i]=='C'):
            sum+=pow(16,i)*12
        elif (value[i]=='D'):
            sum+=pow(16,i)*13
        elif (value[i]=='E'):
            sum+=pow(16,i)*14
        elif (value[i]=='F'):
            sum+=pow(16,i)*15
        else: 
            sum+=pow(16,i)*int(value[i])
    return sum

def pass1(inputFile, outputFile):
    initialLocator=0
    pcLoc=initialLocator
    currentLine=[]
    symTab=np.array([])
    currantSymTab=[]
    literals=np.array([])
    intermadiateData = np.array([])
    file = open(inputFile,"r")
    for x in file:        
        line=x.split()
        if(x[0]!='.'):
            if(x[0]!=' '):
                    if(line[1]=='START'):
                        initialLocator=toDecimal(line[2])
                        pcLoc= initialLocator
                    if(isTheLabelIsExist(symTab,line[0])):
                        print("Dublicate symbol")
                        exit
                    currantSymTab.append(line[0])
                    currantSymTab.append(hex(pcLoc)[2:].upper())
                    symTab=np.append(symTab,currantSymTab)
                    currantSymTab=[]
                    
                    currentLine.append(hex(pcLoc)[2:].upper())
                    currentLine.append(line[0])
                    currentLine.append(line[1])
                    currentLine.append(line[2])
                    intermadiateData= np.append(intermadiateData,currentLine)
                    currentLine=[]
                    if(isTheMnemonicIsExist(line[1])):
                        pcLoc=pcLoc+3
                        if(line[2][0]=='='):
                            literals=np.append(literals,line[2])
                        
                    elif (line[1]=="WORD"):
                        pcLoc=pcLoc+3
                    elif (line[1]=="RESW"):
                        pcLoc+=(3*int(line[2]))
                    elif (line[1]=="RESB"):
                        pcLoc+=int(line[2])
                    elif (line[1]=="BYTE"):
                        if(line[2][0]=='C'):
                            pcLoc+=len(line[2])-3
                        else:
                            pcLoc+=int(math.ceil((len(line[2])-3)/2))
                    elif(line[1]=='START'):
                        continue  
                    elif(line[1]=='END'):
                        intermadiateData[len(intermadiateData)-4]=''
                        for j in literals:
                                if(star(symTab)==-1):
                                    currantSymTab.append('*')
                                    currantSymTab.append(hex(pcLoc)[2:].upper())
                                    symTab=np.append(symTab,currantSymTab)
                                    currantSymTab=[]
                                else:
                                    symTab[star(symTab)+1]=hex(pcLoc)[2:].upper()
                                currentLine.append(hex(pcLoc)[2:].upper())
                                currentLine.append('*')
                                currentLine.append(j)
                                currentLine.append('')
                                intermadiateData= np.append(intermadiateData,currentLine)
                                currentLine=[]
                                if(j[1]=='C'):
                                    pcLoc+=len(j)-4
                                else:
                                    pcLoc+=int(math.ceil((len(j)-4)/2))
                        literals=np.array([])  
                    else:
                        print("Invalid operations code",line[1])
                        exit
            else:
                if(line[0]=='LTORG'):
                    currentLine.append('')
                    currentLine.append('')
                    currentLine.append("LTORG")
                    currentLine.append('')
                    intermadiateData= np.append(intermadiateData,currentLine)
                    currentLine=[]
                    
                    for j in literals:
                        if(star(symTab)==-1):
                            currantSymTab.append('*')
                            currantSymTab.append(hex(pcLoc)[2:].upper())
                            symTab=np.append(symTab,currantSymTab)
                            currantSymTab=[]
                        else:
                            symTab[star(symTab)+1]=hex(pcLoc)[2:].upper()
                        currentLine.append(hex(pcLoc)[2:].upper())
                        currentLine.append('*')
                        currentLine.append(j)
                        currentLine.append('')
                        intermadiateData= np.append(intermadiateData,currentLine)
                        currentLine=[]
                        if(j[1]=='C'):
                            pcLoc+=len(j)-4
                        else:
                            pcLoc+=int(math.ceil((len(j)-4)/2))
                    literals=np.array([])       
                else:
                    currentLine.append(hex(pcLoc)[2:].upper())
                    currentLine.append('')
                    currentLine.append(line[0])
                    if(line[0]=='RSUB'):
                         currentLine.append('')
                    else:
                        currentLine.append(line[1])
                    intermadiateData= np.append(intermadiateData,currentLine)
                    currentLine=[]
                    if(isTheMnemonicIsExist(line[0])):
                        pcLoc=pcLoc+3
                        if(line[0]=='RSUB'):
                            intermadiateData[len(intermadiateData)-1]=''
                        elif(line[1][0]=='='):
                            if(not isTheLitralIsExist(literals,line[1])):
                                literals =np.append(literals,line[1])
                                
                
                    elif (line[0]=="WORD"):
                        pcLoc=pcLoc+3
                    elif (line[0]=="RESW"):
                        pcLoc+=(3*line[1])
                    elif (line[0]=="RESB"):
                        pcLoc+=line[2]
                    elif (line[0]=="BYTE"):
                        if(line[1][0]=='C'):
                            pcLoc+=len(line[1])-3
                        else:
                            pcLoc+=int(math.ceil((len(j)-3)/2))
                    
                    elif(line[0]=='END'):
                        intermadiateData[len(intermadiateData)-4]=''
                        for j in literals:
                            if(star(symTab)==-1):
                                currantSymTab.append('*')
                                currantSymTab.append(hex(pcLoc)[2:].upper())
                                symTab=np.append(symTab,currantSymTab)
                                currantSymTab=[]
                            else:
                                symTab[star(symTab)+1]=hex(pcLoc)[2:].upper()
                            currentLine.append(hex(pcLoc)[2:].upper())
                            currentLine.append('*')
                            currentLine.append(j)
                            currentLine.append('')
                            intermadiateData= np.append(intermadiateData,currentLine)
                            currentLine=[]
                            if(j[1]=='C'):
                                pcLoc+=len(j)-4
                            else:
                                pcLoc+=int(math.ceil((len(j)-4)/2))
                            literals=np.array([])
                    else:
                        print("Invalid operations code")
                        exit  
                
                
                        
            
        
    file.close()
    file = open(outputFile,"w")
    for i in intermadiateData.reshape(-4,4):
        for j in i:
           if(j==' '):
               file.write(j)
           else:
             file.write(j)
             file.write(' ') 
        file.write(' \n')     
    file.write(hex(pcLoc-initialLocator)[2:].upper())     
    file.close()
    print("Program's Name is: ",intermadiateData[1] )
    print("Program's Length is: ",hex(pcLoc-initialLocator)[2:].upper())
    print("LOCCTR: ",hex(pcLoc)[2:].upper())    
    print(symTab.reshape(-2,2))   


def code(x):
    exist=np.where(Mnemonic==x)
    return str(Opcode[exist[0][0]][0]).zfill(2)

def addLit(aux,x):
    for i in aux:
        if(len(i)>=3):
            if(i[1]=='*' and i[2]==x):
                return i[0]
    return -1

def addMn(aux,x):
    for i in aux:
        if(len(i)>=4):
            if(i[1]==x):
                return i[0]   
    return -1

def existX(aux,x,bool,bool2):
        if(bool2==True):
            addMn_2=addMn(aux,x)
        else:
            addMn_2=addLit(aux,x)

        if(addMn_2!=-1):
            d=toDecimal(addMn_2)
            b=bin(d)
            b=b[2:].zfill(16)
            if(bool==True):
                b='1'+b[1:]
            else:
                 b='0'+b[1:]  
            return hex(int(b,2))[2:].upper()
        else: 
            return -1


def pass2(inputFile, outputFile):
       file = open(inputFile,"r")
       aux = []
       aux2=[]
       for x in file:        
            line=x.split()
            for i in line:
                aux2.append(i)
            aux.append(aux2)
            aux2=[]
       theLengthOfProgram=aux.pop(len(aux)-1)   
       for i in aux:
          if(len(i)==4):
              if(i[2]=='START' or i[2]=='RESB' or i[2]=='RESW'):
                  continue
              elif(i[2]=='WORD' or i[2]=='BYTE'):
                  if(i[3][0]=='C'):
                      i.append(''.join(hex(int(str(ord(c))))[2:].upper() for c in i[3][2:-1]) )
                  elif(i[3][0]=='X'):
                      i.append(i[3][2:-1])
                  else: 
                      i.append(str(hex(int(i[3]))[2:]).zfill(6))
              else:
                   if(isTheMnemonicIsExist(i[2])):
                       opcode = code(i[2])
                       if(i[3][-1]=='X' and i[3][-2]):
                              final = existX(aux,i[3][:-2],True,True)
                              if(final!=-1):
                                    opcode = opcode+ final.zfill(4)
                                    i.append(opcode)
                              else:
                                  print("Wrong in ", i[3])
                       elif(i[3][0]=='='):
                           final= existX(aux,i[3],False,False)
                           if(final!=-1):
                               opcode = opcode+ final.zfill(4)
                               i.append(opcode)
                           else:
                               print("Wrong in ", i[3])
                       else:
                           final= existX(aux,i[3],False,True)
                           if(final!=-1):
                               opcode= opcode+final.zfill(4)
                               i.append(opcode)
                           else:
                               print("Wrong in ", i[3])
          elif(len(i)==3):
                   if(isTheMnemonicIsExist(i[1])):
                       opcode = code(i[1])
                       if(i[2][-1]=='X' and i[2][-2]):
                              final = existX(aux,i[2][:-2],True,True)
                              if(final!=-1):
                                    opcode = opcode+ final.zfill(4)
                                    i.append(opcode)
                              else:
                                  print("Wrong in ", i[2])
                       elif(i[2][0]=='='):
                           final= existX(aux,i[2],False,False)
                           if(final!=-1):
                               opcode = opcode+ final.zfill(4)
                               i.append(opcode)
                           else:
                               print("Wrong in ", i[2])
                       else:
                           final= existX(aux,i[2],False,True)
                           if(final!=-1):
                               opcode= opcode+final.zfill(4)
                               i.append(opcode)
                           else:
                               print("Wrong in ", i[2])
                   else:
                        if(i[1]=='*'):
                            if(i[2][1]=='C'):
                                i.append(''.join(hex(int(str(ord(c))))[2:].upper() for c in i[2][3:-1]) )
                            elif(i[2][1]=='X'):
                                i.append(i[2][3:-1])
                            else: 
                                i.append(str(hex(int(i[2][1:]))[2:]).zfill(6))
          elif(len(i)==2):
              if(i[1]=='RSUB'):
                  i.append('4C0000')
       file.close()
       file = open('test.lst',"w")
       for i in aux:
            for j in i:
                file.write(j)
                file.write(' ') 
            file.write(' \n')     
        
       file.close()
       file= open(outputFile,'w')
       arr=[]
       c=0
       for i in aux:
           if(len(i)==4 and i[2]=="START"):
               file.write('H^')
               file.write(i[1].ljust(6))
               file.write('^')
               file.write(i[0].zfill(6))
               file.write('^')
               file.write(theLengthOfProgram[0].zfill(6))
               file.write(' \n') 
           

           else:
               if(len(i)==1 or len(i)==2):
                   continue
               elif(i[2]=="RESW" or i[2]=='RESB'):
                       if(len(arr)==0):
                           continue
                       else:
                           file.write('T^')
                           file.write(arr[0].zfill(6))
                           file.write('^')
                           file.write(hex(int(math.ceil(c*0.5)))[2:].zfill(2).upper())
                           c=0
                           file.write('^')
                           for i in range(len(arr)):
                               if( i==0):
                                   continue
                               elif(i==len(arr)-1):
                                   file.write(arr[i])
                                   file.write(' \n')
                               else:
                                   file.write(arr[i])
                                   file.write('^')
                           arr=[]
               elif(len(arr)==0):
                   arr.append(i[0])
                   arr.append(i[len(i)-1])
                   c=c+len(i[len(i)-1])
               else:
                    if(c+len(i[len(i)-1])<=60):
                         arr.append(i[len(i)-1])
                         c=c+len(i[len(i)-1])
                    else:
                        file.write('T^')
                        file.write(arr[0].zfill(6))
                        file.write('^')
                        file.write(hex(int(math.ceil(c*0.5)))[2:].zfill(2).upper())
                        c=0
                        file.write('^')
                        for j in range(len(arr)):
                            if( j==0):
                                continue
                            elif(j==len(arr)-1):
                                file.write(arr[j])
                                file.write(' \n')
                            else:
                                file.write(arr[j])
                                file.write('^')
                        arr=[]
                        arr.append(i[0])
                        arr.append(i[len(i)-1])
                        c=c+len(i[len(i)-1])
       if(len(arr)>0):
           file.write('T^')
           file.write(arr[0].zfill(6))
           file.write('^')
           file.write(hex(int(math.ceil(c*0.5)))[2:].zfill(2).upper())
           c=0
           file.write('^')
           for j in range(len(arr)):
                if( j==0):
                    continue
                elif(j==len(arr)-1):
                    file.write(arr[j])
                    file.write(' \n')
                else:
                    file.write(arr[j])
                    file.write('^')
       file.write('E^')
       file.write(aux[0][0].zfill(6))  
       file.write(' \n')

data = input()
data = data.split()

if os.path.exists(data[1]):
    if data[0]=="pass1":
        pass1(data[1], data[2])
    elif data[0]=="pass2":
        pass2(data[1], data[2])
    else:
        print("Wrong Input")    

else:
    print("Wrong Input")    






