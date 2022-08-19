from hashlib import new
from os import system, name
import requests

def clear():
   # Clear CLI screen 
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
    _ = system('clear')

def shrink_dict(original_dict, input_string):
   # TODO Complete function contract
   # Filter entries in dictionary based on initial string (starts with)

   shrunken_dict = {}
   print('Dictionary length = ', len(original_dict))
   for j in original_dict:
      if j[0:len(input_string)] == input_string:
         shrunken_dict[j] = original_dict[j]
   return shrunken_dict

def convert_dbrow_list(list):
   # TODO complete function contract
   # Converts datarow list to name array 
   new_list = []
   for item in list:
      new_list.append(item['name'])

   return new_list

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('------------END------------')

