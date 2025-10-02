import customtkinter as ctk
import math

# --- Configure App ---
ctk.set_appearance_mode("dark")  # dark / light / system
ctk.set_default_color_theme("green")  # green, blue, dark-blue

app = ctk.CTk()
app.title("✨ Ultimatecalc ✨")
app.geometry("600x750")

expression = ""

# --- Functions ---
def press(num):
    global expression
    expression += str(num)
    entry_var.set(expression)

def clear():
    global expression
    expression = ""
    entry_var.set("")

def equalpress():
    global expression
    try:
        result = str(eval(expression))
        entry_var.set(result)
        expression = result
    except Exception as e:
        entry_var.set("Error")
        expression = ""

def scientific(func):
    global expression
    try:
        value = eval(expression) if expression else 0
        if func == "√":
            result = math.sqrt(value)
        elif func == "sin":
            result = math.sin(math.radians(value))
        elif func == "cos":
            result = math.cos(math.radians(value))
        elif func == "tan":
            result = math.tan(math.radians(value))
        elif func == "log":
            result = math.log10(value)
        elif func == "ln":
            result = math.log(value)
        elif func == "π":
            result = math.pi
        elif func == "e":
            result = math.e
        else:
            result = value
        entry_var.set(str(result))
        expression = str(result)
    except:
        entry_var.set("Error")
        expression = ""

# --- Hamming Parity ---
def hamming_parity():
    global expression
    try:
        data = expression.strip()
        if not all(ch in "01" for ch in data):
            entry_var.set("Binary only")
            return
        n = len(data)
        parity = data.count("1") % 2
        entry_var.set(f"Data: {data} | Parity: {parity}")
        expression = ""
    except:
        entry_var.set("Error")
        expression = ""

# --- Entry Field ---
entry_var = ctk.StringVar()
entry = ctk.CTkEntry(
    app, textvariable=entry_var,
    font=("Helvetica", 28, "bold"),
    justify="right", width=560, height=80
)
entry.pack(pady=20)

# --- Button Frame ---
frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(padx=15, pady=10, expand=True, fill="both")

btn_font = ("Helvetica", 16, "bold")

def create_button(text, row, col, color="teal", func="normal", colspan=1):
    if func == "normal":
        cmd = lambda: press(text) if text not in ["C", "="] else (clear() if text == "C" else equalpress())
    elif func == "scientific":
        cmd = lambda: scientific(text)
    elif func == "hamming":
        cmd = hamming_parity
    else:
        cmd = lambda: press(text)

    btn = ctk.CTkButton(
        frame, text=text, command=cmd,
        font=btn_font, width=100*colspan, height=60,
        fg_color=color, hover_color="gray20"
    )
    btn.grid(row=row, column=col, padx=5, pady=5, columnspan=colspan, sticky="nsew")

# --- Layout (Arithmetic, Scientific, Logical, Comparison, Bitwise) ---
buttons = [
    ["7", "8", "9", "/", "sin"],
    ["4", "5", "6", "*", "cos"],
    ["1", "2", "3", "-", "tan"],
    ["0", ".", "C", "+", "√"],
    ["%", "//", "**", "(", ")"],
    ["<", ">", "==", "!=", "<="],
    [">=", "&", "|", "^", "~"],
    ["<<", ">>", "and", "or", "not"],
    ["π", "e", "log", "ln", "="],
    ["HAMMING PARITY",]
]

for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        if char == "=":
            create_button(char, r, c, color="green")
        elif char == "C":
            create_button(char, r, c, color="red")
        elif char in ["sin","cos","tan","√","log","ln","π","e"]:
            create_button(char, r, c, color="orange", func="scientific")
        elif char == "HAMMING PARITY":
            create_button(char, r, 0, color="purple", func="hamming", colspan=5)
        else:
            create_button(char, r, c, color="teal")

# Responsive grid
for i in range(5):
    frame.grid_columnconfigure(i, weight=1)
for j in range(len(buttons)):
    frame.grid_rowconfigure(j, weight=1)

app.mainloop()
