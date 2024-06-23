"""Entry point for a singular, manual run."""

from bcorag import misc_functions as misc_fns
from bcorag import option_picker as op
from bcorag.bcorag import BcoRag
from parameter_search.grid_search import BcoGridSearch
from bcorag.custom_types import create_git_data
from parameter_search.custom_types import create_git_data_file_config, init_search_space
import argparse
import os


def main():

    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument(
        "run_mode",
        default="one-shot",
        nargs="?",
        choices=["one-shot", "grid-search", "random-search"],
        help="one-shot/grid-search/random-search",
    )
    options = parser.parse_args()
    run_mode = options.run_mode.lower().strip()

    match run_mode:

        case "one-shot":

            logger = misc_fns.setup_root_logger("./logs/bcorag.log")
            logger.info(
                "################################## RUN START ##################################"
            )

            user_choices = op.initialize_picker()
            if user_choices is None:
                misc_fns.graceful_exit()

            bco_rag = BcoRag(user_choices)
            while True:
                domain = bco_rag.choose_domain()
                if domain is None or isinstance(domain, tuple):
                    misc_fns.graceful_exit()
                _ = bco_rag.perform_query(domain)
                print(f"Successfully generated the {domain} domain.\n")

        case "grid-search":

            logger = misc_fns.setup_root_logger("./logs/grid-search.log")
            logger.info(
                "################################## RUN START ##################################"
            )

            filenames = ["./bcorag/test_papers/High resolution measurement.pdf"]
            loaders = "SimpleDirectoryReader"
            chunking_config = [
                "1024 chunk size/20 chunk overlap",
                "2048 chunk size/50 chunk overlap",
            ]
            embedding_model = "text-embedding-3-large"
            vector_store = "VectorStoreIndex"
            similarity_top_k = [2, 3, 4]
            llms = ["gpt-3.5-turbo", "gpt-4-turbo"]

            github_url = "https://github.com/dpastling/plethora"
            git_info = misc_fns.extract_repo_data(github_url)
            if git_info is None:
                misc_fns.graceful_exit(1, "Error parsing github URL.")
            git_data = create_git_data(git_info[0], git_info[1], "master")
            git_file_data = create_git_data_file_config(
                os.path.basename(filenames[0]), git_data
            )

            search_space = init_search_space(
                filenames=filenames,
                loader=loaders,
                chunking_config=chunking_config,
                embedding_model=embedding_model,
                vector_store=vector_store,
                similarity_top_k=similarity_top_k,
                llm=llms,
                git_data=[git_file_data],
            )

            grid_search = BcoGridSearch(search_space)
            grid_search.train()

            misc_fns.graceful_exit()

        case "random-search":
            # TODO : implement
            pass

        case _:

            misc_fns.graceful_exit(1, "Unsupported run mode.")


if __name__ == "__main__":
    main()
