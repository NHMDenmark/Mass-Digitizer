import traceback
import PySimpleGUI as sg

# Internal dependencies
import home_screen
import util

def main() -> None:
    """
    Main entry point for app. Sets up logging and starts home screen window. 
    """
    
    util.buildLogger()
    util.logger.info("* Mass Digitizer for DaSSCo *")

    try:
        home = home_screen.HomeScreen()    
    except Exception as e:
        util.logger.error(str(e))
        traceBack = traceback.format_exc()
        util.logger.error(traceBack)
        sg.popup_error(f'{e} \n\n {traceBack}', title='Error',  )   

    # TODO start background processes? 

if __name__ == "__main__":
    main()