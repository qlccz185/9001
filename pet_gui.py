import random

class Pet:
    def __init__(self, name, species="Dog"):
        self.name = name
        self.species = species
        self.days_alive = 0
        self.food = 70
        self.health = 70
        self.happiness = 70
        self.money = 500
        self.last_hospital_day = -10
        self.in_business_trip = 0

    def display_status(self):
        def progress_bar(value, max_value=100, length=20):
            filled_length = int(length * value // max_value)
            bar = '█' * filled_length + '-' * (length - filled_length)
            return f"|{bar}| {value}/{max_value}"

        print(f"\n📅 Day {self.days_alive} | 🐾 {self.name}'s Status:")
        print(f"🍗 Food:     {progress_bar(self.food)}")
        print(f"❤️ Health:   {progress_bar(self.health)}")
        print(f"😊 Happiness:{progress_bar(self.happiness)}")
        print(f"💰 Money:    {self.money}")

    def feed(self):
        if self.money < 100:
            return "❌ Not enough money to feed!"
        if self.food == 100 and self.happiness == 100:
            return "❌ Pet is full and happy. No need to feed."
        self.money -= 100
        self.food = min(100, self.food + 15)
        self.happiness = min(100, self.happiness + 5)
        return "🍽️ Feeding successful!"

    def play(self):
        if self.food < 5:
            return "❌ Not enough food to play."
        self.food -= 5
        self.health = min(100, self.health + 10)
        self.happiness = min(100, self.happiness + 10)
        return "🎮 Playtime successful!"

    def work(self):
        self.money += 150
        self.food = max(0, self.food - 5)
        self.health = max(0, self.health - 10)
        self.happiness = max(0, self.happiness - 10)
        return "💼 Worked a day and earned 150 coins."

    def hospital(self):
        if self.days_alive - self.last_hospital_day < 10:
            return "❌ Hospital visits are only allowed every 10 days."
        if self.money < 500:
            return "❌ Not enough money to go to the hospital."
        self.money -= 500
        self.health = min(100, self.health + 50)
        self.happiness = min(100, self.happiness + 10)
        self.food = min(100, self.food + 5)
        self.last_hospital_day = self.days_alive
        return "🏥 Hospital treatment successful!"

    def apply_end_of_day_rules(self):
        messages = []
        self.food = max(0, self.food - 5)
        messages.append("🐾 Lost 5 🍗 due to daily consumption.")

        if self.food == 0:
            self.health = max(0, self.health - 5)
            messages.append("⚠️ Pet is starving. Health decreased!")

        if self.happiness == 0:
            self.health = max(0, self.health - 5)
            messages.append("⚠️ Pet is very unhappy. Health decreased!")

        if self.food > 70 and self.happiness > 70:
            self.health = min(100, self.health + 5)
            messages.append("💖 Pet is in great condition. Health increased!")

        if self.food < 20 or self.health < 20 or self.happiness < 20:
            messages.append("⚠️ Pet is in poor condition. Please take care!")

        if self.money < 300:
            messages.append("⚠️ Low on money. Consider working!")

        return messages

    def trigger_special_events(self):
        if self.in_business_trip > 0:
            self.in_business_trip -= 1
            return "🧳 You are on a business trip. No actions today."

        # Sickness event
        if self.health < 30 and self.days_alive > 10:
            if random.randint(0, 15) in [1, 15]:
                self.health = 15
                self.food = 0
                self.happiness = 0
                return "🤒 Your pet got sick! Stats dropped significantly."

        # Runaway event
        if self.happiness < 40 and self.days_alive > 15:
            if random.randint(0, 15) in [2, 3, 4]:
                self.health = max(0, self.health - 10)
                self.money = max(0, self.money - 300)
                return "🏃‍♂️ Your pet ran away to play. Lost health and money!"

        # Business trip offer
        if self.days_alive > 10 and random.randint(0, 15) == 5 and self.in_business_trip == 0:
            proposed_duration = 3 if random.randint(0, 1) == 0 else 5
            proposed_income = 600 if proposed_duration == 3 else 1000
            return f"✈️ You got an offer to go on a {proposed_duration}-day business trip for {proposed_income} coins. Do you accept?"

        return None

    def is_dead(self):
        return self.health <= 0

    def is_grown_up(self):
        return self.days_alive >= 100

