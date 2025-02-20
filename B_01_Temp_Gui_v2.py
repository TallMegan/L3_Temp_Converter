from tkinter import *
from functools import partial  # to prevent unwanted windows
from datetime import date
import all_constants as c
import conversion_rounding as cr


class Converter:
    """
    Temperature conversion tool (C to F or F to C)
    """

    def __init__(self):
        """
        Temperature converter GUI
        """

        self.all_calculations_list = []

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter", font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature below and " \
                       "then press one of the buttons to convert it from centigrade to Fahrenheit"
        self.temp_instructions = Label(self.temp_frame, text=instructions,
                                       wraplength=250, width=40, justify="left")

        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14"))
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.answer_error = Label(self.temp_frame, text=error,
                                  fg="#004C99", font=("Arial", "14", "bold"))
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["To Celsius", "#990099", lambda: self.check_temp(c.ABS_ZERO_FAHRENHEIT), 0, 0],
            ["To Fahrenheit", "#009900", lambda: self.check_temp(c.ABS_ZERO_CELSIUS), 0, 1],
            ["Help / Info", "#CC6600", self.to_help, 1, 0],
            ["History / Export", "#004C99", self.to_history, 1, 1]
        ]

        # list to hold buttons once they have been made
        self.button_ref_list = []

        # creates the buttons
        for item in button_details_list:
            # creates the button itself
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=12, command=item[2])

            # adjusts the positioning of each button
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            # appends the buttons into the list
            self.button_ref_list.append(self.make_button)

        # retrieve the to_help button
        self.to_help_button = self.button_ref_list[2]

        # retrieve "history / export" button and disable it at the start
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_temp(self, min_temp):

        """
        Checks the temperature is valid and either invokes calculation
        function or shows a custom error
        """

        # retrieve temperature to be converted
        to_convert = self.temp_entry.get()

        # reset label and entry box (if we had an error)
        self.answer_error.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        error = f"Enter a number more than / equal to {min_temp}"
        has_error = "no"

        try:
            to_convert = float(to_convert)
            if to_convert >= min_temp:
                self.convert(min_temp, to_convert)
            else:
                has_error = "yes"

        except ValueError:
            has_error = "yes"
            error = "Please enter a number"

        # checks the if the error message is necessary
        if has_error != "no":
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", "10", "bold"))
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)

    def convert(self, min_temp, to_convert):

        """
        Converts temperatures and updates answer label.
        Also stores calculations for Export / History feature.
        """

        if min_temp == c.ABS_ZERO_CELSIUS:
            answer = cr.to_fahrenheit(to_convert)
            answer_statement = f"{to_convert}°C is {answer}°F"

        else:
            answer = cr.to_celsius(to_convert)
            answer_statement = f"{to_convert}°F is {answer}°C"

        # enables the history export button as soon as we have a valid calculation
        self.to_history_button.config(state=NORMAL)

        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)
        print(self.all_calculations_list)

    def to_help(self):
        """
        Opens help dialogue box and disables help button
        (so that users can't create multiple help boxes).
        """
        DisplayHelp(self)

    def to_history(self):
        """
        Opens history dialogue box and disables history button
        (so that users can't create multiple history boxes)
        """
        HistoryExport(self, self.all_calculations_list)


class DisplayHelp:

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"

        # Toplevel() makes a new dialogue box
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "To use the program, simply enter the temperature you wish " \
                    "to convert and then choose to convert " \
                    "to either degree celsius or Fahrenheit.. \n\n Note that " \
                    "-273 degrees C (-459 F) is absolute zero (the " \
                    "coldest possible temperature). If you try to convert a temperature " \
                    "that is less than -273 " \
                    "degrees C you will get an error message. To see your calculation " \
                    "history and export it to a text " \
                    "file, please click the History / Export button"

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # list and loop to set background colour on
        # everything except the buttons
        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]
        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Closes help dialogue box (and enables help button)
        """
        # Put help button back to normal...
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:
    """
    Displays history dialogue box
    """

    def __init__(self, partner, all_calculations_list):
        # setup dialogue box and background colour

        self.history_box = Toplevel()

        # disables history button
        partner.to_history_button.config(state=DISABLED)

        # if users press cross at top, closes history and
        # 'releases' history button
        self.history_box.protocol('WM_DELETE_WINDOW', partial(self.close_history, partner))

        self.help_frame = Frame(self.history_box)
        self.help_frame.grid()

        # background colour and text for calculation area
        if len(all_calculations_list) <= c.MAX_CALCS:
            calc_back = "#D5E804"
            calc_amount = "all your calculations"
        else:
            calc_back = "#ffe6cc"
            calc_amount = (f"your calculations -"
                           f"showing {c.MAX_CALCS} / {len(all_calculations_list)}")

        # create string from calculations list (newest calculations first)
        newest_first_string = ""
        newest_first_list = list(reversed(all_calculations_list))

        # last item added in outside the for loop so that the spacing is correct
        if len(newest_first_list) <= c.MAX_CALCS:

            for item in newest_first_list[:-1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[-1]

        # if we have more than five items
        else:
            # makes it so that the string will only contain
            # the 5 most recent calculations - MAX_CALCS = 5, so it
            # takes the 5 most recent inside the list because it's actually just [5]
            for item in newest_first_list[:c.MAX_CALCS - 1]:
                newest_first_string += item + "\n"

            newest_first_string += newest_first_list[c.MAX_CALCS - 1]

        # strings for 'long' labels...
        recent_intro_txt = f"Below are {calc_amount} calculations " \
                           f"(to the nearest degree)."

        export_instruction_txt = ("Please push <Export> to save your calculations "
                                  "in a text file. If the filename already exists "
                                  "it will be overwritten")

        # all_calculations_list = ""

        # label list (label text | format | bg)
        history_labels_list = [
            ["History / Export", ("Arial", "16", "bold"), None],
            [recent_intro_txt, ("Arial", "11",), None],
            [newest_first_string, ("Arial", "14"), calc_back],
            [export_instruction_txt, ("Arial", "11"), None],
        ]

        history_label_ref = []
        for count, item in enumerate(history_labels_list):
            make_label = Label(self.history_box, text=item[0], font=item[1],
                               bg=item[2],
                               wraplength=300, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            history_label_ref.append(make_label)

        # retrieve export instruction la bel so that we can
        # configure it to show the filename if the user exports the file
        self.export_filename_label = history_label_ref[3]

        # make frame to hold buttons (two columns)
        self.hist_button_frame = Frame(self.history_box)
        self.hist_button_frame.grid(row=4)

        button_ref_list = []

        # button list (button text | bg colour | command | row | column)
        button_details_list = [
            ["Export", "#004C99", lambda: self.export_data(all_calculations_list), 0, 0],
            ["Close", "#666666", partial(self.close_history, partner), 0, 1],
        ]

        for btn in button_details_list:
            self.make_button = Button(self.hist_button_frame,
                                      font=("Arial", "12", "bold"),
                                      text=btn[0], bg=btn[1],
                                      command=btn[2])
            self.make_button.grid(row=btn[3], column=btn[4], padx=10, pady=10)

    def export_data(self, all_calculations_list):

        # get current date for the text file
        today = date.today()

        # get day, month and year
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        # edit labels so users know that their export has been done
        file_name = f"temperatures_{year}_{month}_{day}"

        success_string = (f"Export Successful! The file is "
                          f"called {file_name}.txt")

        self.export_filename_label.config(fg="#009900", text=success_string,
                                          font=("Arial", "12", "bold"))

        write_to = f"{file_name}.txt"

        with open(write_to, "w") as text_file:
            text_file.write("***** Temperature Calculations ***** \n")
            text_file.write(f"Generated: {day}/{month}/{year}\n\n")
            text_file.write("Here is your calculation history (oldest to newest) \n")
            print(all_calculations_list)
            # write the item to file
            for item in all_calculations_list:
                print(item)
                text_file.write(item)
                text_file.write("\n")

    def close_history(self, partner):
        """
        Closes history dialogue box (and enables history button)
        """
        # put history button back to normal
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# main routine

if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
