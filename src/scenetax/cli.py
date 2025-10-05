import argparse
import sys

from .core import newproject, project, character, location, group, scene


def main():
	#
	# root parser
	# scenetax
	#
	parser = argparse.ArgumentParser(
		prog="scenetax",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.1")

	subparsers = parser.add_subparsers()

	#
	# newproject parser
	# scenetax newproject
	#
	newproject_parser = subparsers.add_parser(
		name="newproject",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	newproject_parser.set_defaults(func = newproject, parser = newproject_parser)

	# positional arguments
	newproject_parser.add_argument("projectname", type=str, nargs="+")

	#
	# project parser
	# scenetax project
	#
	project_parser = subparsers.add_parser(
		name="project",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_parser.set_defaults(func = project, parser = project_parser)

	project_parser.add_argument("-a", "--archive", action="store_true", help="Archive the project")
	project_parser.add_argument("-c", "--commit", action="store_true", help="Add all changes and commit")

	project_parser_subparsers = project_parser.add_subparsers()

	#
	# project compile parser
	# scenetax project compile
	#
	project_compile_parser = project_parser_subparsers.add_parser(
		name="compile",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_compile_parser.add_argument("volume", type=int, help="Choose which volume will be compiled", nargs="?", default=1)
	project_compile_parser.add_argument("-e", "--epub", action="store_true", default=True, help="Compile the project as EPUB")
	project_compile_parser.add_argument("-p", "--pdf", action="store_true", help="Compile the product as PDF")

	#
	# project character parser
	# scenetax project character
	#
	project_character_parser = project_parser_subparsers.add_parser(
		name="character",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_character_parser.set_defaults(func = character, parser = project_character_parser)

	project_character_parser.add_argument("-c", "--create", metavar="NAME", nargs="+", help="Create a new quick-capture character sheet.")
	project_character_parser.add_argument("-v", "--version", metavar="FROM", nargs="?", type=int, const=-1, help="Create new version from an existing character sheet.")

	project_character_parser_subparsers = project_character_parser.add_subparsers()
	character_edit_parser = project_character_parser_subparsers.add_parser(
		name="edit",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Edit an existing character sheet",
		epilog=""
	)

	character_edit_parser.set_defaults(func = character, parser = character_edit_parser)

	character_edit_parser.add_argument("name", help="Name of the character")
	
	character_edit_group = character_edit_parser.add_mutually_exclusive_group(required=True)
	character_edit_group.add_argument("-u", "--upgrade", action="store_true", help="Upgrade an existing quick-capture character sheet to a complete character sheet.")
	character_edit_group.add_argument("-i", "--identity", action="store_true", help="Edit identity section.")
	character_edit_group.add_argument("-a", "--appearance", action="store_true", help="Edit appearance section.")
	character_edit_group.add_argument("-p", "--personality", action="store_true", help="Edit personality and psychology section.")
	character_edit_group.add_argument("-l", "--lore", action="store_true", help="Edit backstory and history section.")
	character_edit_group.add_argument("-b", "--beliefs", action="store_true", help="Edit beliefs and interests section.")
	character_edit_group.add_argument("-r", "--role", action="store_true", help="Edit role section.")

	#
	# project location parser
	# scenetax project location
	#
	project_location_parser = project_parser_subparsers.add_parser(
		name="location",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_location_parser.set_defaults(func = location, parser = project_location_parser)

	project_location_parser.add_argument("-c", "--create", metavar="NAME", nargs="+", help="Create a new quick-capture location sheet.")
	project_location_parser.add_argument("-v", "--version", action="store_true", help="Create new version from an existing location sheet.")

	#
	# project group parser
	# scenetax project group
	#
	project_group_parser = project_parser_subparsers.add_parser(
		name="group",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_group_parser.set_defaults(func = group, parser = project_group_parser)

	project_group_parser.add_argument("-c", "--create", metavar="NAME", nargs="+", help="Create a new quick-capture group/faction/organization sheet.")
	project_group_parser.add_argument("-v", "--version", action="store_true", help="Create new version from an existing group/faction/organization character sheet.")

	# 
	# project scene parser
	# scenetax project scene
	# 
	project_scene_parser = project_parser_subparsers.add_parser(
		name="scene",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_scene_parser.set_defaults(func = scene, parser = project_scene_parser)
	scene_optional_group = project_scene_parser.add_mutually_exclusive_group(required=False)
	scene_optional_group.add_argument("-c", "--newchapter", action="store_true", help="Create a new chapter")
	scene_optional_group.add_argument("-v", "--volume", action="store_true", help="Create a new volume")

	args = parser.parse_args()
	print(args)

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)

	try:
		print(args.func.__name__)
		args.func(args)
	except AttributeError:
		if args.parser:
			args.parser.print_help()
		sys.exit(1)


if __name__ == "__main__":
	main()
