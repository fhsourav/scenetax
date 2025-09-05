import argparse
import pathlib


def create_scaffold(project_path: pathlib.Path):
	scaffold = [
		project_path / "00_Reference" / "00_LoreSeeds",
		project_path / "00_Reference" / "01_Research",
		project_path / "00_Reference" / "02_Inspiration",
		project_path / "10_Lore_and_Planning" / "01_Timeline_Maps",
		project_path / "10_Lore_and_Planning" / "02_Character_Dossiers",
		project_path / "10_Lore_and_Planning" / "03_Locations",
		project_path / "10_Lore_and_Planning" / "04_Groups_Factions_Organizations",
		project_path / "10_Lore_and_Planning" / "05_Mythos_and_Language",
		project_path / "20_Drafts" / "01_Chapters",
		project_path / "20_Drafts" / "02_Alt_Versions",
		project_path / "20_Drafts" / "03_Scraps",
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

	project_scenetax = project_path / ".scenetax.md"
	project_scenetax.touch()


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
	
	# check if prequel or spinoff flags are enabled and the values are correctly provided
	if args.sequel or args.prequel or args.spinoff:
		empty_project = False

		old_project = args.sequel if args.sequel else args.prequel[0] if args.prequel else args.spinoff[0] if args.spinoff else ""
		if not old_project.strip():
			args.parser.error("[SEQUEL | PREQUEL | SPINOFF] cannot be empty")
	
		old_project = old_project.strip().lower().replace(" ", "_")
		old_project_path = root_path / old_project
		if not (old_project_path.exists() or old_project_path.is_dir()):
			args.parser.error(f"'{old_project}' not found")
		
		if args.prequel or args.spinoff:
			year = args.prequel[1] if args.prequel else args.spinoff[1]
			if not year.isnumeric():
				args.parser.error("YEAR must be an integer")
	
	create_scaffold(project_path)


def project(args):
	args.parser.print_help()


def create(args):
	args.parser.print_help()


def write(args):
	args.parser.print_help()
