import random
import tkinter as tk
from tkinter import messagebox
import time

class FlashcardsApp:
    def __init__(self, master):
        self.master = master
        self.flashcards = {}
        self.current_flashcard = None
        self.timer_label = None
        self.start_time = None
        self.high_score = None
        self.timer_running = False

        self.master.title("Flashcards App")
        self.master.geometry("400x300")

        self.question_label = tk.Label(self.master, text="Question:")
        self.question_label.pack()

        self.question_entry = tk.Entry(self.master)
        self.question_entry.pack()

        self.answer_label = tk.Label(self.master, text="Answer:")
        self.answer_label.pack()

        self.answer_entry = tk.Entry(self.master)
        self.answer_entry.pack()

        self.add_flashcard_button = tk.Button(self.master, text="Add Flashcard", command=self.add_flashcard)
        self.add_flashcard_button.pack()

        self.start_flashcards_button = tk.Button(self.master, text="Start Flashcards", command=self.start_flashcards)
        self.start_flashcards_button.pack()

        self.high_score_label = tk.Label(self.master, text="High Score: N/A")
        self.high_score_label.pack()

    def add_flashcard(self):
        question = self.question_entry.get()
        answer = self.answer_entry.get()
        if question and answer:
            self.flashcards[question] = answer
            messagebox.showinfo("Success", "Flashcard added successfully!")
        else:
            messagebox.showerror("Error", "Please enter both question and answer.")
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def start_flashcards(self):
        if not self.flashcards:
            messagebox.showinfo("No Flashcards", "No flashcards added yet!")
            return
        
        self.start_time = time.time()  # Record the start time
        self.timer_running = True
        self.flashcards_session()
        self.update_timer()

    def flashcards_session(self):
        if not self.flashcards:
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Session Complete", f"You completed the flashcards in {elapsed_time} seconds!")
            self.timer_running = False
            if self.high_score is None or elapsed_time < self.high_score:
                self.high_score = elapsed_time
                self.high_score_label.config(text=f"High Score: {self.high_score} seconds")
            return

        question, answer = random.choice(list(self.flashcards.items()))
        self.current_flashcard = question

        flashcard_frame = tk.Frame(self.master)
        flashcard_frame.pack()

        question_label = tk.Label(flashcard_frame, text=question)
        question_label.pack()

        answer_entry = tk.Entry(flashcard_frame)
        answer_entry.pack()

        submit_button = tk.Button(flashcard_frame, text="Submit", command=lambda: self.check_answer(answer_entry.get(), answer, flashcard_frame))
        submit_button.pack()

        # Clear the text entry fields
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)

    def update_timer(self):
        if self.timer_running:
            if self.timer_label is None:
                self.timer_label = tk.Label(self.master, text="")
                self.timer_label.pack()

            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text="Time elapsed: {} seconds".format(elapsed_time))

            # Update the timer every second
            self.master.after(1000, self.update_timer)

    def check_answer(self, user_answer, correct_answer, flashcard_frame):
        flashcard_frame.destroy()
        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", "Your answer is incorrect. The correct answer is: " + correct_answer)
        del self.flashcards[self.current_flashcard]  # Remove the flashcard after answering
        self.flashcards_session()

def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
