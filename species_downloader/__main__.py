import argparse
from species_downloader.downloader import SpeciesDownloader

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-s",
        "--species",
        default=None,
        type=str,
        help="Species to download separated with a comma.",
    )
    argparser.add_argument(
        "-w",
        "--workers",
        default=10,
        type=int,
        help="The number of workers."
    )
    argparser.add_argument(
        "-l",
        "--limit",
        default=1,
        type=int,
        help="The limit of imgs to download."
    )
    argparser.add_argument(
        "-f",
        "--file",
        default=None,
        type=str,
        help="Filename with species list separated with a new line."
    )
    argparser.add_argument(
        "-sd",
        "--save_dir",
        default="./downloads",
        type=str,
        help="Directory for saving images."
    )

    args = argparser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            species_list = [spec.strip() for spec in f.read().split('\n') if spec.strip()]
    else:
        species_list = [spec.strip() for spec in args.species.split(',')] if args.species else None

    if species_list:
        downloader = SpeciesDownloader(species_list)
        downloader.download(save_dir=args.save_dir,
                            num_workers=args.workers,
                            limit_img_per_species=args.limit)
    else:
        print('Specify species with --species or --file parameters')
