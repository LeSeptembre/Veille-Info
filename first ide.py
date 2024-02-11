import tkinter as tk
from tkinter import scrolledtext
import sys
import io

def run_code():
    output_text.delete(1.0, tk.END)
    error_text.delete(1.0, tk.END)
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        code = code_text.get(1.0, tk.END)
        exec(code)
    except Exception as e:
        error_text.insert(tk.END, f"Erreur : {str(e)}")
    output_result = sys.stdout.getvalue()
    error_result = sys.stderr.getvalue()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    output_text.insert(tk.END, output_result)
    error_text.insert(tk.END, error_result)

root = tk.Tk()
root.title("Simple Code Runner")
code_text = scrolledtext.ScrolledText(root, width=40, height=20, wrap=tk.WORD)
code_text.pack(side=tk.LEFT, padx=10, pady=10)
run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack(side=tk.TOP, pady=10)
output_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
output_text.pack(side=tk.TOP, padx=10, pady=10)
error_text = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD, fg="red")
error_text.pack(side=tk.TOP, padx=10, pady=10)
root.mainloop()
