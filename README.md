# ChatBridge

ChatBridge is a seamless background utility that allows you to translate game chat (or any selectable text) instantly with a single hotkey press.

## Features
- **One-Key Translation:** Press a single hotkey (default: `F8`) to instantly translate highlighted text.
- **Auto Detect Language:** Automatically detects the text's language context (Thai <-> English, Japanese -> English) and routes the translation accordingly.
- **Configurable:** Easily customize your preferred hotkey and default languages via `config.json`.
- **Fast & Lightweight:** Operates seamlessly in the background with minimal footprint using `GoogleTranslator`.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Beabexj/ChatBridge.git
   cd ChatBridge
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed. Then, install the locked requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the program:**
   ```bash
   python src/main.py
   ```
2. **Translate Text:**
   - Highlight the text you want to translate (e.g., in a game chat, browser, or notepad).
   - Press the configured hotkey (default: `F8`).
   - The text will automatically be copied, translated, and pasted back in place!

## Configuration
Upon first run, a `config.json` file is generated at the root directory. You can edit this file to change the hotkey and default source/target languages.

## Roadmap
See our plans for future development in [docs/roadmap.md](docs/roadmap.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
