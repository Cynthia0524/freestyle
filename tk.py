from tkinter import *

def process_command(text):
    ''' Given a string, returns a string in response. '''
    text = text.strip().lower()
    if text == 'cynthia':
        return "welcome"
    # elif ...:
    # elif ...:
    elif text in {'quit', 'exit'}:
        return
    else:
        return 'you don not have rights'
        #return 'Unknown command.'

def main():
    ''' Main entry point of the program: create the windows and
        kick off the event loop '''
    tk = Tk()
    canvas = Canvas(tk, width=400, height=200, bg='white')
    canvas.pack()

    text = Text(tk, height=10, width=50, bg='light gray')
    text.pack()

    def process_callback(*args):
        ''' Callback that's called when the user presses enter or
            clicks the button. '''

        # figure out what the response to the input should be
        response = process_command(entry.get())

        if response is None:
            tk.quit()
            tk.destroy()
            return

        # write the response
        text.insert(END, '\n{}\n'.format(response))

        # clear the input field
        entry.delete(0, END)

    entry = Entry(tk, width=65, bd=5)
    entry.pack()
    entry.focus()
    entry.bind('<Return>', process_callback)

    btn = Button(tk, width=50, bd=3, bg='dark gray', text='Submit',
                    command=process_callback)
    btn.pack()

    text.insert(END, "Hi! Please input your username\n")

    tk.mainloop()


if __name__ == '__main__':
    main()
