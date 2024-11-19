import os
import tkinter
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"


class FlashCardApp():

    def __init__(self):
        self.reps = 0
        self.window = None
        self.canvas = None
        self.card_front_image = None
        self.card_back_image = None
        self.card_background = None
        self.right_button = None
        self.wrong_button = None
        self.card_title = None
        self.card_word = None
        self.flip_timer = None
        self.current_card = {}
        self.words_to_learn = []
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.current_dir, 'images')
        self.setup_ui()
        self._init_data()

    # ---------------------------- UI SETUP ------------------------------- #

    def setup_ui(self):
        """ Setup the User Interface. """
        self._setup_window()
        self._setup_canvas()
        self._setup_buttons()

    def _setup_window(self):
        """ Setup the window. """
        self.window = tkinter.Tk()
        self.window.title("Flash Cards")
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    def _setup_canvas(self):
        """ Setup Canvas with card_front image and the title and word text. """
        self.canvas = tkinter.Canvas(width=800, height=526)
        front_image_path = os.path.join(self.images_dir, "card_front.png")
        self.card_front_image = tkinter.PhotoImage(file=front_image_path)
        back_image_path = os.path.join(self.images_dir, "card_back.png")
        self.card_back_image = tkinter.PhotoImage(file=back_image_path)
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_image)
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(column=0, row=0, columnspan=2)
        self.card_title = self.canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

    def _setup_buttons(self):
        """ Setup 'Wrong' and 'Right' Buttons. """
        self.wrong_image = tkinter.PhotoImage(file=os.path.join(self.images_dir, "wrong.png"))
        self.wrong_button = tkinter.Button(image=self.wrong_image, highlightthickness=0,
                                           command=self.next_card)
        self.wrong_button.grid(row=1, column=0)

        self.right_image = tkinter.PhotoImage(file=os.path.join(self.images_dir, "right.png"))
        self.right_button = tkinter.Button(image=self.right_image, highlightthickness=0,
                                           command=self.word_known)
        self.right_button.grid(row=1, column=1)

    # ---------------------------- READ DATA ------------------------------ #

    def _init_data(self):
        """ Reads most common 1000 words from "words_to_learn.csv" file if it exists,
        else from "spanish_words.csv" file and stores them as list of dictionaries. """
        data_file_path = os.path.join(self.current_dir, 'data', "words_to_learn.csv")
        if not os.path.isfile(data_file_path):
            data_file_path = os.path.join(self.current_dir, 'data', "spanish_words.csv")
        data = pandas.read_csv(data_file_path)
        self.words_to_learn = data.to_dict(orient="records")

    # ----------------------- NEXT CARD GENERATOR ------------------------- #

    def flip_card(self):
        """ It flips the card to display the English meaning of the word. """
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card["English"], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_image)

    def next_card(self):
        """ Display the next card when 'wrong' or 'right' button is clicked. It resets the
        flip timer, selects a new word and updates the background."""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
        self.current_card = random.choice(self.words_to_learn)
        self.canvas.itemconfig(self.card_title, text="Spanish", fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card["Spanish"], fill="black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_image)
        self.flip_timer = self.window.after(3000, func=self.flip_card)

    def word_known(self):
        self.words_to_learn.remove(self.current_card)
        data = pandas.DataFrame(self.words_to_learn)
        data_file_path = os.path.join(self.current_dir, 'data', "words_to_learn.csv")
        data.to_csv(data_file_path, index=False)
        self.next_card()
        

# ---------------------------- Main Method ------------------------------- #


def main():
    """ Main method to execute Pomodoro app. """
    flash = FlashCardApp()
    flash.next_card()
    flash.window.mainloop()


if __name__ == "__main__":
    main()
