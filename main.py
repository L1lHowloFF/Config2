#!/usr/bin/env python3
import sys
import os
from config import Config, ConfigError


def print_config_as_key_value(config: Config) -> None:
    config_dict = config.to_dict()
    print("Configuration parameters (key-value format):")
    print("-" * 40)
    for key, value in config_dict.items():
        print(f"{key}: {value}")
    print("-" * 40)


def main():
    config_file = "config.json"
    
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        print("Please create a config.json file with the required parameters.")
        sys.exit(1)

    try:
        config = Config.load_from_file(config_file)
        
        # Валидация
        config.validate()
        
        print_config_as_key_value(config)
        
        print("Configuration loaded successfully!")
        print("Application is ready for the next stages")
        
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()