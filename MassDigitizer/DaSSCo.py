import logging

# Internal dependencies
import home_screen
import util

def main() -> None:

    util.buildLogger()
    logging.info("* Mass Digitizer for DaSSCo *")

    try:
        home = home_screen.HomeScreen()    
    except Exception as e:
        logging.debug(str(e))

    # TODO start background processes? 

if __name__ == "__main__":
    main()