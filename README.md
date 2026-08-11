# Validated_pesel
Telegram bot for validation, parsing, and sorting of Polish PESEL numbers, built with Python and Object-Oriented Programming (OOP)
# 🇵🇱 Polish PESEL Validator Telegram Bot

A Telegram bot built with Python (`pyTelegramBotAPI`) that validates Polish PESEL numbers, extracts personal data (date of birth, gender), and allows sorting/managing a list of numbers.

This project was developed as a practical study of **Object-Oriented Programming (OOP)** principles, transforming an academic requirement into an interactive Telegram interface.

## ✨ Features

- **PESEL Validation:**
  - Length and digit check.
  - Birth date extraction (supports 20th and 21st-century encodings).
  - Control digit (checksum) calculation using standard weights `[1, 3, 7, 9, 1, 3, 7, 9, 1, 3]`.
- **Data Extraction:**
  - Identifies gender based on the 10th digit.
  - Constructs a valid `datetime` birth date object.
- **Sorting & Filtering (via Inline Keyboards):**
  - Sort PESELs by birth date.
  - Sort PESELs by gender.
  - Combined sorting (by gender and date).
  - Prevent duplicate entries.
- **File Support:** Internal class methods to load from and save to external `.txt` files.

## 🛠️ Architecture & OOP Design

The project is structured around two core classes:
1. `PESEL`: Encapsulates a single PESEL entity, handling its validation logic, birth date parsing, and gender determination.
2. `PeselList`: Manages a collection of `PESEL` instances, handling batch sorting algorithms and file I/O operations.

## 🚀 Tech Stack

- **Python 3.x**
- **pyTelegramBotAPI (`telebot`)**
- **datetime** (standard library)

## 🔧 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
