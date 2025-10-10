import argparse
import pathlib
import tarfile
import datetime
import yaml
import io
import uuid
from jinja2 import Environment, FileSystemLoader
from enum import Enum, auto


# Entity categories for project elements
class Category(Enum):
	CHARACTER = auto()
	LOCATION = auto()
	GROUP = auto()



def load_frontmatter(path: pathlib.Path):
	"""
	Extract YAML frontmatter and body from a Markdown file.
	Returns a tuple (frontmatter_dict, body_str).
	If no frontmatter is found, returns empty dict and full text as body.
	"""
	text = path.read_text(encoding="utf-8")
	if text.startswith("---"):
		_, fm_text, body = text.split("---", 2)
		frontmatter = yaml.safe_load(fm_text) or {}
		return frontmatter, body.lstrip()
	else:
		return {}, text



def save_frontmatter_to_file(path: pathlib.Path, frontmatter: dict, body: str):
	"""
	Write YAML frontmatter and body back to a Markdown file.
	Overwrites the file at 'path' with the new content.
	"""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	path.write_text(new_text, encoding="utf-8")



def save_frontmatter(frontmatter: dict, body: str):
	"""
	Return YAML frontmatter and body as a Markdown string.
	Useful for in-memory operations or archiving.
	"""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	return new_text



# Convert YAML template to Markdown fields (currently unused)
# def yaml_to_markdown(yaml_template):
# 	"""
# 	Convert a YAML template to Markdown fields.
# 	Currently unused; placeholder for future expansion.
# 	"""
# 	fields = yaml.safe_load(yaml_template) or {}



def create_scaffold(project_path: pathlib.Path):
	"""
	Create the directory scaffold for a new project.
	Sets up all required folders for worldbuilding, drafts, art, and publishing.
	"""
	project_name = project_path.name
	scaffold = [ # project structure
		project_path / "00_Reference" / f"00_LoreSeeds_{project_name}",
		project_path / "00_Reference" / "01_Research",
		project_path / "00_Reference" / "02_Inspiration",
		project_path / "10_Lore_and_Planning" / "01_Timeline_Maps",
		project_path / "10_Lore_and_Planning" / "02_Character_Dossiers",
		project_path / "10_Lore_and_Planning" / "03_Locations",
		project_path / "10_Lore_and_Planning" / "04_Groups_Factions_Organizations",
		project_path / "10_Lore_and_Planning" / "05_Mythos_and_Language",
		project_path / "20_Drafts" / "Volume_01" / "01_Chapters",
		project_path / "20_Drafts" / "Volume_01" / "02_Alt_Versions",
		project_path / "20_Drafts" / "Volume_01" / "03_Scraps",
		project_path / "30_Art_and_Design" / "01_Illustrations",
		project_path / "30_Art_and_Design" / "02_Maps",
		project_path / "30_Art_and_Design" / "03_Covers",
		project_path / "30_Art_and_Design" / "04_Mockups",
		project_path / "40_Review_and_Notes" / "01_Editor_Feedback",
		project_path / "40_Review_and_Notes" / "02_Self_Review",
		project_path / "50_Publishables" / "01_Ebook",
		project_path / "50_Publishables" / "01_Print",
		project_path / "50_Publishables" / "01_Promo",
		project_path / "99_Archive"
	]

	# Create each directory in the scaffold
	for dir in scaffold:
		dir.mkdir(parents=True, exist_ok=True)



def archive():
	"""
	Archive the current project directory as a tar.gz file.
	Excludes the archive and .git folders. Adds an 'archived_at' timestamp to scenetax.md.
	"""
	exclude_archive = [
		"99_Archive",
		".git"
	]

	now = datetime.datetime.now()

	cwd = pathlib.Path.cwd() # current directory
	project_name = cwd.name # name of the current directory
	archive_name = f"{now.strftime("%Y%m%d%H%M%S")}_{project_name}.tar.gz" # name of the archive

	items = cwd.glob("**/*") # list all items in the current directory
	with tarfile.open(cwd / "99_Archive" / archive_name, "w:gz") as tarf: # start archiving
		for item in items:
			relative_path = item.relative_to(cwd)

			# Skip excluded directories
			if relative_path.parts[0] in exclude_archive:
				continue

			# Special handling for scenetax.md: add archived_at timestamp
			if item.name == "scenetax.md":
				scenetax_frontmatter, scenetax_body = load_frontmatter(item)
				scenetax_frontmatter["archived_at"] = now.strftime("%d-%m-%Y %H:%M:%S.%f")
				new_text = save_frontmatter(scenetax_frontmatter, scenetax_body)
				data = new_text.encode(encoding="utf-8")
				tarinfo = tarfile.TarInfo(name=str(pathlib.Path(project_name) / item.relative_to(cwd)))
				tarinfo.size = len(data)
				tarf.addfile(tarinfo, io.BytesIO(data))
				continue

			# Add other files to archive
			tarf.add(item, arcname=pathlib.Path(project_name) / item.relative_to(cwd))



def newproject(args):
	"""
	Create a new project and initialize its structure and scenetax.md.
	Handles validation, directory creation, and initial metadata setup.
	"""
	root_path = pathlib.Path(".")

	name = " ".join(args.projectname).strip()

	# Validate project name
	if not name:
		args.parser.error("projectname cannot be empty")
    
	# Check if project already exists
	project_name = name.lower().replace(" ", "_")
	print(f"Creating project '{project_name}'...")
	project_path = root_path / project_name
	if project_path.exists() and project_path.is_dir():
		args.parser.error(f"'{project_name}' already exists.")
    
	create_scaffold(project_path)

	# Create initial frontmatter for the project
	frontmatter = {
		"id": str (uuid.uuid4()),
		"name": name
	}
	project_scenetax = project_path / "scenetax.md"
	save_frontmatter_to_file(project_scenetax, frontmatter, "")
	print(f"Project has been created at '{project_path}'")



def project(args):
	if args.archive:
		archive()



def create(parser: argparse.ArgumentParser, category: Category, name_parts: list[str],  from_version: int):
	"""
	Create a character, location, or group file with versioning.
	Handles entity creation, versioning, and template-based metadata population.
	"""
	# Determine the correct datasheet path based on category
	if category == Category.CHARACTER:
		print("Creating character...")
		datasheet_path = pathlib.Path("10_Lore_and_Planning/02_Character_Dossiers")
	elif category == Category.LOCATION:
		print("Creating location...")
		datasheet_path = pathlib.Path("10_Lore_and_Planning/03_Locations")
	elif category == Category.GROUP:
		print("Creating group...")
		datasheet_path = pathlib.Path("10_Lore_and_Planning/04_Groups_Factions_Organizations")
	else:
		parser.error("Illegal category.")

	# Build file name and check for existing versions
	name = " ".join(name_parts)
	file_name = "_".join([part.lower() for part in name_parts])

	# Find existing files with the same base name to determine version count
	files_starting_with_name = datasheet_path.glob(f"{file_name}*")

	version_count = 0

	for filename in files_starting_with_name:
		base_name = filename.stem
		parts = base_name.split("_")

		processed_name = "_".join(parts[: -1]) # processed meaning name lowered and spaces replaced with underscore
		if processed_name == file_name:
			version_count += 1
    
	# If no version specified, error if already exists
	if not from_version:
		if version_count > 0:
			parser.error(f"{name} already exists. use '-v' to create a new version.")
		else:
			from_version = -1
    
	if version_count > 0:
		print(f"Found {version_count} existing version(s)...")

	# Set version for new file
	if from_version == -1:
		from_version = version_count
	elif from_version < 1 or from_version > version_count:
		parser.error("Specified version does not exist.")

	version_count += 1
        
	name_version = f"{file_name}_v{version_count}"
	print(f"Creating new file: {name_version}.md...")

	filepath = datasheet_path / f"{name_version}.md"

	# Load project UUID from scenetax.md
	scenetax_frontmatter, _ = load_frontmatter(pathlib.Path.cwd() / "scenetax.md")
	scenetax_uuid = uuid.UUID(scenetax_frontmatter["id"])

	# Prepare frontmatter context for the new entity
	fm_context = {
		"id": str (uuid.uuid5(scenetax_uuid, name_version)),
		"name": name,
		"version": version_count,
		"created_at": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
	}

	# If first version, use template to generate frontmatter and datasheet
	if version_count == 1:
		program_root = pathlib.Path(__file__).parent.parent.parent

		env = Environment(
			loader=FileSystemLoader(program_root / "templates")
		)

		fm_template = env.get_template("entity_metadata.yaml")

		fm_content = fm_template.render(fm_context)

		frontmatter = yaml.safe_load(fm_content)

		character_yaml = yaml.safe_load((program_root / "templates" / f"{category.name.lower()}" / "quick_capture.yaml").read_text())

		datasheet = ""

		# Build datasheet from template fields
		for key in character_yaml:
			field = " ".join(key.split("_")).capitalize()
			datasheet += f"* **{field}:** _{character_yaml[key]["description"]} Example: {character_yaml[key]["example"]}_\n"
    
	else:
		# For new version, copy frontmatter and datasheet from referenced version
		referenced_version = datasheet_path / f"{file_name}_v{from_version}.md"
		frontmatter, datasheet = load_frontmatter(referenced_version)
		frontmatter["id"] = fm_context["id"]
		frontmatter["version"] = fm_context["version"]
		frontmatter["created_at"] = fm_context["created_at"]
		frontmatter["from_version"] = from_version

	# Save the new entity file
	save_frontmatter_to_file(filepath, frontmatter, datasheet)
	print(f"{category.name.capitalize()} has been created at: '{filepath}'")



# Handler for character creation command

# Handler for character creation command
def character(args):
	"""
	CLI handler for character creation.
	Calls the create() function with character category.
	"""
	if args.create:
		create(args.parser, Category.CHARACTER, args.create, args.version)


# Handler for location creation command

# Handler for location creation command
def location(args):
	"""
	CLI handler for location creation.
	Calls the create() function with location category.
	"""
	if args.create:
		create(args.parser, Category.LOCATION, args.create, args.version)


# Handler for group creation command

# Handler for group creation command
def group(args):
	"""
	CLI handler for group creation.
	Calls the create() function with group category.
	"""
	if args.create:
		create(args.parser, Category.GROUP, args.create, args.version)


# Handler for scene command (currently prints help)

# Handler for scene creation command
def scene(args):
	"""
	CLI handler for scene creation.
	Handles creation of new volumes, chapters, and scenes with metadata.
	"""
	program_root = pathlib.Path(__file__).parent.parent.parent
	env = Environment(
		loader=FileSystemLoader(program_root / "templates")
	)

	now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
	cwd = pathlib.Path.cwd()
    
	# Locate volumes and determine current volume
	volumes_path = pathlib.Path.cwd() / "20_Drafts"
	volumes = sorted([volume for volume in volumes_path.glob("Volume*")])
	current_volume = volumes[-1]

	# If --volume is specified, create a new volume and its folders
	if args.volume:
		print("Creating new volume...")
		current_volume = volumes_path / f"Volume_{len(volumes) + 1:02}"
		current_volume.mkdir()
		print(f"Successfully created directory '{current_volume.relative_to(cwd)}'")
		new_folders = [
			current_volume / "01_Chapters",
			current_volume / "02_Alt_Versions",
			current_volume / "03_Scraps"
		]
		for folder in new_folders:
			folder.mkdir()
			print(f"Successfully created directory '{folder.relative_to(cwd)}'")

	# Locate chapters and determine latest chapter
	chapter_path = current_volume / "01_Chapters"
	chapters = sorted([chapter for chapter in chapter_path.glob("chapter_*")])
    
	# If --chapter is specified or no chapters exist, create a new chapter
	if args.chapter or len(chapters) == 0:
		print("Creating new chapter...")
		latest_chapter = chapter_path / f"chapter_{len(chapters) + 1:02}"
		latest_chapter.mkdir()

		chapter_metadata_path = latest_chapter / f"chapter_{len(chapters) + 1:02}.yaml"
		chapter_metadata_template = env.get_template("chapter/chapter_metadata.yaml")

		chapter_context = {
			"chapter_number": len(chapters) + 1,
			"created_at": now
		}

		chapter_metadata = chapter_metadata_template.render(chapter_context)
		chapter_metadata_path.write_text(chapter_metadata)

		print(f"Successfully created directory '{latest_chapter.relative_to(cwd)}'")
	else:
		latest_chapter = chapters[-1]

	# Create new scene in the latest chapter
	print("Creating new scene...")
	scenes = [scene for scene in latest_chapter.glob("scene_*")]
	new_scene = latest_chapter / f"scene_{len(scenes) + 1:02}.md"

	scene_metadata_template = env.get_template("chapter/scene_metadata.yaml")

	scene_context = {
		"scene_number_in_chapter": len(scenes) + 1,
		"created_at": now
	}
	scene_metadata_rendered = scene_metadata_template.render(scene_context)

	scene_frontmatter = yaml.safe_load(scene_metadata_rendered)

	save_frontmatter_to_file(new_scene, scene_frontmatter, "")

	print(f"Successfully created scene: '{new_scene.relative_to(cwd)}'")
