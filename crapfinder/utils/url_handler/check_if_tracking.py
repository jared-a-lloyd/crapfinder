DELIVERY_URL_STRINGS = ['ups.com', 'fedex.com', 'dhl.com', 'usps.com']

import requests
import pandas as pd

def check_tracking_url(url_str: str) -> bool:
    for s in DELIVERY_URL_STRINGS:
        if s in url_str.lower():
            return True

    return False


def is_a_tracking_link(url_str: str) -> tuple[bool, str]:
    # first check if url base string is a tracking url
    is_tracking = check_tracking_url(url_str)

    if is_tracking:
        return True, url_str

    # try following any redirects
    try:
        r = requests.get(url_str, allow_redirects=True)
    except Exception as e:
        return False, url_str

    is_tracking =  check_tracking_url(r.url)
    if is_tracking:
        return is_tracking, r.url
    else:
        return is_tracking, url_str


def check_all_links(mail_links: dict):
    # loop through emails
    tracking_dict = {}
    i_count = -1
    for key in mail_links.keys():
        for url_str in mail_links[key]:
            print('Checking:', url_str)
            i_count += 1

            # remove any mailto links
            if url_str.startswith('mailto'):
                tracking_dict[i_count] = [url_str, False]
                continue

            # check url
            tracking_dict[i_count] = list(is_a_tracking_link(url_str))

    return (
        pd.DataFrame
        .from_dict(tracking_dict, orient='index')
        .rename(columns={1: 'url', 0: 'is_tracking'})
    )

