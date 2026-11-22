# N-dine-lang

**Author:** Kelly R. Morgan, Assistant Professor of Information Technology  
**Affiliation:** Navajo Technical University (Crownpoint, NM)  
**Created:** November 2026  

---

## Overview

**`N-dine-lang`** is a lightweight, deterministic slot-tag intermediate representation and command syntax inspired by **Diné Bizaad** (the Navajo language). Designed for seamless interoperability between human languages (**Diné Bizaad**, **English**), **AI language models**, and **Python/SQLite** data pipelines, `N-dine-lang` removes spelling ambiguity, diacritic friction, and irregular word-order rules by locking meaning into strict, readable role slots.

---

## Requirements

This project targets **Linux and WSL (Windows Subsystem for Linux)**.

* **Python 3.6 or newer** (tested with Python 3.12 in WSL2). Confirm with:

  ```bash
  python3 --version
  ```

* **The `venv` module.** On Debian/Ubuntu/WSL, install Python and venv support with:

  ```bash
  sudo apt update
  sudo apt install -y python3 python3-venv
  ```

* **Dependencies:** `google-genai` (Gemini SDK) and `python-dotenv` (loads `.env`). Both are listed in the generated `requirements.txt` and installed in Setup, Step 4. `python-dotenv` is optional at runtime: `ndine.py` falls back to a small built-in `.env` parser if it is not installed.
* **Optional:** a **Google Gemini API key** for Gemini-backed features. Create one at [Google AI Studio](https://aistudio.google.com/apikey) and set `GEMINI_API_KEY` in `.env` (see Setup, Step 2).
* **Optional:** the `ping` utility (used only by the `M-now ... V-ping` action). Usually present on WSL2 and desktop Linux; if not, run `sudo apt install -y iputils-ping`.

---

## Core Architecture (`T S V O L`)

Every `N-dine-lang` expression follows a strict, unchanging canonical slot order:

```text
[T/Q/C/M]-[time]  S-[subject]  V-[verb]  O-[object]  L-[location]
```

| Prefix | Role | Description | Example |
| :--- | :--- | :--- | :--- |
| **`T-`** | Tense / Time | `pst` (past), `prs` (present), `fut` (future) | `T-pst`, `T-fut-tomorrow` |
| **`Q-`** | Question | Interrogative marker with tense | `Q-prs` |
| **`C-`** | Condition | Conditional clause (`if`) | `C-prs` |
| **`M-`** | Mode / Command | Imperative execution trigger | `M-now` |
| **`S-`** | Subject | Actor or pronoun (`1sg`, `2sg`, `3sg`, `1pl`, `3pl`) | `S-1sg`, `S-admin` |
| **`V-`** | Verb | Core action root (`un-` for negation) | `V-drink`, `V-un-allow` |
| **`O-`** | Object | Direct receiver or target argument | `O-water`, `O-rout-tul` |
| **`L-`** | Location | Physical or logical destination/environment | `L-home`, `L-serv-dom` |

---

## Two-Way Language Bridge Examples

`N-dine-lang` acts as a neutral pivot layer between **English (SVO)** and plain-ASCII **Diné Bizaad (SOV)**—eliminating the need for glottal stops (`ʼ`) or accent marks during processing:

* **Example 1 (Past Action + Location)**
  * **`N-dine-lang`:** `T-pst S-boy V-see O-dog L-home.`
  * **English:** The boy saw the dog at home.
  * **Diné (Plain ASCII):** `Hooghandi ashkii leechai yiyiiltsa.`

* **Example 2 (Present Action)**
  * **`N-dine-lang`:** `T-prs S-1sg V-drink O-cold-water.`
  * **English:** I am drinking cold water.
  * **Diné (Plain ASCII):** `To sikazi yishdla.`

* **Example 3 (Future Action + Time & Location)**
  * **`N-dine-lang`:** `T-fut-tomorrow S-1pl V-go L-flagstaff.`
  * **English:** Tomorrow we will go to Flagstaff.
  * **Diné (Plain ASCII):** `Yiskaago kinlanigoo diikah.`

---

## Repository Structure

```text
N-dine-lang/
├── .gitignore       # Excludes generated databases, caches, and environment files
├── CITATION.cff     # Academic citation metadata for GitHub & Zenodo
├── LICENSE          # Dual MIT (code) & CC BY 4.0 (specification/docs)
├── README.md        # Specification overview, setup steps, and citation
├── bootstrap.py     # Creates db/, csv/, md/, .env, and requirements.txt (Setup, Step 2)
└── ndine.py         # Official Python reference parser, SQLite builder & runner
```

The following items are **created locally** when you bootstrap and run the project and are not part of the repository:

```text
N-dine-lang/
├── .env                 # Local secret: GEMINI_API_KEY (bootstrap.py)
├── .venv/               # Python virtual environment (Setup, Step 3)
├── csv/                 # CSV import/export workspace (bootstrap.py)
├── db/
│   └── dine_lang.db     # SQLite lexicon database, generated on first run
├── md/                  # Markdown notes/output workspace (bootstrap.py)
└── requirements.txt     # Dependencies: google-genai, python-dotenv (bootstrap.py)
```

> `__pycache__/` is not present initially. Python creates it only when `ndine` is imported (for example, from the Python shell in the Interaction Walkthrough), and it is safe to delete.

---

## Setup & Installation

These steps apply to **Linux and WSL**. In WSL, run every command in your Linux terminal (not PowerShell or `cmd`).

> **WSL tip:** keep the project inside the Linux filesystem — for example `~/projects/` — not under `/mnt/c/...`. Working from the Windows drive is noticeably slower and can cause permission and virtual-environment problems.

### 1. Clone the repository

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/krmorgan-git/N-dine-lang.git
cd N-dine-lang
```

### 2. Initialize the project layout

Immediately after cloning, run the bootstrap script from the project root:

```bash
python3 bootstrap.py
```

This creates  `csv/`, `db/`, `md/`, and `.env`, and writes `requirements.txt` if it is missing.

> **Optional:** open `.env` and add your Gemini API key — only needed for Gemini-backed features. If you are not using Gemini, skip this step.

```ini
GEMINI_API_KEY=your-api-key-here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey). `.env` is git-ignored, so the key stays local and must never be committed. As an alternative, export the variable in your shell — environment variables take precedence over `.env`:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Existing files are preserved; `python bootstrap.py --force` regenerates the templates (and overwrites `.env`, so only use it before adding a real key).

### 3. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt should now show the environment name, for example `(.venv) user@host:~/projects/N-dine-lang$`.

If this fails with an `ensurepip is not available` error, install the venv package and retry:

```bash
sudo apt install -y python3-venv
```

### 4. Install dependencies

Upgrade `pip`, then install the dependencies declared in `requirements.txt` (`google-genai` and `python-dotenv`):

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the built-in demo

From the project root (`N-dine-lang/`):

```bash
python ndine.py
```

Expected output:

```text
1. ASCII Sanitizer: Taa akwii abini to sikazi yishdla
2. Slot Parser: {'T': 'pst', 'S': 'boy', 'V': 'see', 'O': 'dog', 'L': 'home'}
3. Query Command: {'status': 'ok', 'action': 'find', 'target': 'water', 'results': [(1, 'To yishdla', 'I am drinking water.', 'T-prs S-1sg V-drink O-water.')]}
```

The first run creates `db/dine_lang.db` (the engine's default path) and seeds two sample lexicon entries. Because `db/` and `*.db` are in `.gitignore`, the database will not appear in `git status`. To start over, delete `db/dine_lang.db` and run the script again.

### 6. Deactivate when finished

```bash
deactivate
```

### Other platforms (brief)

* **macOS:** the same commands work (`python3` is provided by the system or Homebrew).
* **Windows (native):** use `python -m venv .venv` and activate with `.venv\Scripts\Activate.ps1` in PowerShell. WSL is the path documented above.

---

## Interaction Walkthrough (`ndine.py`)

Let's revisit what happens when you run `python ndine.py` (Setup, Step 5). The script creates and seeds the database, then prints three demonstrations. This walkthrough explains each one and shows how to experiment with the same engine interactively. Start a Python shell from the project root with the virtual environment activated:

```console
$ python
>>> from ndine import NDineEngine
>>> engine = NDineEngine()          # creates or opens db/dine_lang.db
```

**1. ASCII Sanitizer** — converts Diné Bizaad text to plain ASCII by stripping accents, glottal stops, and barred letters:

```python
>>> engine.to_plain_ascii("Tó sikʼazí yishdlą́.")
'To sikazi yishdla'
```

**2. Slot Parser** — splits an N-dine-lang sentence into its role slots:

```python
>>> engine.parse("T-pst S-boy V-see O-dog L-home.")
{'T': 'pst', 'S': 'boy', 'V': 'see', 'O': 'dog', 'L': 'home'}
```

**3. Query Command** — searches the lexicon database. It is seeded by the first `python ndine.py` run; add your own entries with `engine.add_entry(...)`:

```python
>>> engine.execute_command("Q-prs S-1sg V-find O-water L-lexicon.")
{'status': 'ok', 'action': 'find', 'target': 'water', 'results': [(1, 'To yishdla', 'I am drinking water.', 'T-prs S-1sg V-drink O-water.')]}
```

---

## Citation

If you use **`N-dine-lang`**, its specification, or the reference Python engine in academic research, curriculum development, or software projects, please cite:

> Morgan, K. R. (2026). *N-dine-lang: A Deterministic Slot-Tag Intermediate Representation for Diné Bizaad, English, and Computational Pipelines*. Navajo Technical University, Crownpoint, NM.

---

## License

* **Software & Source Code (`*.py`):** Licensed under the [MIT License](LICENSE).
* **Specification, Documentation & Linguistic Datasets (`*.md`, `*.csv`, `*.db`):** Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
