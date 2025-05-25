# 🐾 Virtual Puppy Guardian

A Python + Tkinter-based 100-day pet simulation game where you take care of a virtual puppy. Keep it happy, healthy, and well-fed — and help it survive for 100 days to win!

## 🎮 Game Overview
In Virtual Puppy Guardian, your job is to take care of your puppy by managing four key stats: Food, Health, Happiness, and Money. Each day, you choose one activity: feed, play, work, or go to the hospital.

Random events such as getting sick, running away, or going on a business trip may occur. If any vital stat reaches zero, the puppy dies. Make it to day 100 to win!

## 📌 How to Play
Each day, you can perform one of the following actions:

🍗 Feed: Increases food and slightly boosts happiness.

🎾 Play: Increases happiness but decreases health.

💼 Work: Earns money but decreases health and happiness.

🏥 Hospital: Restores health (can only be used once every 10 days and costs money).

## 📅 End of Day Rules
Loses 5 food automatically each day.

If food is 0, health decreases due to starvation.

If happiness is 0, health decreases due to depression.

If both food and happiness are above 70, health slightly improves.

Random events may occur (e.g., illness, runaway, business trip).

## 🎯 Game Goal
Keep all key stats above zero and survive for 100 days!

# Simply run main_gui.py to start the game!
