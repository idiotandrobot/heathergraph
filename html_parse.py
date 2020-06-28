import imp
import logging
log = logging.getLogger(__name__)

def module_exists(module_name):
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

if module_exists("bs4"):    
    log.info("Parsing HTML using beautifulsoup4")
    from bs4 import BeautifulSoup

    def parse(html):
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text()
elif module_exists("html2text"):    
    log.info("Parsing HTML using html2text")
    import html2text

    def parse(html):
        h = html2text.HTML2Text()
        h.single_line_break = True
        return h.handle(html)
else:
    warning_msg = "HTML parsing not available. Install beautifulsoup4 or html2text"
    log.warning(warning_msg)
    def parse(html):
        raise ImportWarning(warning_msg)