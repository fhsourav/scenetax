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

### 1\. Project Management

#### Create a New Project

`scenetax newproject <projectname>`

  * **Description:** Initializes a new project directory with the standard Scenetax folder structure.
  * **Example:** `scenetax newproject my_fantasy_novel`

#### Create a Project with Legacy Data

Use the `--sequel`, `--prequel`, or `--spinoff` flags to import worldbuilding from an existing project.

  * `scenetax newproject <projectname> --sequel <oldproject>`

      * **Description:** Creates a new project based on an existing one, copying all worldbuilding data.
      * **Example:** `scenetax newproject my_next_novel --sequel my_first_novel`

  * `scenetax newproject <projectname> --prequel <oldproject> --year <year>`

      * **Description:** Creates a new project as a prequel. It copies worldbuilding data that existed *prior* to the specified `<year>` in the `<oldproject>`.
      * **Example:** `scenetax newproject ancient_history --prequel my_fantasy_novel --year 100`

  * `scenetax newproject <projectname> --spinoff <oldproject> --year <year>`

      * **Description:** Creates a new project as a spinoff, copying worldbuilding data from the `<oldproject>` up to a specified `<year>`, allowing for a divergent timeline.
      * **Example:** `scenetax newproject alternate_timeline --spinoff my_fantasy_novel --year 589`

### 2\. Item Creation

Use the `create` command to generate templates for different project elements.

  * `scenetax project create --character <name1> [name2] ...`
      * **Description:** Creates markdown files (character sheets) for one or more characters.
      * **Example:** `scenetax project create --character John Jane "Sir Reginald"`
  * `scenetax project create --location <name1> [name2] ...`
      * **Description:** Creates markdown files for one or more locations.
      * **Example:** `scenetax project create --location "Eldoria" "The Whispering Woods"`
  * `scenetax project create --group <name1> [name2] ...`
      * **Description:** Creates markdown files for one or more groups or organizations.
      * **Example:** `scenetax project create --group "The Guild" "Guardians of the City"`

### 3\. Writing & Drafting

Commands to assist with the writing process.

  * `scenetax project write --scene`
      * **Description:** Creates a new scene file. It will place the scene in the last available chapter folder, sorting existing scenes to maintain order.
      * **Example:** `scenetax project write --scene "The Discovery"`
  * `scenetax project write --scene --newchapter`
      * **Description:** Creates a new chapter folder and then adds a new scene file within it.
      * **Example:** `scenetax project write --scene --newchapter "The Confrontation"`

### 4\. Project Management

Commands for project-wide operations.

  * `scenetax project --archive`
      * **Description:** Archives the entire project directory into a compressed file (e.g., `.tar.gz`) using Rclone and Git.
      * **Example:** `scenetax project --archive`
  * `scenetax project --commit`
      * **Description:** Stages all changes, commits them with an automated message (e.g., "WIP: Updated scenes"), and pushes to Git.
      * **Example:** `scenetax project --commit`
  * `scenetax project --compile`
      * **Description:** Uses Pandoc to compile your markdown project into a final document format (e.g., PDF, EPUB).
      * **Example:** `scenetax project --compile --format pdf`

-----

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. See the [LICENSE]() file for more details.

-----
