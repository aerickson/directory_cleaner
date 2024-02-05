#!/usr/bin/env python3

import argparse
import configparser

import directory_cleaner.directory_cleaner as DC

def parse_config_file(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Parse config file in INI format.')

    # Add command line argument for config file path
    parser.add_argument('--config', '-c', dest='config_file', type=str, required=True,
                        help='Path to the config file in INI format.')

    # Parse command line arguments
    args = parser.parse_args()

    # Parse the config file
    config_path = args.config_file
    config = parse_config_file(config_path)

    # Print the parsed config
    for section in config.sections():
        print(f'Section: {section}')
        for key, value in config.items(section):
            print(f'  {key} = {value}')

if __name__ == '__main__':
    main()
