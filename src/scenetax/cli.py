import argparse
import sys

# Import core command handlers
from .core import newproject, project, character, location, group, scene


def main():
	"""
	Main entry point for the scenetax CLI.
	Sets up argument parsing and dispatches to the appropriate command handler.
	"""
	# Root parser for the cli
	parser = argparse.ArgumentParser(
		prog="scenetax",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Scenetax: Project and worldbuilding management CLI",
		epilog="Use 'scenetax <command> --help' for more info on a subcommand."
	)

	# Version flag
	parser.add_argument(
		"-v", "--version",
		action="version",
		version="%(prog)s 0.0.1"
	)

	# Subparsers for main commands
	subparsers = parser.add_subparsers()

	#
	# newproject subcommand
	#
	newproject_parser = subparsers.add_parser(
		name="newproject",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Create a new project directory and scaffold.",
		epilog=""
	)

	newproject_parser.set_defaults(func = newproject, parser = newproject_parser)

	# positional arguments
	newproject_parser.add_argument(
		"projectname",
		type=str,
		nargs="+",
		help="Name of the new project."
	)

	#
	# project subcommand
	#
	project_parser = subparsers.add_parser(
		name="project",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Project-level actions and entity management.",
		epilog=""
	)

	project_parser.set_defaults(func = project, parser = project_parser)

	project_parser.add_argument(
		"-a", "--archive",
		action="store_true",
		help="Archive the project as a tar.gz file."
	)
	# project_parser.add_argument(
	# 	"-c", "--commit",
	# 	action="store_true",
	# 	help="Add all changes and commit with an automated message."
	# )

	# Subparsers for project subcommands (compile, character, location, group, scene)
	project_parser_subparsers = project_parser.add_subparsers()

	#
	# project compile subcommand
	#
	# project_compile_parser = project_parser_subparsers.add_parser(
	# 	name="compile",
	# 	formatter_class=argparse.RawDescriptionHelpFormatter,
	# 	description=""Compile the project into EPUB or PDF format."",
	# 	epilog=""
	# )

	# project_compile_parser.add_argument("volume", type=int, help="Choose which volume will be compiled", nargs="?", default=1)
	# project_compile_parser.add_argument("-e", "--epub", action="store_true", default=True, help="Compile the project as EPUB")
	# project_compile_parser.add_argument("-p", "--pdf", action="store_true", help="Compile the product as PDF")

	#
	# project character subcommand
	#
	project_character_parser = project_parser_subparsers.add_parser(
		name="character",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Create or edit character sheets.",
		epilog=""
	)

	project_character_parser.set_defaults(func = character, parser = project_character_parser)

	project_character_parser.add_argument(
		"-c", "--create",
		metavar="NAME",
		nargs="+",
		help="Create a new quick-capture character sheet."
	)
	project_character_parser.add_argument(
		"-v", "--version",
		metavar="FROM",
		nargs="?",
		type=int,
		const=-1,
		help="Create new version from an existing character sheet."
	)

	#
	# project location subcommand
	#
	project_location_parser = project_parser_subparsers.add_parser(
		name="location",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Create or edit location sheets.",
		epilog=""
	)

	project_location_parser.set_defaults(func = location, parser = project_location_parser)

	project_location_parser.add_argument(
		"-c", "--create",
		metavar="NAME",
		nargs="+",
		help="Create a new quick-capture location sheet."
	)
	project_location_parser.add_argument(
		"-v", "--version",
		metavar="FROM",
		nargs="?",
		type=int,
		const=-1,
		help="Create new version from an existing location sheet."
	)

	#
	# project group subcommand
	#
	project_group_parser = project_parser_subparsers.add_parser(
		name="group",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_group_parser.set_defaults(func = group, parser = project_group_parser)

	project_group_parser.add_argument(
		"-c", "--create",
		metavar="NAME",
		nargs="+",
		help="Create a new quick-capture group/faction/organization sheet."
	)
	project_group_parser.add_argument(
		"-v", "--version",
		metavar="FROM",
		nargs="?",
		type=int,
		const=-1,
		help="Create new version from an existing group/faction/organization sheet."
	)

	# 
	# project scene subcommand
	# 
	project_scene_parser = project_parser_subparsers.add_parser(
		name="scene",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Create scenes, chapters, or volumes.",
		epilog=""
	)

	project_scene_parser.set_defaults(func = scene, parser = project_scene_parser)
	scene_optional_group = project_scene_parser.add_mutually_exclusive_group(required=False)
	scene_optional_group.add_argument(
		"-c", "--chapter",
		action="store_true",
		help="Create a new chapter."
	)
	scene_optional_group.add_argument(
		"-v", "--volume",
		action="store_true",
		help="Create a new volume."
	)

	# Parse arguments from command-line
	args = parser.parse_args()
	# print(args)

	# If no arguments are provided, print help and exit
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)

	# Dispatch to the appropriate handler function
	try:
		args.func(args)
	except AttributeError:
		if args.parser:
			args.parser.print_help()
		sys.exit(1)


if __name__ == "__main__":
	main()
