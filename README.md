# Scenetax: A Markdown-Based Toolkit for Fiction Writers & World-Builders ✍️

Welcome to Scenetax\! This project provides a command-line interface (CLI) toolkit designed to streamline your writing and world-building process. Scenetax focuses on using free, open-source, and privacy-respecting tools, allowing you to manage your creative projects efficiently without proprietary software.

## ✨ Core Philosophy

Scenetax is built on the principle of **"Don't reinvent the wheel."** Instead of creating new tools, it integrates and orchestrates existing powerful open-source software. The goal is to provide a consistent interface for managing your creative workflow, from initial brainstorming to final publication.

## 🛠️ Technology Stack

We leverage the following free and open-source tools:

  * **Core Engine:** Python with `argparse` for CLI, `pathlib` for file operations, and `subprocess` for tool orchestration.
  * **Project Structure:** A standardized directory layout for organizing your creative assets.

### Tool Suggestions:

  * **Brainstorming:**
      * **Logseq** ([github.com/logseq/logseq](https://github.com/logseq/logseq)): For knowledge management, note-taking, and outlining.
      * **Freeplane** ([github.com/freeplane/freeplane](https://github.com/freeplane/freeplane)): For mind mapping and visual brainstorming.
  * **Lore & Planning:**
      * **Zettlr** ([github.com/Zettlr/Zettlr](https://github.com/Zettlr/Zettlr)): A professional markdown editor for writers, ideal for organizing lore, planning timelines, and character development.
  * **Drafting:**
      * **Zettlr** ([github.com/Zettlr/Zettlr](https://github.com/Zettlr/Zettlr)): Your primary writing environment for drafting scenes, chapters, and alternative versions.
  * **Art & Design:**
      * **Krita** ([github.com/KDE/krita](https://github.com/KDE/krita)): For digital painting and illustration.
      * **Inkscape** ([github.com/inkscape/inkscape](https://github.com/inkscape/inkscape)): For vector graphics and diagrams.
      * **Nortantis** ([github.com/jeheydorn/nortantis](https://github.com/jeheydorn/nortantis)): For world map generation.
  * **Review & Notes:**
      * **Zettlr** ([github.com/Zettlr/Zettlr](https://github.com/Zettlr/Zettlr)): For gathering feedback and writing review notes.
  * **Publishing:**
      * **Pandoc** ([github.com/jgm/pandoc](https://github.com/jgm/pandoc)): The universal document converter for turning your markdown drafts into various formats (EPUB, PDF, DOCX, etc.).
  * **Archiving & Version Control:**
      * **Rclone** ([github.com/rclone/rclone](https://github.com/rclone/rclone)): For syncing and archiving your project to cloud storage or local destinations.
      * **Git** ([git-scm.com](https://git-scm.com/)): For robust version control of your project files.

-----

## 🚀 Installation

### Prerequisites

  * **Python:** Version 3.13 or higher.
  * **Pip:** Python's package installer.
  * **Git:** For version control.

### Installing Scenetax

You can install Scenetax directly from its source code using `pip`.

1.  **Clone the repository:**

    ```bash
    https://github.com/fhsourav/scenetax.git
    cd scenetax
    ```

2.  **Install Scenetax and its Python dependencies:**

    ```bash
    pip install -e .
    ```

    The `-e` flag installs the package in "editable" mode, meaning changes you make to the source code will be reflected immediately without needing reinstallation.

-----

## 💡 Usage

Scenetax is designed to be used via the command line. The primary commands are structured for clarity and consistency.


### 1. Project Management

#### Create a New Project

`scenetax newproject <projectname>`

  * **Description:** Initializes a new project directory with the standard Scenetax folder structure.
  * **Example:** `scenetax newproject "My Fantasy Novel"`

### 2. Entity Creation

Use the `project` subcommands to generate templates for different project elements:

  * `scenetax project character --create <name>`
      * **Description:** Creates markdown file (character sheet) for character <name>.
      * **Example:** `scenetax project character --create Sir Reginald`
      * **Versioning:** Use `--version <n>` to create a new version from an existing character sheet.

  * `scenetax project location --create <name>`
      * **Description:** Creates markdown file for location <name>.
      * **Example:** `scenetax project location --create The Whispering Woods`
      * **Versioning:** Use `--version <n>` to create a new version from an existing location sheet.

  * `scenetax project group --create <name>`
      * **Description:** Creates markdown file for group <name>.
      * **Example:** `scenetax project group --create Guardians of the City`
      * **Versioning:** Use `--version <n>` to create a new version from an existing group sheet.

### 3. Writing & Drafting

Commands to assist with the writing process:

  * `scenetax project scene --chapter`
      * **Description:** Creates a new chapter folder and adds a new scene file within it.
      * **Example:** `scenetax project scene --chapter`

  * `scenetax project scene --volume`
      * **Description:** Creates a new volume folder and its subfolders, creates the first chapter and adds a new scene file within it..
      * **Example:** `scenetax project scene --volume`

  * `scenetax project scene`
      * **Description:** Creates a new scene in the last available chapter, maintaining order.
      * **Example:** `scenetax project scene`

### 4. Project-Wide Operations

Commands for project-wide operations:

  * `scenetax project --archive`
      * **Description:** Archives the entire project directory into a compressed file (e.g., `.tar.gz`).
      * **Example:** `scenetax project --archive`

  * *(Planned)* `scenetax project --commit`
      * **Description:** Stages all changes, commits them with an automated message, and pushes to Git.
      * **Example:** `scenetax project --commit`

  * *(Planned)* `scenetax project compile --epub|--pdf`
      * **Description:** Uses Pandoc to compile your markdown project into a final document format (e.g., PDF, EPUB).
      * **Example:** `scenetax project compile --epub`

-----

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. See the [LICENSE]() file for more details.

-----
