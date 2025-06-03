import sys
from cheat.defenses.cheat import CHeaT
from cheat.utils.argument_parser import parse_arguments
from cheat.utils.logger import setup_logger


def main():
    # Setup logger
    logger = setup_logger()

    # Parse command-line arguments
    args = parse_arguments(sys.argv[1:])
    logger.info(f"Arguments received: {args}")

    # Initialize Defense Manager
    cheat = CHeaT(args['database'], logger)

    try:
        if args['action'] == 'plant':
            if not args['details']:
                logger.error("--details must be provided for the 'plant' action.")
                sys.exit(1)

            # Parse details into a dictionary (assuming it's passed as JSON-like string)
            import json
            details = json.loads(args['details'])

            cheat.plant_defense(details['assettype'], details['file_path'], details['technique'], 
                                   method=details.get('method', 'prompt_injection'), 
                                   template=details.get('template', 'Combined_Attack'))

        elif args['action'] == 'list':
            list_type = args.get('type', None)
            if list_type == 'available':
                cheat.print_available_defenses()
            elif list_type == 'installed':
                cheat.print_installed_defenses()
            else:
                logger.error("Invalid list type. Use --type 'available' or 'installed'.")
                sys.exit(1)

        elif args['action'] == 'remove':
            if not args['id']:
                logger.error("Defense ID (--id) must be provided for the 'remove' action.")
                sys.exit(1)
            cheat.remove_defense(args['id'])

        elif args['action'] == 'remove_all':
            cheat.remove_all_defenses()

        else:
            logger.error("Invalid action provided. Use 'plant', 'list', 'remove', or 'remove_all'.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
