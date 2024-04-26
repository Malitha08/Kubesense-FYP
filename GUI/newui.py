import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
from DatasetCreator import DatasetCreator
from MultiModelCommandGenerator import KubesenseGenerator
from driver import KubeDriver

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class WelcomeScreen(tk.Tk):
    def __init__(self, main_screen):
        super().__init__()
        self.main_screen = main_screen

        # Configure window
        self.title("Welcome to Kubesense")
        self.geometry("372x250")

        # Center the window on the screen
        self.center_window()

        # Create frame for content
        self.content_frame = customtkinter.CTkFrame(self, width=300)
        self.content_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Create label for credentials
        self.label = customtkinter.CTkLabel(self.content_frame, text="Enter Cluster credentials:", font=customtkinter.CTkFont(size=14))
        self.label.place(relx=0.5, rely=0.2, anchor="center")

        # Create entry widget for password
        self.password_entry = customtkinter.CTkEntry(self.content_frame, placeholder_text="Password")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Create login button
        self.login_button = customtkinter.CTkButton(self.content_frame, text="Login", command=self.login, fg_color="blue", text_color="white")
        self.login_button.place(relx=0.5, rely=0.8, anchor="center")


    def center_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position for the window to be centered
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2

        # Set the window position
        self.geometry("+{}+{}".format(x, y))

    def login(self):
        # Perform authentication here
        # For demonstration, let's check if the entered password is "password"
        entered_auth_login = self.password_entry.get()
        if entered_auth_login == "gcloud container clusters get-credentials cluster-fyp --zone us-central1-c --project kubesense":
            self.main_screen.show()
            self.destroy()
        else:
            tk.messagebox.showerror("Error", "Invalid credentials. Please try again.")




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.welcome_screen = None

        # configure window
        self.title("Kubesense")
        self.geometry(f"{800}x{450}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="K8 Clusters", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter required operation in the cluster")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Run', command=self.generate_command)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create output text box
        self.output_textbox = tkinter.Text(self, height=10, width=40, bg="black", highlightthickness=2, fg="white")
        self.output_textbox.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        font = ("Courier New", 14, "bold")  # Change the font family and size as needed
        self.output_textbox.config(font=font)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='Generate command')
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text='Execute command')
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")

        # Create a button to go back to the welcome screen
        # self.back_button = customtkinter.CTkButton(self, text="Back", command=self.go_back)
        # self.back_button.grid(row=1, column=0)

        self.hide()

    # def go_back(self):
    #     # self.main_screen.show_welcome_screen()
    #     if self.welcome_screen:
    #         self.welcome_screen.show()
    #         self.hide()
    #
    # def show_welcome_screen(self):
    #     if self.welcome_screen:
    #         self.welcome_screen.show()
    #         self.hide()

    def show(self):
        self.deiconify()

    def hide(self):
        self.withdraw()

    def generate_command(self):

        entered_text = self.entry.get()
        generate_checked = self.checkbox_1.get()
        execute_checked = self.checkbox_2.get()

        # ---------------------------------------------------------
        file_path = 'C:/Users/acer/Desktop/(DS and AI) Lectures/4th Year/CM4605-Individual Research Project/kubesense/Kubesense-FYP/Kubesense/Dataset/updted_data_with_class.json'
        creator = DatasetCreator(json_path=file_path, csv_path='data.csv')
        data = creator.create_dataset()

        kubesense_generator = KubesenseGenerator()
        driver = KubeDriver(data, kubesense_generator)
        if generate_checked == 1 and execute_checked == 1:
            generated_command = driver.generate_and_execute(entered_text)
        elif generate_checked == 1:
            generated_command = driver.generate(entered_text)
        elif execute_checked == 1:
            generated_command = driver.generate_and_execute(entered_text)
        else:
            generated_command = driver.generate(entered_text)


        print(generate_checked)
        print(execute_checked)

        # kubesense_generator = KubesenseGenerator()
        # driver = KubeDriver(data, kubesense_generator)
        #
        # generated_command = driver.generate(entered_text)
        # ---------------------------------------------------------

        # Clear the output textbox
        self.output_textbox.delete("1.0", tkinter.END)
        # Insert the processed text into the output textbox
        self.output_textbox.insert(tkinter.END, generated_command)

    def process_text(self, text):
        # Placeholder for processing logic
        # Here you would pass the text through your other model and get the processed output
        # For demonstration purposes, let's just return the input text reversed
        return text[::-1]

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type ifn a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # customtkinter.set_appearance_mode(new_appearance_mode)
        try:
            customtkinter.set_appearance_mode(new_appearance_mode)
        except Exception as e:
            print("Error changing appearance mode:", e)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

if __name__ == "__main__":
    # Create an instance of the main application
    app = App()

    # Create an instance of the welcome screen
    welcome_screen = WelcomeScreen(app)
    app.welcome_screen = welcome_screen

    # Start the main loop with the welcome screen
    welcome_screen.mainloop()
