from tkinter import *
import pandas
import random
# import json
BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
BLACK = "#000000"
flip = None
current_card = {}

# Functionality to be added:
# -some of the "learned" words should be added back in whenever the program is started
# -new words should be added to the list of words to learn occasionally


def main():
    # ----------Functions----------
    # This function selects a word from the list of dictionaries and presents it in french to the user, triggering the
    # function after three seconds.
    def random_word():
        global flip, current_card
        try:
            window.after_cancel(flip)
        except ValueError:
            pass
        current_card = random.choice(translations_dicts)
        canvas.itemconfig(background, image=front)
        canvas.itemconfig(learning_lang, text="French", fill=BLACK)
        canvas.itemconfig(learning_word, text=current_card["French"], fill=BLACK)
        flip = window.after(3000, flip_card)

    # This function is called three seconds after the random_word function has been triggered. It changes the word
    # being presented to the user from the french version to the english.
    def flip_card():
        window.after_cancel(flip)
        canvas.itemconfig(background, image=back)
        canvas.itemconfig(learning_lang, text="English", fill=WHITE)
        canvas.itemconfig(learning_word, text=current_card["English"], fill=WHITE)

    # Initial code to save learned words before I realized I needed to save it as a CSV. This code overwrites instead
    # of appending, which would need to be resolved if I planned to use it.

    # def learned_word():
    #     new_word = current_card
    #     try:
    #         with open("learned_words.json", "r") as f:
    #             learned_words = json.load(f)
    #
    #     except FileNotFoundError:
    #         with open("learned_words.json", "w") as f:
    #             json.dump(new_word, f, indent=4)
    #
    #     else:
    #         learned_words.update(new_word)
    #
    #         with open("learned_words.json", "w") as f:
    #             json.dump(learned_words, f, indent=4)

    # This function is called when the user clicks the checkmark button. It removes the word from the translations
    # database, converts the database (with the word removed) into a csv file, and saves that NEW file in the
    # "words_to_learn.csv" file.
    def learned_word():
        translations.drop(translations.index[(translations["French"] == current_card["French"])], inplace=True)
        translations.to_csv("words_to_learn.csv", index=False)
        random_word()

        # Below is alternate code that serves the same purpose, commented out but left here as an alternative to use.

        # translations_dicts.remove(current_card)
        # new_translations = pandas.DataFrame(translations_dicts)
        # new_translations.to_csv("words_to_learn.csv", index=False)
        # random_word()
    # ----------Creation of the translation dictionary----------
    try:
        translations = pandas.read_csv("words_to_learn.csv")
    except FileNotFoundError:
        translations = pandas.read_csv("french_words.csv")
    translations_df = pandas.DataFrame(translations)
    translations_dicts = translations_df.to_dict(orient="records")

    # ----------User Interface stuff----------
    window = Tk()
    window.title("Flash Cards")
    window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

    canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
    front = PhotoImage(file="images/card_front.png")
    back = PhotoImage(file="images/card_back.png")
    background = canvas.create_image(400, 263, image=front)
    learning_lang = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
    learning_word = canvas.create_text(400, 263, text="Ready...", font=("Ariel", 60, "bold"))
    canvas.grid(column=0, row=0, columnspan=2)

    wrong_image = PhotoImage(file="images/wrong.png")
    x_button = Button(image=wrong_image, highlightthickness=0, command=random_word)
    x_button.grid(column=0, row=1)

    check_image = PhotoImage(file="images/right.png")
    check_button = Button(image=check_image, highlightthickness=0, command=learned_word)
    check_button.grid(column=1, row=1)

    # This calls the primary function so the program begins running as soon as it's open.
    random_word()

    window.mainloop()


if __name__ == '__main__':
    main()
