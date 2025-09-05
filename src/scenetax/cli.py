import argparse
import sys

from core import newproject, project, create, write


def main():
	parser = argparse.ArgumentParser(
		prog="scenetax",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.1")

	subparsers = parser.add_subparsers()

	# Create a new project
	newproject_parser = subparsers.add_parser(
		name="newproject",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	newproject_parser.set_defaults(func = newproject, parser = newproject_parser)

	# positional arguments
	newproject_parser.add_argument("projectname", type=str)

	newproject_flags_group = newproject_parser.add_mutually_exclusive_group(required=False)

	# optional arguments
	newproject_flags_group.add_argument("-s", "--sequel")
	newproject_flags_group.add_argument("-p", "--prequel", metavar=("PREQUEL", "YEAR"), nargs=2)
	newproject_flags_group.add_argument("-o", "--spinoff", metavar=("SPINOFF", "YEAR"), nargs=2)

	# Commands to use inside an existing project
	project_parser = subparsers.add_parser(
		name="project",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_parser.set_defaults(func = project, parser = project_parser)

	project_parser.add_argument("-a", "--archive", action="store_true")
	project_parser.add_argument("-c", "--commit", action="store_true")
	project_parser.add_argument("-p", "--compile", action="store_true")

	project_parser_subparsers = project_parser.add_subparsers()

	project_create_parser = project_parser_subparsers.add_parser(
		name="create",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_create_parser.set_defaults(func = create, parser = project_create_parser)

	project_create_group = project_create_parser.add_mutually_exclusive_group(required=True)
	project_create_group.add_argument("-c", "--character", nargs="+")
	project_create_group.add_argument("-l", "--location", nargs="+")
	project_create_group.add_argument("-g", "--group", nargs="+")

	project_write_parser = project_parser_subparsers.add_parser(
		name="write",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog=""
	)

	project_write_parser.set_defaults(func = write, parser = project_write_parser)

	project_write_parser.add_argument("-s", "--scene", action="store_true", required=True)
	project_write_parser.add_argument("-n", "--newchapter", action="store_true", help="Create a new chapter")

	args = parser.parse_args()

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
