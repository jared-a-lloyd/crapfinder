from imap_tools import MailBox, AND
import bs4
from bs4 import BeautifulSoup, SoupStrainer

from crapfinder.utils.password import get_app_password

def links_from_html(html_string) -> list[bs4.element.Tag]:
    links = []

    for link in BeautifulSoup(html_string, parse_only=SoupStrainer('a'), features='html.parser'):
        if link.has_attr('href'):
            links.append(link['href'])

    return links


def fetch_email_links(msg) -> tuple[str, list]:
    subj = msg.subject
    links = links_from_html(msg.html)

    return subj, links


def extract_links_from_gmail(sender_name: str):
    user, password = get_app_password()
    imap_url = 'imap.gmail.com'

    email_links = {}
    # use MailBox to fetch matching messages
    with MailBox(imap_url).login(user, password) as mailbox:
        for msg in mailbox.fetch(AND(from_=sender_name)):
            subj, links = fetch_email_links(msg)
            email_links[subj] = links

    return email_links


if __name__ == '__main__':
    results = extract_links_from_gmail('hello@email.lacolombe.com')

    from crapfinder.utils.url_handler.check_if_tracking import check_all_links
    results_df = check_all_links(results)