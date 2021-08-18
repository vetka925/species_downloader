from species_downloader.functions import get_img_links, get_url_save_pairs, download_img
import logging
from tqdm import tqdm
import concurrent.futures


def init_logger(level: int) -> logging.Logger:
    FORMAT_STR = '%(asctime)s %(levelname)s %(message)s'
    logger = logging.getLogger()
    formatter = logging.Formatter(FORMAT_STR)
    ch = logging.StreamHandler()
    ch.name = 'Download Logger'
    ch.formatter = formatter
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger


logs = init_logger(logging.INFO)


class SpeciesDownloader:
    def __init__(self, species_names: list[str],
                 logger: logging.Logger = logs) -> None:

        self.species_names = species_names
        self.logger = logger

    def download(self, save_dir: str, num_workers: int = 10, limit_img_per_species: int = 15) -> None:

        self.logger.info('Start getting species images urls from INAT API')
        urls_dict = {}
        total = len(self.species_names) * limit_img_per_species
        with tqdm(total=total) as progress_bar:
            for spec in self.species_names:
                urls = get_img_links(spec.lower().strip(), self.logger, progress_bar, limit_img_per_species)
                urls_dict[spec] = urls
                self.logger.info(f'{len(urls)} URLS found for {spec}')

        if sum(map(len, urls_dict.values())) == 0:
            self.logger.info('No img URLs found')
            self.logger.info('Stop downloading')
            return

        self.logger.info('Start preparing save paths')
        url_pairs = get_url_save_pairs(urls_dict, save_dir)
        self.logger.info('Start downloading')
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(tqdm(executor.map(download_img, url_pairs), total=len(url_pairs)))
