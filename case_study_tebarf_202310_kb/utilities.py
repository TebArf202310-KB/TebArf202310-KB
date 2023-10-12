import json
import pandas as pd
import configparser
from pprint import pprint

def read_json_file(file_path):
    """
    Read and parse a JSON file.

    Parameters:
    - file_path: Path to the JSON file.

    Returns:
    Parsed JSON data or None in case of errors.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def get_unique_intent_and_sentiment_from_conversation(json_data):
    """
    Extract unique intent and sentiment labels from conversation.

    Parameters:
    - json_data: Parsed JSON data.

    Returns:
    Dictionary containing unique intent and sentiment labels.
    """
    conversation = json_data.get("conversation")

    intent_list = list(pd.DataFrame(conversation)["intent"].unique())
    sentiment_list = list(pd.DataFrame(conversation)["sentiment"].unique())

    return {"intent_labels":intent_list, "sentiment_labels":sentiment_list}

def read_config_file(config_file_path=r"..\config\config.ini",verbose = True):
    """
    Read configuration file and extract configurations.

    Parameters:
    - config_file_path: Path to the config file.

    Returns:
    Dictionary containing the configuration values or None in case of errors.
    """
    try:
        config = configparser.ConfigParser()
        config.read(config_file_path)

        config_data = {}
        for section in config.sections():
            config_data[section] = {}
            for option in config.options(section):
                config_data[section][option] = config.get(section, option)

        if verbose:
            pprint(config_data)
        return config_data
    except configparser.Error as e:
        print(f"Error reading configuration file: {e}")
        return None
