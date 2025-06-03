import argparse


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(description="Defense Planting Application")
    parser.add_argument("--action", type=str, required=True, 
                        help="Action to perform: plant, list, remove, remove_all")
    parser.add_argument("--type", type=str, 
                        help="Type to 'list': 'available', 'installed'")
    parser.add_argument("--details", type=str, 
                        help="Details of the defense to plant, provided as a JSON-like string")
    parser.add_argument("--id", type=str, 
                        help="ID of the defense to remove (required for 'remove')")
    parser.add_argument("--database", type=str, default="database", 
                        help="Path to defense database directory (default is 'database')")

    return vars(parser.parse_args(arguments))
