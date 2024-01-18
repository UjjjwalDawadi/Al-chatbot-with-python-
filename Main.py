import tkinter as tk
from tkinter import scrolledtext
from Functions import get_chatbot_response, load_patterns, load_knowledge_base

# Load patterns and knowledge_base
patterns = load_patterns()
knowledge_base = load_knowledge_base()

def process_input(event=None):
    user_input = entry.get()

    if user_input.lower() == 'bye':
        window.destroy()  # Destroy the Tkinter window to exit the program
        return

    if user_input == "Type here...":
        return

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"You: {user_input}\n")

    chatbot_response = get_chatbot_response(user_input, patterns, knowledge_base)

    chat_log.insert(tk.END, f"Chatbot: {chatbot_response}\n")

    entry.delete(0, tk.END)
    chat_log.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Talkey Chatbot")
window.geometry("480x500")
window.configure(bg='lightblue')

chat_log = scrolledtext.ScrolledText(window, width=50, height=25, wrap=tk.WORD, state=tk.DISABLED, bg='white')
chat_log.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="Type here...", color='grey', **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)

    def focus_out(self, event):
        if not self.get():
            self.put_placeholder()

entry = PlaceholderEntry(window, width=50, fg='grey')
entry.grid(column=0, row=1, padx=10, pady=10)

send_button = tk.Button(window, text="Send", command=process_input, bg='lightblue', fg='black')
send_button.grid(column=1, row=1, padx=10, pady=10)

# Bind the Enter key to the process_input function
entry.bind("<Return>", process_input)

window.mainloop()
