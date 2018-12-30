# -*- coding:utf-8 -*-
import sys
from tkinter import *

""""
Implementation of simplex algorithm by Santiago Blasco Arnaiz
"""

"""
Array containing all the texts printed by the program to facilitate its translation and change.
"""
texts = ['Las inecuaciones no están escritas correctamente.',
         'Función a maximizar',
         'Función a minimizar']

"""
Correct the format and syntax of the string introduced. If it contains non typical characters of an inequation throws an error.
Param: ineq, string inequation writed by user in string format.
Return: string formed by the inequation introduced without containing spaces or syntactic errors.
"""
def inequationsInput(ineq):
    print(ineq)
    corrected = ''
    for char in ineq:
        cod = ord(char)
        if (cod >= ord('0') and cod <= ord('9') or cod >= ord('A') and cod <= ord('Z') or cod >= ord('a') and cod <= ord('z')
            or cod == ord('-') or cod == ord('<') or cod == ord('>') or cod == ord('=') or cod == ord('.')):
            corrected += char
        elif(cod != ord(' ') and cod != ord('+')):
            print (chr(cod))
            print(texts[0])
            sys.exit()
        
    return corrected

"""
Create an array whose columns are variables, values and limit of an inequation.
Param: ineq, string formed by values,variables, innequality and limit.
Param: variables, array that contains the variables of the function.
Return: Array formed by three rows, variables, values and limit.
"""
def ineqToVecs(ineq,variables):
    ineqArray = [[],[],[]]
    for var in variables:
        ineqArray[0].append(var)
        ineqArray[1].append(0)
        
    number = ''
    for char in ineq:
        if (ord(char) >= ord('0') and ord(char) <= ord('9') or char == '-' or char == '.'):
            number += char
            
        elif(char == '=' or char == '<' or char == '>'):
            if(char == '='):
                ineqArray[2].append(float(ineq[ineq.index(char)+1:]))
                break
            elif(char == '>'):                          #Append -1 if is >, 1 if is <
                ineqArray[1] = [-1] + ineqArray[1]
            else:
                ineqArray[1] = [1] + ineqArray[1]
        else:
            if(number == '' or number == '-'):
                number = number + '1'
            ineqArray[1][ineqArray[0].index(char)] = float(number)
            number = ''

    return ineqArray

"""
Converts the function string in an array and alocates it to functionArray.
Param: function, string function writed by user in string format.
Return: array formed by two rows, variables and its values.
"""
def functionToArray(function):
    functionArray = [[],[]]
    function = inequationsInput(function)
    function = function[2:] #eliminate the equality of function
    number = ''
    for char in function:
        if (ord(char) >= ord('0') and ord(char) <= ord('9') or char == '-' or char == '.'):
            number += char
        else:
            functionArray[0].append(char)
            if(number == '' or number == '-'):
                number = number + '1'   #withot number means that the number is 1 or -1
            number = float(number)
            functionArray[1].append(number)
            
            number = ''
    return functionArray

"""
Calculates the optimal solution of the problem posed by the function and the inequacuations.
Param: function, the function to be optimized written as a bidimensional array, first row: variables, second row: values.
Param: inequations, restrictions for the function written as an array that contains bidimensional arrays, first row: values of variables, second row: value of inequality.
"""
def simplex(function,inequations):
    global maximize
    targetVar = []
    targetVal = []
    
    solVar = []
    solVal = []
    varVal = []
    
    variables = []
    
    control = []
    
    a = 0
    b = 0
    
    targetVar += function[0]    #Variables
    targetVal += function[1]    #Values
    
    for i in range(len(inequations)):   
        slackVar = 'S' + str(i)
        ident = '0'*i + '1' + '0'*(len(inequations)-1-i) #Creates the slack variables and its values (identity matrix)
        targetVar.append(slackVar)
        targetVal.append(0.0)
        
        solVar.append(slackVar)
        solVal.append(inequations[i][1][0]) #Independet term
        varVal.append(0)
        
        variables.append(inequations[i][0]) #Values of variables in inequations
        
        for j in ident:
            num = float(j)
            variables[i].append(num)    
    
    sum = []
    for i in range(len(targetVal)):
        sumatory = 0
        for j in range(len(inequations)):   #Calculates that utility that wasnt perceived in the solution
            sumatory += variables[j][i]*varVal[j]
        control.append(targetVal[i] - sumatory)
        sum.append(sumatory)
    profit = 0
    ####Aqui empieza el algoritmo como tal####
    while(allNegatives(control) == False):
        
        print ('Target variables',targetVar)
        print ('Target values',targetVal)
        
        print('Solution variables',solVar)
        print('Solution values',solVal)
        print('Valores variables',varVal)
        print('Variables',variables)
        print('Control',control)
        print("##############STEP##############")
        
        a = majorOf(control)
        
        divisions = []
        for i in range(len(solVal)):
            if (variables[i][a] > 0):
                div = solVal[i]/variables[i][a]
            else:
                div = 'NA'     #When we cant divide we give a value that doesnt matter
            divisions.append(div)
        
        window = Tk()
        l1=Label(window,text="   Cj   "+" ")
        l1.grid(row=0,column=1)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="Cb"+" ")
        l1.grid(row=1,column=0)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="Variable\n solución"+" ")
        l1.grid(row=1,column=1)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="Solución"+" ")
        l1.grid(row=1,column=2)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="Zj"+" ")
        l1.grid(row=2+len(solVar),column=1)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="Cj-Zj"+" ")
        l1.grid(row=3+len(solVar),column=1)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text=str(profit)+" ", fg="red",font=("Courier",20))
        l1.grid(row=3+len(solVar),column=2)
        
        l1=Label(window,text="Divisiones"+" ")
        l1.grid(row=1,column= 3 + len(targetVal))
        l1.config(font=("Courier",20))
        
        for i in range(len(targetVal)):
            
            l1=Label(window,text="%.2f"%targetVal[i]+" ")
            l1.grid(row=0,column= i +3)
            l1.config(font=("Courier",20))
            
            l1=Label(window,text=targetVar[i]+" ")
            l1.grid(row=1,column= i +3)
            l1.config(font=("Courier",20))
            
        for i in range(len(varVal)):
            l1=Label(window,text="%.2f"%varVal[i]+" ")
            l1.grid(row=2+i,column= 0)
            l1.config(font=("Courier",20))
            
            l1=Label(window,text=solVar[i]+" ")
            l1.grid(row=2+i,column= 1)
            l1.config(font=("Courier",20))
            
            l1=Label(window,text="%.2f"%solVal[i]+" ")
            l1.grid(row=2+i,column= 2)
            l1.config(font=("Courier",20))
            
        for i in range(len(variables)):
            for j in range(len(variables[i])):
                l1=Label(window,text="%.2f"%variables[i][j]+" ")
                l1.grid(row=2+i,column= 3 + j)
                l1.config(font=("Courier",20))
                
        for i in range(len(control)):
            l1=Label(window,text="%.2f"%sum[i]+" ")
            l1.grid(row=2+len(solVar),column= 3 + i)
            l1.config(font=("Courier",20))
            
            l1=Label(window,text="%.2f"%control[i]+" ")
            l1.grid(row=3+len(solVar),column= 3 + i)
            l1.config(font=("Courier",20))
        
        for i in range(len(solVal)):
            if(divisions[i]=='NA'):  
                l1=Label(window,text=divisions[i]+" ")
            else:
                l1=Label(window,text="%.2f"%divisions[i]+" ")
            l1.grid(row=2+i,column= 3 + len(targetVal))
            l1.config(font=("Courier",20))
            
        window.mainloop()
        
        b = minorOf(divisions)
        solVar[b] = targetVar[a]
        varVal[b] = targetVal[a]
        
        div = variables[b][a]
        if(div != 0.0):
            for i in range(len(variables[b])):
                variables[b][i] = variables[b][i]/div
            solVal[b] = solVal[b]/div
        
        for i in range(len(variables)):
            if (i != b):
                mult = variables[i][a]
                for j in range(len(variables[i])):
                    variables[i][j] = variables[i][j] - (mult * variables[b][j])
                solVal[i] = solVal[i] - (mult * solVal[b])
                
        for i in range(len(targetVal)):
            sumatory = 0
            
            for j in range(len(inequations)):
                sumatory += variables[j][i]*varVal[j]
            control[i] = targetVal[i] - sumatory
            sum[i] = sumatory
        
        profit = 0
        for i in range(len(solVal)):
            profit += solVal[i] * varVal[i]
    
    
    print ('Target variables',targetVar)
    print ('Target values',targetVal)
    print('Solution variables',solVar)
    print('Solution values',solVal)
    print('Valores variables',varVal)
    print('Variables',variables)
    print('Control',control)
    print('PROFIT',profit)
    
    if maximize:
        for i in range(len(solVar)):
            if (len(solVar[i]) == 1):
                print(solVar[i],'=',solVal[i])
    else:
        for i in range(len(solVar)):
            if (control[len(solVar)+i] != 0.0):
                print(targetVar[i],'=',-1 *control[len(solVar)+i])
    
    
    window = Tk()
    l1=Label(window,text="   Cj   "+"  ")
    l1.grid(row=0,column=1)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Cb"+"  ")
    l1.grid(row=1,column=0)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Variable\n solución"+"  ")
    l1.grid(row=1,column=1)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Solución"+"  ")
    l1.grid(row=1,column=2)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Zj"+"  ")
    l1.grid(row=2+len(solVar),column=1)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Cj-Zj"+"  ")
    l1.grid(row=3+len(solVar),column=1)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text="Fin"+"  ")
    l1.grid(row=3+len(solVar),column=0)
    l1.config(font=("Courier",20))
    
    l1=Label(window,text=str(profit)+"  ", fg="red",font=("Courier",20))
    l1.grid(row=3+len(solVar),column=2)
    
    for i in range(len(targetVal)):
        
        l1=Label(window,text="%.2f"%targetVal[i]+"  ")
        l1.grid(row=0,column= i +3)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text=targetVar[i]+"  ")
        l1.grid(row=1,column= i +3)
        l1.config(font=("Courier",20))
        
    for i in range(len(varVal)):
        l1=Label(window,text="%.2f"%varVal[i]+"  ")
        l1.grid(row=2+i,column= 0)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text=solVar[i]+"  ")
        l1.grid(row=2+i,column= 1)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="%.2f"%solVal[i]+"  ")
        l1.grid(row=2+i,column= 2)
        l1.config(font=("Courier",20))
        
    for i in range(len(variables)):
        for j in range(len(variables[i])):
            l1=Label(window,text="%.2f"%variables[i][j]+"  ")
            l1.grid(row=2+i,column= 3 + j)
            l1.config(font=("Courier",20))
            
    for i in range(len(control)):
        l1=Label(window,text="%.2f"%sum[i]+"  ")
        l1.grid(row=2+len(solVar),column= 3 + i)
        l1.config(font=("Courier",20))
        
        l1=Label(window,text="%.2f"%control[i]+"  ")
        l1.grid(row=3+len(solVar),column= 3 + i)
        l1.config(font=("Courier",20))
        
    window.mainloop()

"""
Check that all elements of the vector are negative.
Param:Vector to evaluates
Return:True if all are negatives or False if not.
"""
def allNegatives(vector):
    flag = True
    for i in vector:
        if (i > 0):
            flag = False
    return flag

"""
Check that all elements of the vector are positive.
Param:Vector to evaluates
Return:True if all are positives or False if not.
"""
def allPositives(vector):
    flag = True
    for i in vector:
        if (i < 0):
            flag = False
    return flag

"""
Search the biggest element in a vector.
Param:vector, vector to look for.
Return:biggest, the index of the biggest element of the vector.
"""
def majorOf(vector):
    major = 0
    for i in range(len(vector)):
        if(vector[i] != 'NA' and vector[major] != 'NA'):
            if(vector[i] >= vector[major]):
                major = i
        elif(vector[i] == 'NA' and vector[major] == 'NA'):
            major +=1
    return major

"""
Search the smallest element in a vector.
Param:vector, vector to look for.
Return:biggest, the index of the smallest element of the vector.
"""
def minorOf(vector):
    minor = 0
    for i in range(len(vector)):
        if(vector[i] != 'NA' and vector[minor] != 'NA'):
            if(vector[i] <= vector[minor]):
                minor = i
        elif(vector[i] == 'NA' and vector[minor] == 'NA'):
            minor += 1
            
    return minor

"""
Change the inequality of the inequations, if you want to maximize all are changed to less, if you want to minimize all are changed to lower
Param: ineqs, inequations to change written as an array that contains bidimensional arrays, first row: variables, second row: values of variables, third row: value of inequality.
Return: ineqs, inequations changed.
"""
def changeIneqs(ineqs):
    if maximize:
        comp = -1
    else:
        comp = 1
    for i in range(len(ineqs)):
        if(ineqs[i][1][0] == comp):
            for j in range(len(ineqs[i][1])):
                ineqs[i][1][j] = ineqs[i][1][j] * -1
            ineqs[i][2][0] = ineqs[i][2][0] * -1
        del ineqs[i][1][0]
    return ineqs

"""
Change the minimization problem for a maximization problem.
Param: problem, array that contains the function an its inequations.
Return: problem, array that contains the function an its inequations changed.
"""
def changeToMax(problem):
    var = 65
    solutions = []
    values = []
    variables = problem[1][0][0]
    
    for i in range(len(problem[1])):
        del problem[1][i][0]
        values.append(problem[1][i][0])
        solutions.append(problem[1][i][1][0])
    
    values = list(map(list, zip(*values)))
    
    while(len(variables)< len(solutions)):
        if not chr(var) in variables:
            variables.append(chr(var))
        var+=1
    
    function = [variables,solutions]
    
    for i in range(len(values)):
        values[i]= [values[i],[problem[0][1][i]]]
        
    problem[0] = function
    problem[1] = values
    return problem

#Max
#cadenaFunction = 'Z= 1000 X + 500 Y + 2500 Z'
#cadenaIneqs = ['100X + 80Y<= 200','90X + 50 Y + 100 Z<= 250','30X +100Y+ 40Z <= 180']

#Max
#cadenaFunction = 'Z= 20000 X + 20000 Y + 20000 Z + 20000 W'
#cadenaIneqs = ['2X + 1Y + 1Z + 2W <= 24','2X + 2Y + 1Z <= 20','2Z + 2W <= 20','4W <= 16']

#Min
#cadenaFunction = 'Z= 24 X + 20 Y + 20 Z + 16 W'
#cadenaIneqs = ['2X +2Y>= 20000','X + 2Y>= 20000','+X +Y +2Z >= 20000','+2X +2Z +4W >= 20000']

#Min
cadenaFunction = 'Z= 425 X + 525 Y + 475 Z + 500 W'
cadenaIneqs = ['X + Y <= 120','Z+W<= 250','X+Z>=200','Y+W>=150']

#cadenaFunction = 'Z= 5 X + 4 Y + 3 Z'
#cadenaIneqs = ['2X + 3Y + 1Z <= 5','4X + Y + 2Z <= 11','3X + 4Y + 2Z <= 8']

#cadenaFunction = 'Z= 50x + 40 y'
#cadenaIneqs = ['x + 1.5y <= 750','2x + y <= 1000']


#cadenaFunction = 'Z= 6.5x + 7y'
#cadenaIneqs = ['2x + 3y <= 600','x + y<= 500','2x + y<= 400','x>=0','y>=0']

#cadenaFunction = 'Z= 30x + 50y'
#cadenaIneqs = ['x + 3y <= 200','x + y<= 100','x >= 20','y>=10']

#Min
#cadenaFunction = 'Z= 30x + 40 y'
#cadenaIneqs = ['20x + 30y >= 3000','40x + 30 y >= 4000','x>=0','y>=0']

#Max
#cadenaFunction = 'Z= x -3y + 3z'
#cadenaIneqs = ['3x-y+2z<=7','-2x - 4 y<=12','-4x+3y+8z<=10']

#Min
#cadenaFunction = 'Z= 3x + 9y'
#cadenaIneqs = ['2x+y >=8','x+2y >=8']

#Min
#cadenaFunction = 'Z= 30x + 40y'
#cadenaIneqs = ['20x+30y>=3000','40x+30y>=4000','x>=0','y>=0']

#Min
#cadenaFunction = 'Z= 10x + 30 y'
#cadenaIneqs = ['x + 5y >= 15','5x + y >= 15','x>=0','y>=0']

#Min
#cadenaFunction = 'Z= 3x+2y'
#cadenaIneqs = ['2x+y>=6','x+y>=4']

#No funciona NA en todas
#cadenaFunction = 'Z= 30x + 40y'
#cadenaIneqs = ['20x+30y>=3000','40x+30y>=4000']

#Min
#cadenaFunction = 'Z= 0.12x + 0.15y'
#cadenaIneqs = ['60x+60y>=300','12x+6y>=36','10x+30y>=90']


"""
Indicates whether to maximize(True) or minimize(False).
"""
maximize = False

if maximize:
    print(texts[1])
else:
    print(texts[2])
functionArray = functionToArray(cadenaFunction)


arrayIneqs = []
print('\nInecuaciones')
for i in cadenaIneqs:
    arrayIneqs.append(ineqToVecs(inequationsInput(i),functionArray[0]))
arrayIneqs = changeIneqs(arrayIneqs)
problem = [functionArray,arrayIneqs]
if maximize:
    for i in range(len(problem[1])):
        del problem[1][i][0]
else:
    changeToMax(problem)
    
simplex(problem[0],problem[1])
