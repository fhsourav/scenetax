# Standard library imports
import argparse  # For command-line argument parsing
import pathlib   # For filesystem path operations
import tarfile   # For creating tar.gz archives
import datetime  # For timestamps
import yaml      # For YAML frontmatter handling
import io        # For in-memory file operations
import uuid      # For unique IDs
from jinja2 import Environment, FileSystemLoader  # For templating
from enum import Enum, auto  # For entity categories
import re        # For regex operations


# Enum for entity categories
class Category(Enum):
	CHARACTER = auto()
	LOCATION = auto()
	GROUP = auto()


def load_frontmatter(path: pathlib.Path):
	"""Extract YAML frontmatter and body from a Markdown file."""
	text = path.read_text(encoding="utf-8")
	if text.startswith("---"):
		_, fm_text, body = text.split("---", 2)
		frontmatter = yaml.safe_load(fm_text) or {}
		return frontmatter, body.lstrip()
	else:
		return {}, text


def save_frontmatter_to_file(path: pathlib.Path, frontmatter: dict, body: str):
	"""Write YAML frontmatter and body back to a Markdown file"""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	path.write_text(new_text, encoding="utf-8")


def save_frontmatter(frontmatter: dict, body: str):
	"""Return YAML frontmatter and body as a Markdown string"""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	return new_text


# Convert YAML template to Markdown fields (currently unused)
def yaml_to_markdown(yaml_template):
	fields = yaml.safe_load(yaml_template) or {}


def create_scaffold(project_path: pathlib.Path):
	"""Create the directory scaffold for a new project."""
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
		project_path / "20_Drafts" / "01_Volume_01" / "01_Chapters",
		project_path / "20_Drafts" / "01_Volume_01" / "02_Alt_Versions",
		project_path / "20_Drafts" / "01_Volume_01" / "03_Scraps",
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
	"""Archive the current project directory as a tar.gz file."""
	exclude_archive = [
		"99_Archive",
		".git"
	]

	now = datetime.datetime.now()

	cwd = pathlib.Path.cwd() # current directory
	project_name = cwd.name # name of the current directory
	archive_name = f"{now.strftime("%Y%m%d%H%M%S")}_{project_name}.tar.gz" # name of the archive

	items = cwd.glob("**/*") # list all items in the current directory
	with tarfile.open(archive_name, "w:gz") as tarf: # start archiving
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
	"""
	root_path = pathlib.Path(".")

	name = " ".join(args.projectname).strip()

	# Validate project name
	if not name:
		args.parser.error("projectname cannot be empty")
    
	# Check if project already exists
	project_name = name.lower().replace(" ", "_")
	print(project_name)
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



# Handle project-level commands (archive, etc.)
def project(args):
	if args.archive:
		archive()



# Create a character, location, or group file with versioning
def create(parser: argparse.ArgumentParser, category: Category, name_parts: list[str],  from_version: int):
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
	files_starting_with_name = datasheet_path.rglob(f"{file_name}*")

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
		project_root = pathlib.Path(__file__).parent.parent.parent

		env = Environment(
			loader=FileSystemLoader(project_root / "templates")
		)

		fm_template = env.get_template(f"{category.name.lower()}/frontmatter.yaml")

		fm_content = fm_template.render(fm_context)

		frontmatter = yaml.safe_load(fm_content)

		character_yaml = yaml.safe_load((project_root / "templates" / f"{category.name.lower()}" / "quick_capture.yaml").read_text())

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
	
	print(frontmatter)

	# Save the new entity file
	save_frontmatter_to_file(filepath, frontmatter, datasheet)
	print(f"{category.name.capitalize()} has been created.")



# Handler for character creation command
def character(args):
	if args.create:
		create(args.parser, Category.CHARACTER, args.create, args.version)


# Handler for location creation command
def location(args):
	if args.create:
		create(args.parser, Category.LOCATION, args.create, args.version)


# Handler for group creation command
def group(args):
	if args.create:
		create(args.parser, Category.GROUP, args.create, args.version)


# Handler for scene command (currently prints help)
def scene(args):
	args.parser.print_help()
