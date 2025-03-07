from tqdm import tqdm
from utils import write_csv, load_data
from verifier import Verifier

source_file = "data/source.json"
destination_file = 'data/result.csv'
rules_file = "config/rules.json"
headers = ["Page", "Valid", "Reason/Notes", "Review", "Url"]

ver = Verifier(rules_file)

data = load_data(source_file)
write_csv(headers=headers, file=destination_file)

for group, links in tqdm(data, unit="pages"):
  for link in tqdm(links, unit="links", colour='blue', leave=False):
    reason = ver.verify(link)
    reason = "" if not reason else reason
    valid = "Yes" if not reason else "No"
    write_csv([group, valid, reason, "No", link])