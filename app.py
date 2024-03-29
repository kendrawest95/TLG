from tkinter import *
import math
import PIL.Image
import PIL.ImageTk
import pygame
# ___________________________________CONSTANTS___________________________________________#
work_min = 25
short_break = 5
long_break = 15
reps = 0
timer = None
# ______________________________SOUND BITE FUNCTION_____________________________________#
pygame.mixer.init()


def play():
    pygame.mixer.music.load("quack.mp3")
    pygame.mixer.music.play(loops=0)
# __________________________________TIMER AND COUNTDOWN FUNCTION_______________________#
# create function for resetting the timer


def reset_timer():
    start_button["state"] = "normal"
    root.after_cancel(timer)
    canvas.itemconfig(timer_text, text="0:00")
    title_label.config(text="Timer", fg="#a020f0")
    check_marks.config(text="")
    global reps
    reps = 0

# start timer function that prevents user from clicking it again


def start_timer():
    start_button["state"] = "disabled"
    global timer
    global reps
    reps += 1

    if reps % 2 == 1:  # Odd reps are work sessions
        countdown(work_min * 60)
        title_label.config(text="Work", fg="#a020f0")
    elif reps % 8 == 0:  # Every 4th break is a long break
        countdown(long_break * 60)
        title_label.config(text="Break", fg="#a020f0")
    else:
        countdown(short_break * 60)
        title_label.config(text="Break", fg="#a020f0")

# function that updates gui timer and continues countdown until it reaches 0


def countdown(count):  # function that takes count parameter
    count_min = math.floor(count / 60)
    # math calculation for total minutes and seconds from the total time in seconds
    count_sec = count % 60
    if count_sec < 10:
        # if seconds are less than 10, add a leading 0
        count_sec = f"0{count_sec}"
    # update canvas display with formatted time
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        # if count is greater than 0, a schedule is made to call the function after 1000ms(1s)
        timer = root.after(1000, countdown, count - 1)
    else:
        update_check_marks()
        start_timer()
        play()


def update_check_marks():
    marks = ""
    work_sessions = math.floor(reps / 2)
    for _ in range(work_sessions):
        marks += "✓"
    check_marks.config(text=marks)


def skip_session():
    global timer
    root.after_cancel(timer)
    update_check_marks()
    start_timer()
    play()


# ________________________________________UI SETUP_______________________________________#
root = Tk()
root.title("PomoDuck")
root.config(bg="#87ceeb")

title_label = Label(text="Timer", fg="#eba031",
                    bg="#87ceeb", font=("Helvetica", 100))
title_label.grid(column=1, row=0, pady=(10, 0))
title_label.lift()

root.config(padx=100, pady=50)

# create widget image
canvas = Canvas(width=200, height=224, borderwidth=3,
                relief="ridge", bg="#87ceeb")
im = PIL.Image.open("microwave-duck.gif")
duck_img = PIL.ImageTk.PhotoImage(im)
canvas.create_image(100, 112, image=duck_img)
timer_text = canvas.create_text(
    100, 130, text="0:00", fill="#87ceeb", font=("Helvetica", 75, "bold"))
canvas.grid(column=1, row=1, pady=(0, 10))

# create and style button
start_button = Button(text="Start", highlightthickness=1,
                      command=start_timer, bg="#1e90c9", font=("Helvetica", 25, "bold"))
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=1,
                      command=reset_timer, bg="#1e90c9", font=("Helvetica", 25, "bold"))
reset_button.grid(column=2, row=2)

skip_button = Button(text="Skip", highlightthickness=1,
                     command=skip_session, bg="#1e90c9", font=("helvetica", 25, "bold"))
skip_button.grid(column=1, row=2)

# check marks styling
check_marks = Label(text="", fg="#eba031", bg="#87ceeb",
                    font=("Helvetica", 25, "bold"))
check_marks.grid(column=1, row=3)

root.mainloop()
