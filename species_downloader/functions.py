from tqdm import tqdm
from hashlib import sha1
import os
import requests
import json
import time
import random
import logging

INAT_BASE_URL = 'https://www.inaturalist.org'


def arg_wrapper(func):
    """
    Use one argument as *args
    """
    def wrap(args):
        func(*args)
    return wrap


def get_img_links(spec: str,
                  logger: logging.Logger,
                  progress_bar: tqdm = None,
                  limit: int = 10) -> list[str]:
    """
    Get image links from observations of spec from iNaturalist API.
    """
    result = []
    count = 0
    pages = (limit // 199) + 1
    for page_num in range(pages):
        if count >= limit:
            break
        time.sleep(random.uniform(0.2, 0.4))
        resp_observ = requests.get(f'{INAT_BASE_URL}/observations.json',
                                   params={'taxon_name': spec, 'page': page_num, 'per_page': 199})
        if resp_observ.status_code != 200:
            logger.info(f'API request status: {resp_observ.status_code} for {spec}')
            continue

        observations = json.loads(resp_observ.content)
        if observations:
            for obs in observations:
                if count >= limit:
                    break
                taxon = obs.get('taxon', None)
                if taxon:
                    name = taxon['name'].lower()
                else:
                    name = ''
                if spec not in name:
                    logger.info(f'Check species name {spec}')
                    break
                if spec in name and obs['photos']:
                    url = obs['photos'][0]['large_url']
                    result.append(url)
                    count += 1
                    if progress_bar:
                        progress_bar.update()
        else:
            logger.info(f'Not found {limit - count} observations for {spec}')
            break

    return result


def get_url_save_pairs(urls_dict: dict[str, list[str]],
                       save_dir: str) -> list[tuple[str, str]]:
    """

    """
    result = []
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    for spec, urls in urls_dict.items():
        spec_dir = os.path.join(save_dir, spec)
        if not os.path.exists(spec_dir):
            os.mkdir(spec_dir)
        for url in urls:
            filename = sha1(str.encode(url)).hexdigest() + ".jpeg"
            save_path = os.path.join(spec_dir, filename)
            result.append((url, save_path))
    return result


@arg_wrapper
def download_img(url: str, save_path: str) -> None:
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'INFO: Failed download image {url}')
        return
    img_data = resp.content
    with open(save_path, 'wb') as handler:
        handler.write(img_data)
        handler.close()
