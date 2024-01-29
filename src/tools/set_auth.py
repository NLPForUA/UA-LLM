import argparse
import logging
import os

OPENAI_ORG_ID = "<OPENAI_ORG_ID>"
OPENAI_API_KEY = "<OPENAI_API_KEY>"
COHERE_API_KEY = "<COHERE_API_KEY>"
REPLICATE_API_KEY = "<REPLICATE_API_KEY>"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def replace_in_file(file_path, search_str, replace_str):
    with open(file_path, "r") as f:
        file_content = f.read()
    updated_file_content = file_content.replace(search_str, replace_str)
    if file_content == updated_file_content:
        return 0
    with open(file_path, "w") as f:
        f.write(updated_file_content)
    return 1


def search_and_replace(root_dir, search_str, replace_str):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".yaml"):
                continue
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                if replace_in_file(file_path, search_str, replace_str):
                    logger.info(
                        f"Replaced {search_str} with {replace_str} in {file_path}"
                    )


def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai_org_id", type=str, help="OpenAI organization ID")
    parser.add_argument("--openai_api_key", type=str, help="OpenAI API key")
    parser.add_argument("--cohere_api_key", type=str, help="Cohere API key")
    parser.add_argument("--replicate_api_key", type=str, help="Replicate API key")
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    parser = parser.parse_args()

    root_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "configs")
    )

    if parser.openai_org_id is not None or parser.openai_api_key is not None:
        if parser.openai_org_id is None or parser.openai_api_key is None:
            logger.error("You must provide both --openai_org_id and --openai_api_key")
        else:
            search_and_replace(root_dir, OPENAI_ORG_ID, parser.openai_org_id)
            search_and_replace(root_dir, OPENAI_API_KEY, parser.openai_api_key)
    if parser.cohere_api_key is not None:
        search_and_replace(root_dir, COHERE_API_KEY, parser.cohere_api_key)
    if parser.replicate_api_key is not None:
        search_and_replace(root_dir, REPLICATE_API_KEY, parser.replicate_api_key)
