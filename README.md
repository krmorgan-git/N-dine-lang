# N-dine-lang

**Author:** Kelly R. Morgan, Assistant Professor of Information Technology  
**Affiliation:** Navajo Technical University (Crownpoint, NM & Chinle, AZ)  
**Created:** November 2026  

---

## Overview

**`N-dine-lang`** is a lightweight, deterministic slot-tag intermediate representation and command syntax inspired by **Diné Bizaad** (the Navajo language). Designed for seamless interoperability between human languages (**Diné Bizaad**, **English**), **AI language models**, and **Python/SQLite** data pipelines, `N-dine-lang` removes spelling ambiguity, diacritic friction, and irregular word-order rules by locking meaning into strict, readable role slots.

---

## Core Architecture (`T S V O L`)

Every `N-dine-lang` expression follows a fixed left-to-right slot order:

```text
T-[time]  S-[subject]  V-[verb]  O-[object]  L-[location]
```

| Prefix | Role | Plain-English Meaning | Example |
| :--- | :--- | :--- | :--- |
| **`T-`** | Time | `pst` (past), `prs` (present), `fut` (future) | `T-pst`, `T-fut-tomorrow` |
| **`S-`** | Subject | Who does the action (`1sg` = I, `2sg` = you, `1pl` = we, or a noun) | `S-1sg`, `S-boy` |
| **`V-`** | Verb | The action or state (`un-` means *not*) | `V-drink`, `V-un-like` |
| **`O-`** | Object | What receives the action | `O-water`, `O-coffee` |
| **`L-`** | Location | Where it happens or where someone is going | `L-home`, `L-flagstaff` |

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

## Multi-Step Reasoning (The 4-Stage Diné Cycle)

For math, programming, and quantum-computing workflows, `N-dine-lang` pairs with the 4-stage Diné cycle—keeping one flat `T S V O L` expression per step:

1. **Thinking (*Nitsáhákees*):** Identify given values and unknowns (`T-prs S-inputs V-be O-2-and-3.`).
2. **Planning (*Nahatʼá*):** Break into ordered operations (`T-fut S-1pl V-add O-2-and-3.`).
3. **Implementing (*Iiná*):** Execute one operation per line (`T-prs S-1pl V-add O-2-and-3.`).
4. **Reflecting (*Siihasin*):** Verify the result and constraints (`T-prs S-result V-equal O-5.`).

---

## Proof-of-Concept Applications & Resources

Use the links below to download and test live proof-of-concept apps built on **`N-dine-lang`** (each includes a one-command `bash start.sh` / `start.bat` launcher and automatically downloads the fine-tuned Gemma 3 1B GGUF model on first run):

| Repository | Purpose | Quick Launch |
| :--- | :--- | :--- |
| **[`N-dine-lang-translator`](https://github.com/krmorgan-git/N-dine-lang-translator)** | Starter Flask web translator (`English → N-dine-lang → Diné ASCII`) + SQLite lookup | `bash start.sh` / `start.bat` |
| **[`N-dine-lang-app`](https://github.com/krmorgan-git/N-dine-lang-app)** | Standalone offline Diné translator with curated modern lexicon & reverse translation | `bash start.sh` / `start.bat` |
| **[`N-dine-lang-math`](https://github.com/krmorgan-git/N-dine-lang-math)** | Interactive 4-stage Diné math, geometry, and quantum-computing preview demo | `bash start.sh` / `start.bat` |
| **[`N-dine-lang` Releases (`v1.0`)](https://github.com/krmorgan-git/N-dine-lang/releases)** | Direct download for `gemma3-1b-ndine-Q4_K_M.gguf` (~777 MB) used by the demo apps | Auto-downloaded on first run |

- **`N-dine-lang-studio`** — Internal curation, JSONL export, and Google Colab Gemma 3 LoRA training hub that produces the lexicon and `.gguf` model.

---

## Citation

If you use **`N-dine-lang`**, its specification, or the reference Python engine in academic research, curriculum development, or software projects, please cite:

> Morgan, K. R. (2026). *N-dine-lang: A Deterministic Slot-Tag Intermediate Representation for Diné Bizaad, English, and Computational Pipelines*. Navajo Technical University, Crownpoint, NM.

---

## License

* **Software & Source Code (`*.py`):** Licensed under the [MIT License](LICENSE).
* **Specification, Documentation & Linguistic Datasets (`*.md`, `*.csv`, `*.db`):** Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
