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
	newproject_parser.add_argument("projectname", type=str)

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

	project_character_parser.add_argument("-c", "--create", )

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

	project_character_parser.set_defaults(func = location, parser = project_location_parser)

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

	project_character_parser.set_defaults(func = group, parser = project_group_parser)

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
		args.func(args)
	except AttributeError:
		if args.parser:
			args.parser.print_help()
		sys.exit(1)


if __name__ == "__main__":
	main()
