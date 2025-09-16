import argparse
import pathlib
import tarfile
import datetime
import yaml
import io


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
	"""Write YAML frontmatter + body back to file."""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	path.write_text(new_text, encoding="utf-8")


def save_frontmatter(frontmatter: dict, body: str):
	"""Write YAML frontmatter + body in a single string."""
	fm_text = yaml.safe_dump(frontmatter, sort_keys=False).strip()
	new_text = f"---\n{fm_text}\n---\n\n{body}"
	return new_text


def create_scaffold(project_path: pathlib.Path):
	"""Create the project scaffold."""
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

	for dir in scaffold:
		dir.mkdir(parents=True, exist_ok=True)

	project_scenetax = project_path / "scenetax.md"
	project_scenetax.touch()


def archive():
	"""Archive the project directory."""
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

			if relative_path.parts[0] in exclude_archive:
				continue # exclude archives

			if item.name == "scenetax.md": # add archived_at frontmatter in scenetax.md
				scenetax_frontmatter, scenetax_body = load_frontmatter(item)
				scenetax_frontmatter["archived_at"] = now.strftime("%d-%m-%Y %H:%M:%S.%f")
				new_text = save_frontmatter(scenetax_frontmatter, scenetax_body)
				data = new_text.encode(encoding="utf-8")
				tarinfo = tarfile.TarInfo(name=str(pathlib.Path(project_name) / item.relative_to(cwd)))
				tarinfo.size = len(data)
				tarf.addfile(tarinfo, io.BytesIO(data))
				continue

			tarf.add(item, arcname=pathlib.Path(project_name) / item.relative_to(cwd)) # add rest of the items to archive


def newproject(args):
	"""
	Create a new project.
	"""
	empty_project = True
	root_path = pathlib.Path(".")

	# check if projectname is empty
	if not args.projectname.strip():
		args.parser.error("projectname cannot be empty")
	
	# check if project already exists
	project_name = args.projectname.strip().lower().replace(" ", "_")
	project_path = root_path / project_name
	if project_path.exists() and project_path.is_dir():
		args.parser.error(f"'{project_name}' already exists.")
	
	create_scaffold(project_path)


def project(args):
	if args.archive:
		archive()
	args.parser.print_help()


def character(args):
	args.parser.print_help()


def location(args):
	args.parser.print_help()


def group(args):
	args.parser.print_help()


def scene(args):
	args.parser.print_help()
