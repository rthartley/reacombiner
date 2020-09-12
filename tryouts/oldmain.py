# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import rppFile
from rppFile import Element
from tkinter import *
import PySimpleGUI as sg


class Table:
    def __init__(self, root, lst):
        # code for creating table
        total_rows = len(lst)
        total_columns = len(lst[0])
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='blue')

                self.e.grid(row=i + 1, column=j)
                self.e.insert(END, lst[i][j])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def printstruct(struct, indent):
    print("%s%s children" % ((" " * indent), len(struct)))
    for child in struct:
        if isinstance(child, Element):
            print("%sElement %s %s" % ((" " * indent), child.tag, child.attrib))
            gc = child.findall('*')
            printstruct(gc, indent + 3)
        else:
            print("%s%s" % ((" " * indent), child))

def showSimpleGUI():
    sg.theme('DarkAmber')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.Text('Some text on Row 1')],
              [sg.Text('Enter something on Row 2'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()

def showCalc():
    # creating basic window
    window = Tk()
    window.geometry("500x500")  # size of the window width:- 500, height:- 375
    window.resizable(0, 0)  # this prevents from resizing the window
    window.title("Calculator")

    ################################### functions ######################################
    # 'btn_click' function continuously updates the input field whenever you enters a number
    def btn_click(item):
        global expression
        expression = expression + str(item)
        input_text.set(expression)

    # 'btn_clear' function clears the input field
    def btn_clear():
        global expression
        expression = ""
        input_text.set("")

    # 'btn_equal' calculates the expression present in input field

    def btn_equal():
        global expression

        result = str(eval(expression))  # 'eval' function evaluates the string expression directly

        # you can also implement your own function to evaluate the expression instead of 'eval' function

        input_text.set(result)

        expression = ""

    expression = ""

    # 'StringVar()' is used to get the instance of input field

    input_text = StringVar()

    # creating a frame for the input field

    input_frame = Frame(window, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black",
                        highlightthickness=1)

    input_frame.pack(side=TOP)

    # creating a input field inside the 'Frame'

    input_field = Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#eee", bd=0,
                        justify=RIGHT)

    input_field.grid(row=0, column=0)

    input_field.pack(ipady=10)  # 'ipady' is internal padding to increase the height of input field

    # creating another 'Frame' for the button below the 'input_frame'

    btns_frame = Frame(window, width=312, height=272.5, bg="grey")

    btns_frame.pack()

    # first row

    clear = Button(btns_frame, text="C", fg="black", width=32, height=3, bd=0, bg="#eee", cursor="hand2",
                   command=lambda: btn_clear()).grid(row=0, column=0, columnspan=3, padx=1, pady=1)

    divide = Button(btns_frame, text="/", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                    command=lambda: btn_click("/")).grid(row=0, column=3, padx=1, pady=1)

    # second row

    seven = Button(btns_frame, text="7", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click(7)).grid(row=1, column=0, padx=1, pady=1)

    eight = Button(btns_frame, text="8", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click(8)).grid(row=1, column=1, padx=1, pady=1)

    nine = Button(btns_frame, text="9", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click(9)).grid(row=1, column=2, padx=1, pady=1)

    multiply = Button(btns_frame, text="*", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                      command=lambda: btn_click("*")).grid(row=1, column=3, padx=1, pady=1)

    # third row

    four = Button(btns_frame, text="4", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click(4)).grid(row=2, column=0, padx=1, pady=1)

    five = Button(btns_frame, text="5", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click(5)).grid(row=2, column=1, padx=1, pady=1)

    six = Button(btns_frame, text="6", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click(6)).grid(row=2, column=2, padx=1, pady=1)

    minus = Button(btns_frame, text="-", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                   command=lambda: btn_click("-")).grid(row=2, column=3, padx=1, pady=1)

    # fourth row

    one = Button(btns_frame, text="1", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click(1)).grid(row=3, column=0, padx=1, pady=1)

    two = Button(btns_frame, text="2", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click(2)).grid(row=3, column=1, padx=1, pady=1)

    three = Button(btns_frame, text="3", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click(3)).grid(row=3, column=2, padx=1, pady=1)

    plus = Button(btns_frame, text="+", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

    # fourth row

    zero = Button(btns_frame, text="0", fg="black", width=21, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)

    point = Button(btns_frame, text=".", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                   command=lambda: btn_click(".")).grid(row=4, column=2, padx=1, pady=1)

    equals = Button(btns_frame, text="=", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                    command=lambda: btn_equal()).grid(row=4, column=3, padx=1, pady=1)

    window.mainloop()

def showGUI3():
    window = Tk()
    window.title("GUI")
    # creating 2 text labels and input labels
    Label(window, text="Username").grid(row=0)  # this is placed in 0 0
    # 'Entry' is used to display the input-field
    Entry(window).grid(row=0, column=1)  # this is placed in 0 1
    Label(window, text="Password").grid(row=1)  # this is placed in 1 0
    Entry(window).grid(row=1, column=1)  # this is placed in 1 1
    # 'Checkbutton' is used to create the check buttons
    Checkbutton(window, text="Keep Me Logged In").grid(columnspan=2)
    #'columnspan' tells to take the width of 2 columns
    # you can also use 'rowspan' in the similar manner
    window.mainloop()

def showGUI2():
    window = Tk()
    window.title("GUI")
    # creating 2 frames TOP and BOTTOM
    top_frame = Frame(window).pack()
    bottom_frame = Frame(window)
    # now, create some widgets in the top_frame and bottom_frame
    btn1 = Button(top_frame, text="Button1", fg="red").pack()  # 'fg - foreground' is used to color the contents
    btn2 = Button(top_frame, text="Button2",
                          fg="green").pack()  # 'text' is used to write the text on the Button
#    btn3 = Button(bottom_frame, text="Button2", fg="purple").pack(
#        side="left")  # 'side' is used to align the widgets
#    btn4 = Button(bottom_frame, text="Button2", fg="orange").pack(side="left")
    lst = [(1, 'Raj', 'Mumbai', 19),
           (2, 'Aaryan', 'Pune', 18),
           (3, 'Vaishnavi', 'Mumbai', 20),
           (4, 'Rachna', 'Mumbai', 21),
           (5, 'Shubham', 'Delhi', 21)]
    t = Table(bottom_frame, lst)
    bottom_frame.pack()
    window.mainloop()

def showGUI():
    root = Tk()

    # giving title to the main window
    root.title("First_Program")
    root.geometry("350x500")
    # adding menu bar in root window
    # new item in menu bar labelled as 'New'
    # adding more items in the menu bar
    menu = Menu(root)
    item = Menu(menu)
    item.add_command(label='New')
    menu.add_cascade(label='File', menu=item)
    root.config(menu=menu)
    # Label is what output will be
    # show on the window
    label = Label(root, text="Hello World !")
    label.grid()

    # adding Entry Field
    txt = Entry(root, width=10)
    txt.grid(column=1, row=0)

    # button widget with red color text
    # function to display text when
    # button is clicked
    def clicked():
        res = "You wrote" + txt.get()
        label.configure(text=res)
        # inside
    btn = Button(root, text="Click me",
                 fg="red", command=clicked)

    btn.grid(column=2, row=0)

    lst = [(1, 'Raj', 'Mumbai', 19),
           (2, 'Aaryan', 'Pune', 18),
           (3, 'Vaishnavi', 'Mumbai', 20),
           (4, 'Rachna', 'Mumbai', 21),
           (5, 'Shubham', 'Delhi', 21)]
    t = Table(root, lst)

    # calling mainloop method which is used
    # when your application is ready to run
    # and it tells the code to keep displaying
    root.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    with open('/home/roger/rpp/SW5.rpp', 'r') as file:
        rpp = rppFile.load(file)
        children = rpp.findall('*')
#        print(children)
        printstruct(children, 0)
        expression = ""
        showSimpleGUI()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

