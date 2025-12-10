import random
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk


class SudokuOkn(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Судоку")
        self.Main()
        self.sudoku_setk = SudokuLG(self)
        self.sudoku_setk.blocks()
        self.config(bg='#DCDCDC')
         
        check_button = ctk.CTkButton(self, text="ПРОВЕРКА", font=('Arial', 14),
                                 command=self.sudoku_otv, corner_radius=5, fg_color="#4B4C4C")
        check_button.grid (row=9 , column=0, columnspan=9 , pady=10)

    def Main(self):
        scw = self.winfo_screenwidth()
        sch = self.winfo_screenheight()

        pw = 0.423
        ph = 0.83

        ok_w = int(scw * pw)
        ok_h = int(sch * ph)

        x = (scw - ok_w) // 2
        y = (sch - ok_h) // 2
        self.geometry(f"{ok_w}x{ok_h}+{x}+{y}")

    def sudoku_otv(self):
        values = self.sudoku_setk.val()
        for row in values:
            print(row)
        result = logic_sudoku(values)
        if result == "v":
            messagebox.showinfo( "Проверка" , "решено правильно" )

        elif result == "0":
            messagebox.showinfo( "Проверка", "таблица не заполнена!!!!!!" )
        
        else:
            messagebox.showinfo( "Проверка", "у тебя ошибки" )

class SudokuLG:
    def __init__(self, root):
        self.root = root
        self.cells = [ [None for _ in range(9)] for _ in range(9) ]

    def blocks(self):
        for r in range(9):
            for c in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 44) ,
                                 justify='center')
                entry.grid(row=r, column=c, padx=1, pady=1)
                self.cells[r][c] = entry


                if (r/3 + c/3) % 2 == 0 :
                    entry.config(bg='#A5A5A5')
                else:
                    entry.config(bg='#A5A5A5')

        zadacha = generate_zadacha()
        for r in range(9):
            for c in range(9):
                if zadacha[r][c] != 0:
                    self.cells[r][c].insert( 0, str(zadacha[r][c]))
                    self.cells[r][c].config( state='disabled')


    def val(self):
        values = []
        for row in self.cells:
            r_val = []
            for entry in row:
                val = entry.get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    r_val.append(int(val))
                else:
                    r_val.append(0)
            values.append(r_val)
        return values
    

def can_place(setk, row, col, num):
    if num in setk[row]:
        return False
    if num in [setk[r][col] for r in range(9)]: 
        return False
    s_rw, s_cl = 3 * ( row//3), 3 * ( col//3)
    for r in range( s_rw, s_rw + 3):
        for c in range( s_cl, s_cl + 3):
            if setk[r][c] == num: 
                return False
    return True
    
def resh(setk):
    for r in  range(9):
        for c in range(9):
            if setk[r][c] == 0:
                ns = list(range(1, 10))
                random.shuffle(ns)
                for num in ns:
                    if can_place(setk, r, c, num):
                        setk[r][c] = num
                        if resh(setk): 
                            return True
                        setk[r][c] = 0
                return False
    return True

def blk(setk):
    for k in range (0, 9, 3):
        ns = list (range(1, 10))
        random.shuffle(ns)
        for i in range(3):
            for j in range(3):
                setk[k+i][k+j] = ns.pop()
            
def gener():
    setk = [[0] * 9 for _ in range(9)]
    blk(setk)
    resh(setk)
    return setk

def generate_zadacha():
    setk = gener()
    kletk_del = random.sample(range(81), 61)
    for idx in kletk_del:
        r, c = divmod(idx, 9)
        setk[r][c] = 0
    return setk

                
def logic_sudoku(setk):

    for row in setk:
        num = [n for n in row if n != 0]
        if len(num) != len(set(num)):
            print("ошибка в строке")
            return "x"
    
    for c in range(9):
        col = [setk[r][c] for r in range(9) if setk[r][c] != 0]
        if len(col) != len(set(col)):
            print("ошибка в колонке")
            return "x"
        
    for br in range(0, 9 ,3):
        for bc in range(0, 9 ,3):
            block = []
            for r in range (br, br+3):
                for c in range (bc, bc+3):
                    if setk[r][c] != 0 :
                        block.append(setk[r][c])
            if len(block) != len(set(block)):
                print('ошибка в блоке 3*3')
                return "x"
    
    for  row  in setk:
        if 0 in row:
            print('сетка не заполнена ')
            return "0"
    
    return "v"

if __name__ == "__main__":
    app = SudokuOkn()
    app.mainloop()