import random
import tkinter as tk
from tkinter import messagebox


class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Судоку Сетка 9x9")
        self.Main()
        self.sudoku_grid = SudokuGrid(self)
        self.sudoku_grid.blocks()
        self.config(bg='turquoise')
         
        # Кнопка проверки
        check_button = tk.Button(self, text="проверка",
                                 command=self.sudoku_otv)
        check_button.grid(row=9, column=0, columnspan=9, pady=10)
# расположение
    def Main(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        percent_width = 0.2645
        percent_height = 0.40

        window_width = int(screen_width * percent_width)
        window_height = int(screen_height * percent_height)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def sudoku_otv(self):
        all_values = self.sudoku_grid.val()
        for row in all_values:
            print(row)
        result = logic_sudoku(all_values)
        if result == "v":
            messagebox.showinfo("Проверка", "решено правильно")

        elif result == "0":
            messagebox.showinfo("Проверка", "таблица не заполнена")
        
        else:
            messagebox.showinfo("Проверка", "решено с ошибками")

class SudokuGrid:
    def __init__(self, root):
        self.root = root
        self.cells = [[None for _ in range(9)] for _ in range(9)]

# разбиение блоков по цвету 3*3*
    def blocks(self):
        for r in range(9):
            for c in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18),
                                 justify='center')
                entry.grid(row=r, column=c, padx=1, pady=1)
                self.cells[r][c] = entry

                if (r // 3 + c // 3) % 2 == 0:
                    entry.config(bg='lightgray')
                else:
                    entry.config(bg='lightgray')

        zadacha = generate_zadacha()
        for r in range(9):
            for c in range(9):
                if zadacha[r][c] != 0:
                    self.cells[r][c].insert(0, str(zadacha[r][c]))
                    self.cells[r][c].config(state='disabled')


    def val(self):
        values = []
        for row in self.cells:
            row_values = []
            for entry in row:
                val = entry.get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row_values.append(int(val))
                else:
                    row_values.append(0)
            values.append(row_values)
        return values
    

def can_place(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(9)]: 
        return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for r in range(sr, sr + 3):
        for c in range(sc, sc + 3):
            if grid[r][c] == num: 
                return False
    return True
    
def resh(grid):
    for r in  range(9):
        for c in  range(9):
            if grid[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if can_place(grid, r, c, num):
                        grid[r][c] = num
                        if resh(grid): 
                            return True
                        grid[r][c] = 0
                return False
    return True

def blk(grid):
    for k in range (0, 9, 3):
        nums = list (range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                grid[k+i][k+j] = nums.pop()
            

def gener():
    grid = [[0] * 9 for _ in range(9)]
    blk(grid)
    resh(grid)
    return grid

def generate_zadacha():
    grid = gener()
    cells_to_remove = random.sample(range(81), 61)
    for idx in cells_to_remove:
        r, c = divmod(idx, 9)
        grid[r][c] = 0
    return grid

                
def logic_sudoku(grid):

    for row in grid:
        num = [n for n in row if n != 0]
        if len(num) != len(set(num)):
            print("ошибка в строке")
            return "x"
    
    for c in range(9):
        col = [grid[r][c] for r in range(9) if grid[r][c] != 0]
        if len(col) != len(set(col)):
            print("ошибка в колонке")
            return "x"
        
    for br in range(0, 9 ,3):
        for bc in range(0, 9 ,3):
            block = []
            for r in range (br, br+3):
                for c in range (bc, bc+3):
                    if grid[r][c] != 0 :
                        block.append(grid[r][c])
            if len(block) != len(set(block)):
                print('ошибка в блоке 3*3')
                return "x"
    
    for  row  in grid:
        if 0 in row:
            print('сетка не заполнена ')
            return "0"
    
    return "v"

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()