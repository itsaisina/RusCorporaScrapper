"""
Main script to start the web scraping process.
"""

import json
from facade_api import FacadeAPI


def main():
    """
    Main function to initiate the web scraping process for words listed in 'biverbal_verbs.txt'.
    Scraped data for each word will be saved in separate JSON files.
    """
    scraper = None
    try:
        scraper = FacadeAPI(config_path='scrapper_config.json')

        with open('biverbal_verbs.txt', 'r', encoding='utf-8') as file:
            words = [word.strip() for word in file.readlines()]

        for word in words:
            print(f"Processing word: {word}")
            perfective_data, imperfective_data = scraper.process_word(word)

            with open(f'perfective_{word}.json', 'w', encoding='utf-8') as f:
                json.dump(perfective_data, f, ensure_ascii=False, indent=4)

            with open(f'imperfective_{word}.json', 'w', encoding='utf-8') as f:
                json.dump(imperfective_data, f, ensure_ascii=False, indent=4)

    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
