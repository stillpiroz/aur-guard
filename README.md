# aur-guard
A lightweight, AI-powered CLI security auditor designed for Arch Linux users. It analyzes `PKGBUILD` files, `.install` scripts, and patches from the Arch User Repository (AUR) before execution to detect malicious code, supply-chain threats, and potential security risks.

## 📁 Project Structure

```text
aur-guard/
├── src/
│   └── aur_guard/          # Main package root
│       ├── __init__.py
│       ├── api/            # AI service communication logic
│       ├── cli/            # Typer CLI commands & interface
│       ├── config/         # Configuration & system prompts
│       └── scanner/        # File parsing & security analysis
├── .gitignore
├── LICENSE
└── README.md
```

## 📊 Status

This project is currently in its early development stage. The foundational structure and basic working prototype are in place, but it is actively being built and refined.

## 📌 Roadmap & Future Goals

- [ ] Improving error handling

- [ ] Improving default prompts to increase scanning accuracy

- [ ] Moving the config directory: moving from src/config to the ~/.config/aur-guard directory (compliance with the 'XDG Base Directory Specification' standard)

- [ ] Improving the CLI: especially subcommands related to config (such as setting the model and URL)

- [ ] Integration with AUR helper: and the ability to install any package using aur-guard -S (it first scans, asks for your confirmation, and then installs with yay/paru)

- [ ] Arch package: converting into a real Arch package (easier installation, better integration with Arch Linux)

## ⚠️  Warning

If the program says a package is safe or unsafe, it is not definitive.
AI can make mistakes.
