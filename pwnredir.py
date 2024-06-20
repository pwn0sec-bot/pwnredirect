#!/usr/bin/env python3
import os
import requests
import signal
from optparse import OptionParser
from colorama import Fore, Style

def banner():
    print(Style.BRIGHT + Fore.YELLOW + """
██████  ██     ██ ███    ██ ██████  ███████ ██████  ██ ██████  ███████  ██████ ████████ 
██   ██ ██     ██ ████   ██ ██   ██ ██      ██   ██ ██ ██   ██ ██      ██         ██    
██████  ██  █  ██ ██ ██  ██ ██████  █████   ██   ██ ██ ██████  █████   ██         ██    
██      ██ ███ ██ ██  ██ ██ ██   ██ ██      ██   ██ ██ ██   ██ ██      ██         ██    
██       ███ ███  ██   ████ ██   ██ ███████ ██████  ██ ██   ██ ███████  ██████    ██  
       [ version 0.1 ]       [ Pwn0sec (pwn0sec.researcher@gmail.com) ]
                                           [ twitter.com/pwn0sec ]
        """ + Style.RESET_ALL)

def main():
    os.system('clear')
    banner()
    usage = "Usage: python %prog [-h] -u 'URL' -f [file]"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="target URL")
    parser.add_option("-f", "--file", dest="file", help="payloads file")

    (options, args) = parser.parse_args()
    if options.url is None or options.file is None:
        parser.print_help()
        exit(1)

    # Open file
    with open(options.file, 'r') as f:
        for payload in f:
            payloadF = payload.strip()
            urlF = options.url + payloadF
            print(urlF)

            # Get the response(200,400,404).
            try:
                response = requests.get(urlF, verify=True)

                # Process to find an open redirect.
                if response.history:
                    # Compare the destination url with Bing's url.
                    if response.url.startswith('http://www.bing.com') or response.url.startswith('https://www.bing.com'):
                        print(Style.BRIGHT + Fore.YELLOW + "Open Redirect Vulnerability found!" + Style.RESET_ALL)
                        print(Fore.YELLOW + f"Redirected to: {response.status_code} {response.url}" + Style.RESET_ALL)
                        print(Style.BRIGHT + Fore.BLUE + f"Payload ---> {payloadF}" + Style.RESET_ALL + "\n")
                        exit()
                    else:
                        print(Fore.YELLOW + f"Redirected to: {response.status_code} {response.url}" + Style.RESET_ALL + "\n")
                else:
                    print("Request was not redirected\n")

            except requests.exceptions.RequestException as e:
                print(f"Error accessing {urlF}: {e}")

# Press ctrl+c to finish
def ctrl_c(signum, frame):
    print("\nSee you soon!\n")
    exit()

signal.signal(signal.SIGINT, ctrl_c)

try:
    main()
    print(Fore.YELLOW + "RESULT: " + Style.RESET_ALL + "No Open Redirect Found!")
except TypeError:
    print("Usage: python ordetector.py -u 'URL' -f [file]\n")
