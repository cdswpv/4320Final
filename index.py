import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import re, string

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your secret key'

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        menuSelect = request.form['menu']
        if menuSelect == '':
            flash("Select a redirect option", "error")
        elif menuSelect == '1':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('reserve'))
    return render_template('index.html')

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        passFile = open('passcodes.txt', 'r')
        passList = re.split(', |\n', passFile.read()) #puts the passwords and usernames in a neat list
        while("" in passList): #removes the extra blank string
            passList.remove("")
        
        badInput = True
        count = 0
        for index in passList:
            if (username == passList[count]):
                if (password == passList[count+1]):
                    seatList = getMap()
                    badInput = False
                    passFile.close()
                    break
            count +=1

        passFile.close()
        if badInput:
            flash('Invalid username/password combination', "error")
            return render_template('admin.html')
        else:                   
            return render_template('admin.html', seatList = seatList, totalSales = sales)
    return render_template('admin.html')
    
    

@app.route('/reserve', methods = ['GET', 'POST'])
def reserve():
    seatList = getMap()
    if request.method == 'POST':
        fname = request.form['fname'].strip()
        lname = request.form['lname'].strip()
        row = request.form['row']
        seat = request.form['seat']

        
        if fname == "":
            flash("Enter First Name", "error")
        elif lname == "":
            flash("Enter Last Name", "error")
        elif row == "":
            flash("Choose a Row", "error")
        elif seat == "":
            flash("Choose a Seat", "error")
        elif checkInput(row, seat):
            flash("That seat has already been chosen", "error")
        else:
            row = int(row)
            seat = int(seat)
            ticketConfirmation = [fname, row, seat, reserveSeat(fname, row, seat)]
            return render_template('reservations.html', seatList = seatList, ticketConfirmation = ticketConfirmation)

        
    return render_template('reservations.html', seatList = seatList)

def reserveSeat(fname, row, seat):
    reserveWrite = open('reservations.txt', 'a')

    ticketCode = getTicketCode(fname)

    reserveWrite.write("\n{}, {}, {}, {}".format(fname, row-1, seat-1, ticketCode))
    reserveWrite.close()

    return ticketCode

def getTicketCode(fname):
    code = 'INFOTC4320'
    result = ''
    length = min(len(fname), len(code))
    for char in range(length):
        result += fname[char] + code[char]
    result += fname[length:] + code[length:]
    return result

def checkInput(row, seat):
    busMap = getMap()
    row = int(row)
    seat = int(seat)
    if busMap[row - 1][seat - 1] == "X":
        return True
    else:
        return False

def getMap():
    busMap = [['O','O','O','O'] for row in range(12)]
    x = 0
    reserveFile = open('reservations.txt', 'r')
    readMap = re.split(', |\n', reserveFile.read())
    holdNum = []

    for index in range(len(readMap)):
        if (len(readMap[index]) < 2):
            holdNum.append(readMap[index])

    while("" in holdNum): #removes the extra blank string
        holdNum.remove("")
        
    for i in range(len(holdNum)): #turns the strings to integers
        holdNum[i] = int(holdNum[i])

    while x < len(holdNum):

        busMap[holdNum[x]][holdNum[x+1]] = "X"
        x += 2

    global sales
    sales = getSales(holdNum)

    reserveFile.close()

    return busMap

def getSales(holdNum):
    costMatrix = getCost()
    costNum = []
    y = 0

    while y < len(holdNum):
        costNum.append(costMatrix[holdNum[y]][holdNum[y+1]])
        y += 2

    sales = sum(costNum)
    return sales

def getCost():
    costMatrix = [[100, 75, 50, 100] for row in range(10)]
    return costMatrix

app.run(host='0.0.0.0')
