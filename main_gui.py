import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from pet_gui import Pet
import os

class PetGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet Game")

        self.pet = None
        self.images = self.load_images()

        self.message_label = None

        self.setup_start_screen()

    def load_images(self):
        base_dir = os.path.dirname(__file__)  
        image_dir = os.path.join(base_dir, "images")  

        image_files = {
            "start": "start.jpg",
            "feed": "feed.jpg",
            "hospital": "hospital.jpg",
            "lose": "lose.jpg",
            "play": "play.jpg",
            "runaway": "runaway.jpg",
            "sick": "sick.jpg",
            "warning": "warning.jpg",
            "win": "win.jpg",
            "work": "work.jpg",
            "business": "business.jpg"
        }

        imgs = {}
        for name, filename in image_files.items():
            path = os.path.join(image_dir, filename)
            imgs[name] = ImageTk.PhotoImage(Image.open(path).resize((150, 150)))
        return imgs


    def setup_start_screen(self):
        self.clear_screen()
        self.name_label = tk.Label(self.root, text="Enter your pet's name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Warning", "Please enter your pet's name!")
            return
        self.pet = Pet(name)
        self.show_start_image()

    def show_start_image(self):
        self.clear_screen()
        self.show_image("start")
        tk.Label(self.root, text=f"{self.pet.name} is ready! Click below to start the game").pack()
        tk.Button(self.root, text="Continue", command=self.update_game_screen).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_game_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Day {self.pet.days_alive + 1}").pack()
        tk.Label(self.root, text=f"Pet: {self.pet.name}").pack()

        self.status_label = tk.Label(self.root, text=self.get_status_text(), justify="left")
        self.status_label.pack()

        self.add_progress_bar("🍗 Food", self.pet.food)
        self.add_progress_bar("❤️ Health", self.pet.health)
        self.add_progress_bar("😊 Happiness", self.pet.happiness)
        self.add_progress_bar("💰 Money", self.pet.money, max_value=4000)

        if self.pet.food < 20 or self.pet.health < 20 or self.pet.happiness < 20 or self.pet.money < 300:
            self.show_image("warning")
        else:
            self.show_image("start")

        tk.Button(self.root, text="Feed", command=self.feed).pack()
        tk.Button(self.root, text="Play", command=self.play).pack()
        tk.Button(self.root, text="Work", command=self.work).pack()
        tk.Button(self.root, text="Hospital", command=self.hospital).pack()

        self.message_label = tk.Label(self.root, text="", fg="blue", wraplength=300, justify="left")
        self.message_label.pack(pady=5)

    def log_message(self, message):
        if self.message_label:
            self.message_label.config(text=message)

    def get_status_text(self):
        return f"""🍗 Food: {self.pet.food}/100
❤️ Health: {self.pet.health}/100
😊 Happiness: {self.pet.happiness}/100
💰 Money: {self.pet.money}
"""

    def add_progress_bar(self, label_text, value, max_value=100):
        frame = tk.Frame(self.root)
        frame.pack(pady=2)

        tk.Label(frame, text=label_text, width=6, anchor='w').pack(side="left")
        progress = ttk.Progressbar(frame, length=200, maximum=max_value)
        progress["value"] = value
        progress.pack(side="left")
        tk.Label(frame, text=f"{value}/{max_value}", width=10, anchor='w').pack(side="left")

    def show_image(self, key):
        if key in self.images:
            panel = tk.Label(self.root, image=self.images[key])
            panel.image = self.images[key]
            panel.pack()

    def next_day(self):
        self.pet.days_alive += 1

        # Trigger special events
        special_event_msg = self.pet.trigger_special_events()
        if special_event_msg:
            if "Business Trip" in special_event_msg and "Accept?" in special_event_msg:
                duration = 3 if "3 days" in special_event_msg else 5
                income = 600 if duration == 3 else 1000
                result = messagebox.askyesno("Business Trip Offer", special_event_msg)
                if result:
                    self.pet.money += income
                    self.pet.in_business_trip = duration
                    self.after_action_screen("business", f"You accepted a {duration}-day business trip and earned {income} coins.")
                    return
                else:
                    self.log_message("You declined the business trip offer.")

            elif "got sick" in special_event_msg:
                self.after_action_screen("sick", special_event_msg)
                return
            elif "ran away" in special_event_msg:
                self.after_action_screen("runaway", special_event_msg)
                return
            
            elif "on a business trip" in special_event_msg:
                daily_msgs = self.pet.apply_end_of_day_rules()

                if self.pet.is_dead():
                    self.clear_screen()
                    self.show_image("lose")
                    tk.Label(self.root, text=f"{self.pet.name} died after surviving {self.pet.days_alive} days.").pack()
                    return
                elif self.pet.is_grown_up():
                    self.clear_screen()
                    self.show_image("win")
                    tk.Label(self.root, text=f"🎉 Congratulations! You raised {self.pet.name} for 100 days!").pack()
                    return

                self.after_action_screen("business", special_event_msg + "\n\n" + "\n".join(daily_msgs))
                return
            
            else:
                self.log_message(special_event_msg)

        daily_msgs = self.pet.apply_end_of_day_rules()
        if self.pet.is_dead():
            self.clear_screen()
            self.show_image("lose")
            tk.Label(self.root, text=f"{self.pet.name} died after surviving {self.pet.days_alive} days.").pack()
        elif self.pet.is_grown_up():
            self.clear_screen()
            self.show_image("win")
            tk.Label(self.root, text=f"🎉 Congratulations! You raised {self.pet.name} for 100 days!").pack()
        else:
            self.update_game_screen()
            self.log_message("\n".join(daily_msgs))

    def after_action_screen(self, image_key, message):
        self.clear_screen()
        self.show_image(image_key)
        tk.Label(self.root, text=message, wraplength=300).pack(pady=10)
        tk.Button(self.root, text="Continue", command=self.next_day).pack()

    def work(self):
        msg = self.pet.work()
        self.after_action_screen("work", msg)

    def feed(self):
        msg = self.pet.feed()
        self.after_action_screen("feed", msg)

    def play(self):
        msg = self.pet.play()
        self.after_action_screen("play", msg)

    def hospital(self):
        msg = self.pet.hospital()
        self.after_action_screen("hospital", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = PetGameGUI(root)
    root.mainloop()

