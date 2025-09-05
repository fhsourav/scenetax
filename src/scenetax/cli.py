import argparse


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
		description="",
		epilog=""
	)

	# positional arguments
	newproject_parser.add_argument("projectname")

	newproject_flags_group = newproject_parser.add_mutually_exclusive_group(required=False)

	# optional arguments
	bleh = newproject_flags_group.add_argument("-s", "--sequel")

	newproject_flags_group.add_argument("-p", "--prequel", metavar=("PREQUEL", "YEAR"), nargs=2)
	newproject_flags_group.add_argument("-o", "--spinoff", metavar=("SPINOFF", "YEAR"), nargs=2)

	# Commands to use inside an existing project
	project_parser = subparsers.add_parser(
		name="project"
	)

	project_parser.add_argument("-a", "--archive", action="store_true")
	project_parser.add_argument("-c", "--commit", action="store_true")
	project_parser.add_argument("-p", "--compile", action="store_true")

	project_parser_subparsers = project_parser.add_subparsers()

	project_create_parser = project_parser_subparsers.add_parser(
		name="create",
		description="",
		epilog=""
	)

	project_create_group = project_create_parser.add_mutually_exclusive_group(required=True)
	project_create_group.add_argument("-c", "--character", nargs="+")
	project_create_group.add_argument("-l", "--location", nargs="+")
	project_create_group.add_argument("-g", "--group", nargs="+")

	project_write_parser = project_parser_subparsers.add_parser(
		name="write",
		description="",
		epilog=""
	)

	project_write_parser.add_argument("-s", "--scene", action="store_true", required=True)
	project_write_parser.add_argument("-n", "--newchapter", action="store_true", help="Create a new chapter")

	args = parser.parse_args()

	print(args)


if __name__ == "__main__":
	main()
