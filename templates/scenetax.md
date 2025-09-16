---
# =========================
# NOVEL METADATA TEMPLATE
# =========================
# This file lives at the root of your project and acts as the single source of truth
# for your novel's creative direction, structure, and project management data.

# Core Identity
title: "{{ title }}"                       # Working title of the novel
series: "{{ series }}"                     # Series name (leave blank if standalone)
series_number: {{ series_number }}         # Position in series (integer)
author: "{{ author }}"                     # Author name or pen name
status: "{{ status }}"                     # outline | drafting | editing | complete
version: "{{ version }}"                   # Semantic version for tracking changes

# Genre & Tone
genre: "{{ genre }}"                       # Primary genre (e.g., High Fantasy)
subgenres:                                 # Secondary genre tags for nuance
{% for subgenre in subgenres -%}
  - "{{ subgenre }}"
{% endfor %}
tone_keywords:                             # Adjectives or short phrases for mood/tone
{% for keyword in tone_keywords -%}
  - "{{ keyword }}"
{% endfor %}

# World & Setting
primary_world: "{{ primary_world }}"       # Main world or realm name
primary_region: "{{ primary_region }}"     # Key region/kingdom/continent
time_period: "{{ time_period }}"           # In-world historical era
magic_system: "{{ magic_system }}"         # Short label for your magic system
technology_level: "{{ technology_level }}" # Tech baseline (e.g., Late Medieval)

# Themes & Motifs
themes:                                    # Big-picture ideas explored in the story
{% for theme in themes -%}
  - "{{ theme }}"
{% endfor %}
motifs:                                    # Recurring symbolic elements or imagery
{% for motif in motifs -%}
  - "{{ motif }}"
{% endfor %}

# Narrative Structure
pov_style: "{{ pov_style }}"               # Narrative perspective (e.g., Third Person Limited)
pov_characters:                            # Main POV characters and their roles
{% for character in pov_characters -%}
  - name: "{{ character.name }}"
    role: "{{ character.role }}"
{% endfor %}
narrative_arc: "{{ narrative_arc }}"       # Short description of story structure

# Word Count Goals
target_word_count: {{ target_word_count }}            # Total word count goal
target_chapters: {{ target_chapters }}                # Planned number of chapters
average_words_per_chapter: {{ average_words_per_chapter }} # Helps with pacing

# Project Management
created: {{ created }}                     # Project start date (YYYY-MM-DD)
last_updated: {{ last_updated }}           # Last metadata update date
milestones:                                # Key goals with target dates
{% for milestone in milestones -%}
  - name: "{{ milestone.name }}"
    target_date: {{ milestone.target_date }}
{% endfor %}

# Linked Projects
linked_projects:                          # Related works in the same universe
  sequels:                                # Direct continuations of this story
  {% for sequel in linked_projects.sequels -%}
    - title: "{{ sequel.title }}"
      status: "{{ sequel.status }}"       # planned | drafting | published
      release_date: {{ sequel.release_date }}
  {% endfor %}
  prequels:                               # Stories set before this one
  {% for prequel in linked_projects.prequels -%}
    - title: "{{ prequel.title }}"
      status: "{{ prequel.status }}"
      release_date: {{ prequel.release_date }}
  {% endfor %}
  spinoffs:                               # Side stories or related works
  {% for spinoff in linked_projects.spinoffs -%}
    - title: "{{ spinoff.title }}"
      status: "{{ spinoff.status }}"
      release_date: {{ spinoff.release_date }}
  {% endfor %}

# Notes
summary: >                                 # Short synopsis for quick reference
  {{ summary }}

---
# {{ project_name }}

{% block linked_projects %}{% endblock %}

## Linked Projects

| Relation | Project Name       | Path                          | Date Linked |
|----------|--------------------|-------------------------------|-------------|
| Sequel   | The Iron Rebellion | ../The_Iron_Rebellion         | 2025-09-01  |
| Prequel  | Clockmaker Origins | ../Clockmaker_Origins         | 2025-09-10  |
