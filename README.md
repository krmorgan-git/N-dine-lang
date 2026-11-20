# N-dine-lang

**Author:** Kelly R. Morgan, Assistant Professor of Information Technology  
**Affiliation:** Navajo Technical University (Crownpoint, NM)  
**Created:** November 2026  

---

## Overview

**`N-dine-lang`** is a lightweight, deterministic slot-tag intermediate representation and command syntax inspired by **Diné Bizaad** (the Navajo language). Designed for seamless interoperability between human languages (**Diné Bizaad**, **English**), **AI language models**, and **Python/SQLite** data pipelines, `N-dine-lang` removes spelling ambiguity, diacritic friction, and irregular word-order rules by locking meaning into strict, readable role slots.

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
n-dine-lang/
├── README.md        # Specification overview, authorship, and citation
├── LICENSE          # Dual MIT (code) & CC BY 4.0 (specification/docs)
├── CITATION.cff     # Academic citation metadata for GitHub & Zenodo
└── ndine.py         # Official Python reference parser, SQLite builder & runner
```

---

## Quickstart (`ndine.py`)

```python
from ndine import NDineEngine

engine = NDineEngine("dine_lang.db")

# 1. Sanitize Diné text to plain ASCII
clean = engine.to_plain_ascii("Tó sikʼazí yishdlą́.")
print(clean)  # Output: To sikazi yishdla.

# 2. Parse N-dine-lang slots into a dictionary
slots = engine.parse("T-pst S-boy V-see O-dog L-home.")
print(slots)  # {'T': 'pst', 'S': 'boy', 'V': 'see', 'O': 'dog', 'L': 'home'}

# 3. Execute an N-dine-lang database query command
engine.execute("Q-prs S-1sg V-find O-water L-lexicon.")
```

---

## Citation

If you use **`N-dine-lang`**, its specification, or the reference Python engine in academic research, curriculum development, or software projects, please cite:

> Morgan, K. R. (2026). *N-dine-lang: A Deterministic Slot-Tag Intermediate Representation for Diné Bizaad, English, and Computational Pipelines*. Navajo Technical University, Crownpoint, NM.

---

## License

* **Software & Source Code (`*.py`):** Licensed under the [MIT License](LICENSE).
* **Specification, Documentation & Linguistic Datasets (`*.md`, `*.csv`, `*.db`):** Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
