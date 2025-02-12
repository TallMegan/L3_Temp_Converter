from tkinter import *
from functools import partial  # to prevent unwanted windows


class Converter:
    """
    Temperature conversion tool (C to F or F to C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.to_history_button = Button(self.temp_frame,
                                        text="Help / Info",
                                        bg="#CC6600",
                                        fg="#FFFFFF",
                                        font=("Arial", "14", "bold"),
                                        width=12, command=self.to_history)

        self.to_history_button.grid(row=1, padx=5, pady=5)

    def to_history(self):
        """
        Opens history dialogue box and disables history button
        (so that users can't create multiple history boxes)
        """
        HistoryExport(self)


class HistoryExport:
    """
    Displays history dialogue box
    """

    def __init__(self, partner):
        # setup dialogue box and background colour

        green_back = "#D5E804"
        peach_back = "ffe6cc"

        self.history_box = Toplevel()

        # disables history button
        partner.to_history_button.config(state=DISABLED)

        # if users press cross at top, closes history and
        # 'releases' history button
        self.history_box.protocol('WM_DELETE_WINDOW', partial(self.close_history, partner))

        self.help_frame = Frame(self.history_box)
        self.help_frame.grid()

        # strings for 'long' labels...
        recent_intro_txt = "Below are your recent calculations " \
                           "- showing 3 / 3 calculations. All calculations " \
                           "are shown to the nearest degree"

        export_instruction_txt = ("Please push <Export> to save your calculations "
                                  "in a text file. If the filename already exists "
                                  "it will be overwritten")

        calculations = ""

        # label list (label text | format | bg)
        history_labels_list = [
            ["History / Export", ("Arial", "16", "bold"), None],
            [recent_intro_txt, ("Arial", "11", ), None],
            ["History / Export", ("Arial", "14"), green_back],
            [export_instruction_txt, ("Arial", "11"), None],
        ]

        history_label_ref = []


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
