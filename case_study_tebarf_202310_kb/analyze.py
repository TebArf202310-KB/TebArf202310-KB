from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from pprint import pprint
from . import utilities

class ZeroShotClassification:
    """
    This class provides functionalities for zero-shot classification
    using Hugging Face library.
    """

    def __init__(self, config_file_path=r"..\config\config.ini"):
        """
        Initialization of the classifier.

        Parameters:
        - task: The classification task. Default is "zero-shot-classification".
        - model_path: Path to the pre-trained model.
        """

        try:
            # Reading config data
            print("Reading config")
            config_data = utilities.read_config_file(config_file_path=config_file_path)
            default_task = config_data["model"]["default_task"]
            default_model = config_data["model"]["default_model"]
            default_model_path = config_data["model"]["default_model_path"]
        except FileNotFoundError:
            print(f"Error: Config file not found at path '{config_file_path}' Please enter a valid config file path via config_file_path parameter")
        except KeyError as e:
            print(f"Error: Key '{e}' not found in the config file. Please check the config file structure.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

        print("Initializing pipeline and loading models")
        if not self.check_model_existence(default_model_path):
            download_choice = input(f"The specified model {default_model} does not exist. Do you want to download (facebook/bart-large-mnli)? (Yes/No): ").strip().lower()
            if (download_choice == "yes") or (download_choice == "y"):
                self.download_model(model_name = default_model, save_directory=default_model_path)
            else:
                print("Exiting... No model present")
                return None

        try:
            self.classifier = pipeline(task=default_task, model=default_model_path)
            print("Done")
        except Exception as e:
            print(f"Error initializing model: {e}")

    def check_model_existence(self, model_path):
        """
        Check if model exists at the given path.

        Parameters:
        - model_path: Path to the pre-trained model.

        Returns:
        Boolean indicating if the model exists.
        """
        import os
        return os.path.exists(model_path)

    def download_model(self, model_name, save_directory):
        """
        Download the model from Hugging Face's model hub.

        Parameters:
        - model_name: Name of the model on the Hugging Face's model hub.
        - save_directory: Directory to save the downloaded model.
        """
        print(f"Downloading {model_name}...")

        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        model.save_pretrained(save_directory)
        tokenizer.save_pretrained(save_directory)
        print("Model downloaded and saved!")

    def classify(self, text, labels):
        """
        Classify the given text for the provided labels.

        Parameters:
        - text: The text to be classified.
        - labels: The possible labels.

        Returns:
        Tuple containing raw result and the most probable label.
        """
        try:
            result = self.classifier(text, labels)
            return result, result['labels'][0]
        except Exception as e:
            print(f"Error classifying text: {e}")
            return None, None

    def analyze_all_conversation(self, file_path=r"..\data\simulated_conversations\prompt1_conversation1.json"):
        """
        Analyze the entire conversation from the given file and predict
        sentiment/intent.

        Parameters:
        - file_path: Path to the JSON file containing the conversation.

        Returns:
        None
        """
        json_data = utilities.read_json_file(file_path)
        if not json_data:
            print("Failed to read JSON data.")
            return

        # Extract unique labels for intent and sentiment
        labels_dictionary = utilities.get_unique_intent_and_sentiment_from_conversation(json_data)

        for step in json_data["conversation"]:
            print("-----------")
            step_number = step.get("step")
            role = step.get("role")
            message = step.get("message")
            sentiment = step.get("sentiment")
            intent = step.get("intent")

            _, predicted_intent_label = self.classify(message, labels_dictionary["intent_labels"])
            _, predicted_sentiment_label = self.classify(message, labels_dictionary["sentiment_labels"])

            pprint(step)
            print(f"Predicted intent: {predicted_intent_label}")
            print(f"Predicted sentiment: {predicted_sentiment_label}")

        return None
