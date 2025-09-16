import datetime

from jinja2 import Environment, FileSystemLoader

env = Environment(
	loader=FileSystemLoader("templates")
)

template = env.get_template("scenetax.md")

now = datetime.datetime.now()

context = {
    "title": "The Shattered Crown",
    "series": "Legends of Aelthar",
    "series_number": 1,
    "author": "Fahim",
    "status": "outline",
    "version": "0.1.0",
    "genre": "High Fantasy",
    "subgenres": ["Epic", "Political Intrigue", "Mythic"],
    "tone_keywords": ["Dark", "Hopeful", "Sweeping", "Character-driven"],
    "primary_world": "Aelthar",
    "primary_region": "The Verdant Expanse",
    "time_period": "Age of Fractured Thrones",
    "magic_system": "Leyline Convergence",
    "technology_level": "Late Medieval",
    "themes": ["Power and Corruption", "Legacy and Memory", "Sacrifice for the Greater Good"],
    "motifs": ["Shattered artifacts", "Blood-red moons", "Songs of the lost"],
    "pov_style": "Third Person Limited",
    "pov_characters": [
        {"name": "Kaelen Duskbane", "role": "Exiled Prince"},
        {"name": "Serenya Veyra", "role": "Warden of the Leylines"}
    ],
    "narrative_arc": "Hero’s Journey with Political Subplot",
    "target_word_count": 120000,
    "target_chapters": 40,
    "average_words_per_chapter": 3000,
    "created": now.date(),
    "last_updated": now.date(),
    "milestones": [
        {"name": "Worldbuilding Complete", "target_date": "2025-10-01"},
        {"name": "First Draft Complete", "target_date": "2026-03-15"}
    ],
    "linked_projects": {
        "sequels": [
            {"title": "The Iron Thronefall", "status": "planned", "release_date": "2027-05-01"}
        ],
        "prequels": [
            {"title": "The Dawn of Aelthar", "status": "published", "release_date": "2023-08-15"}
        ],
        "spinoffs": []
    },
    "folders": {
        "worldbuilding": "world/",
        "characters": "characters/",
        "locations": "locations/",
        "chapters": "chapters/",
        "appendices": "appendices/",
        "research": "research/"
    },
    "summary": (
        "In the wake of a shattered crown, rival heirs and ancient powers vie for control of Aelthar. "
        "Amidst political intrigue and forgotten magic, unlikely allies must unite before the leyline storms consume the realm."
    )
}

content = template.render(context)

print(content)
