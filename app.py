import customtkinter
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image
from tkcalendar import DateEntry
from db_management import get_names, get_years, new_entry, get_game_by_name, edit_entry, delete_entry, delete_all_data
import io

TITLE_FONT = ("Open San", 20)


class AddWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("600x700")
        self.title("Add entry")
        self.attributes("-topmost", True)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title_hint = customtkinter.CTkLabel(self, text="Title *", corner_radius=6, font=(None, 20),
                                                 wraplength=500)
        self.title_hint.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = customtkinter.CTkEntry(self)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.review_hint = customtkinter.CTkLabel(self, text="Review *", corner_radius=6, font=(None, 20),
                                                  wraplength=500)
        self.review_hint.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.list_of_reviews = customtkinter.CTkComboBox(self, font=(None, 20),
                                                         values=["Bad", "Okay", "Good", "Amazing"])
        self.list_of_reviews.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.image_hint = customtkinter.CTkLabel(self, text="Image", corner_radius=6, font=(None, 20),
                                                 wraplength=500)
        self.image_hint.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.open_btn = customtkinter.CTkButton(self, text="Browse", font=(None, 20), command=self.open_image)
        self.open_btn.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.image_label = customtkinter.CTkLabel(self, text=None, corner_radius=6, fg_color=None, width=200,
                                                  height=200)
        self.image_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.image_label.grid_propagate(False)

        self.time_hint = customtkinter.CTkLabel(self, text="Time spent (hours) *", corner_radius=6,
                                                font=(None, 20), wraplength=500)
        self.time_hint.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.time_entry = customtkinter.CTkEntry(self)
        self.time_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.dlc_hint = customtkinter.CTkLabel(self, text="DLC (n/n)", corner_radius=6, font=(None, 20),
                                               wraplength=500)
        self.dlc_hint.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.dlc_entry = customtkinter.CTkEntry(self)
        self.dlc_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.achievements_hint = customtkinter.CTkLabel(self, text="Achievements (n/n)", corner_radius=6,
                                                        font=(None, 20),
                                                        wraplength=500)
        self.achievements_hint.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.achievements_entry = customtkinter.CTkEntry(self)
        self.achievements_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.date_hint = customtkinter.CTkLabel(self, text="Date of completion", corner_radius=6, font=(None, 20),
                                                wraplength=500)
        self.date_hint.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.calendar = DateEntry(self, selectmode="night", date_pattern="yyyy-mm-dd", width="23", height="20")
        self.calendar.grid(row=7, column=1, padx=16, pady=10, sticky="w")

        self.accept_btn = customtkinter.CTkButton(self, text="Add", font=(None, 30), command=self.add_object)
        self.accept_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="sew")

        self.file_path = None

    def open_image(self):
        self.attributes("-topmost", False)
        self.file_path = filedialog.askopenfilename(title="Choose an image",
                                                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;")])
        if self.file_path:
            image = Image.open(self.file_path)
            photo = CTkImage(light_image=image,
                             size=(self.image_label.winfo_width() - 50, self.image_label.winfo_height() - 50))
            self.image_label.configure(image=photo)
            self.image_label.image = image

        self.attributes("-topmost", True)

    def add_object(self):

        if self.file_path:
            object_image = self.file_path
        else:
            object_image = "img/intro.jpg"

        object_title = self.title_entry.get()
        object_time = self.time_entry.get()
        object_dlc = self.dlc_entry.get()
        object_achievements = self.achievements_entry.get()
        object_date = self.calendar.get_date()
        object_review = self.list_of_reviews.get()

        if object_title == "" or object_time == "":
            self.attributes("-topmost", False)
            messagebox.showinfo(title="Attention",
                                message='Fields: "Title" and "Time spent" are required to be filled in.')
            self.attributes("-topmost", True)
        else:
            if object_dlc == "":
                object_dlc = "N/A"
            if object_achievements == "":
                object_achievements = "N/A"
            self.attributes("-topmost", False)
            messagebox.showinfo(title="Completed", message="New entry has been successfully added to the database!")
            self.destroy()
            return new_entry(name=object_title, image=object_image, time_spent=object_time, dlc=object_dlc,
                             achievements=object_achievements, date=object_date, review=object_review)


class EditWindow(AddWindow):
    def __init__(self, master, entry):
        super().__init__(master)
        self.title("Edit entry")
        self.entry = entry
        self.title_entry.insert(0, entry.name)
        self.list_of_reviews.set(entry.review)

        self.image = Image.open(io.BytesIO(entry.image))
        photo = CTkImage(light_image=self.image, size=(self.image_label.winfo_width(), self.image_label.winfo_height()))
        self.image_label.configure(image=photo)

        self.time_entry.insert(0, entry.time_spent)
        self.dlc_entry.insert(0, entry.dlc)
        self.achievements_entry.insert(0, entry.achievements)
        self.calendar.set_date(entry.date)

        self.accept_btn.configure(text="Apply changes", command=self.edit_object)
        self.delete_btn = customtkinter.CTkButton(self, text="Delete entry", font=(None, 30),
                                                  command=self.delete_object, fg_color="red")
        self.delete_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="sew")

    def edit_object(self):

        if self.file_path:
            object_image = self.file_path
            print(type(object_image))
        else:
            object_image = None

        object_title = self.title_entry.get()
        object_time = self.time_entry.get()
        object_dlc = self.dlc_entry.get()
        object_achievements = self.achievements_entry.get()
        object_date = self.calendar.get_date()
        object_review = self.list_of_reviews.get()

        self.attributes("-topmost", False)
        messagebox.showinfo(title="Completed", message="Сhanges have been successfully applied!")
        self.destroy()

        return edit_entry(entry=self.entry, name=object_title, time_spent=object_time, review=object_review,
                          image=object_image, dlc=object_dlc, achievements=object_achievements, date=object_date)

    def delete_object(self):
        self.attributes("-topmost", False)
        attention = messagebox.askyesno(title="Confirmation", message="Do you really want to delete this entry?")
        if attention:
            self.destroy()
            messagebox.showinfo(title="Completed", message="Entry has been successfully deleted!")
            return delete_entry(self.entry)
        else:
            self.attributes("-topmost", True)


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("600x700")
        self.title("Options")
        self.attributes("-topmost", True)
        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self,
                                            text="About the program: Game Tracker is a program for storing and editing records of completed video games. \n\n"
                                                 "Each entry contains the name of the game, "
                                                 "image, number of hours spent, number of DLC completed, "
                                                 "number of achievements earned, overall score of the game (Bad, Okay, Good, Amazing).\n\n"
                                                 "Developed by Samuel-K732 aka zombiechest in 2024.\n\n"
                                                 "GitHub: https://github.com/Samuel-K732?tab=overview&from=2024-10-01&to=2024-10-27",
                                            corner_radius=6, font=(None, 20), wraplength=590, fg_color="#686D76",
                                            anchor="w", justify="left")
        self.label.grid(row=0, column=0, padx=0, pady=10, sticky="ew")

        self.delete_btn = customtkinter.CTkButton(self, text="Delete all data", font=(None, 30),
                                                  command=self.delete_all_data, fg_color="red")
        self.delete_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="sew")

    def delete_all_data(self):
        self.attributes("-topmost", False)
        attention = messagebox.askyesno(title="Attention",
                                        message="Do you really want to delete all the data? This action is irreversible, "
                                                "and it will be impossible to restore the data.")
        if attention:
            self.destroy()
            messagebox.showinfo(title="Completed", message="All data has been successfully deleted!")
            return delete_all_data()
        else:
            self.attributes("-topmost", True)


class LeftFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        self.list_of_years = customtkinter.CTkComboBox(self, values=get_years(), font=(None, 30))
        self.list_of_years.set("Year")
        self.list_of_years.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="new")

        self.list_of_games = customtkinter.CTkComboBox(self, values=get_names(), font=(None, 30))
        self.list_of_games.set("Game")
        self.list_of_games.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="new")

        self.add_btn = customtkinter.CTkButton(self, text="Add entry", font=(None, 30), width=300,
                                               command=self.open_add_window)
        self.add_btn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.edit_btn = customtkinter.CTkButton(self, text="Edit entry", font=(None, 30), width=300,
                                                command=self.open_edit_window)
        self.edit_btn.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.info_btn = customtkinter.CTkButton(self, text="Options", font=(None, 30), width=300,
                                                command=self.open_settings_window)
        self.info_btn.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.add_window = None
        self.edit_window = None
        self.settings_window = None

    def open_add_window(self):
        if self.add_window is None or not self.add_window.winfo_exists():
            self.add_window = AddWindow(self)
        else:
            self.add_window.focus()

    def open_edit_window(self):
        if self.edit_window is None or not self.edit_window.winfo_exists():
            game = get_game_by_name(self.list_of_games.get())
            if game is None:
                messagebox.showinfo(title="Atention",
                                    message='To edit, select a game from the drop-down game list')
            else:
                self.edit_window = EditWindow(self, entry=game)
        else:
            self.edit_window.focus()

    def open_settings_window(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()


class RightFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        label_width = 200

        self.title = customtkinter.CTkLabel(self, font=(None, 35), wraplength=600)
        self.title.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.review = customtkinter.CTkLabel(self, font=(None, 30), anchor="center", width=label_width)
        self.review.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.cover_image = customtkinter.CTkLabel(self, text="")
        self.cover_image.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.stats_frame = customtkinter.CTkFrame(self)
        self.stats_frame.grid(row=3, column=1, padx=10, pady=(20, 0), sticky="ew")
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(1, weight=1)
        self.stats_frame.grid_columnconfigure(2, weight=1)
        self.stats_frame.rowconfigure(0, weight=1)
        self.stats_frame.rowconfigure(1, weight=1)

        time_spent_header = customtkinter.CTkLabel(self.stats_frame, text="Hours spent", font=(None, 30),
                                                   anchor="center", width=label_width)
        time_spent_header.grid(row=0, column=0, padx=5, sticky="nsew")
        number_of_dlcs_header = customtkinter.CTkLabel(self.stats_frame, text="DLC", font=(None, 30), anchor="center",
                                                       width=label_width)
        number_of_dlcs_header.grid(row=0, column=1, padx=5, sticky="nsew")
        achievements_header = customtkinter.CTkLabel(self.stats_frame, text="Achievements", font=(None, 30),
                                                     anchor="center", width=label_width)
        achievements_header.grid(row=0, column=2, padx=5, sticky="nsew")

        self.time_spent = customtkinter.CTkLabel(self.stats_frame, font=(None, 30), anchor="center", width=label_width)
        self.time_spent.grid(row=1, column=0, padx=5, pady=(20, 0), sticky="nsew")

        self.number_of_dlcs = customtkinter.CTkLabel(self.stats_frame, font=(None, 30), anchor="center",
                                                     width=label_width)
        self.number_of_dlcs.grid(row=1, column=1, padx=5, pady=(20, 0), sticky="nsew")

        self.achievements = customtkinter.CTkLabel(self.stats_frame, font=(None, 30), anchor="center",
                                                   width=label_width)
        self.achievements.grid(row=1, column=2, padx=5, pady=(20, 0), sticky="nsew")

        self.date = customtkinter.CTkLabel(self, font=(None, 20), width=label_width)
        self.date.grid(row=4, column=1, pady=(20, 0), sticky="we")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Game Tracker")
        self.geometry("1100x850")
        self.minsize(1000, 850)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.left_frame.configure(width=500)

        self.right_frame = RightFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")
        self.right_frame.configure(width=600)

    def change_review_color(self, label, review):
        review = review.lower()
        if "amazing" == review:
            label.configure(text_color="#8B5DFF")
        elif "good" == review:
            label.configure(text_color="#06D001")
        elif "okay" == review:
            label.configure(text_color="#B4B4B8")
        elif "bad" == review:
            label.configure(text_color="#B8001F")

    def set_object(self, data_object):
        image = Image.open(io.BytesIO(data_object.image))
        photo = CTkImage(light_image=image, size=(450, 500))

        self.right_frame.title.configure(text=data_object.name)
        self.right_frame.cover_image.configure(image=photo)
        self.right_frame.cover_image.image = photo
        self.right_frame.time_spent.configure(text=data_object.time_spent)
        self.right_frame.number_of_dlcs.configure(text=data_object.dlc)
        self.right_frame.achievements.configure(text=data_object.achievements)
        self.right_frame.review.configure(text=data_object.review)
        self.right_frame.date.configure(text=data_object.date)
        self.right_frame.stats_frame.grid()

    def set_intro_object(self):
        image = Image.open("img/intro.jpg")
        photo = CTkImage(light_image=image, size=(550, 500))
        self.right_frame.title.configure(
            text='Welcome! Add the first entry by clicking on the "Add entry" button on the left side of the application window.')
        self.right_frame.cover_image.configure(image=photo)
        self.right_frame.time_spent.configure(text="")
        self.right_frame.number_of_dlcs.configure(text="")
        self.right_frame.achievements.configure(text="")
        self.right_frame.review.configure(text="")
        self.right_frame.stats_frame.grid_forget()
        self.right_frame.date.grid_forget()
