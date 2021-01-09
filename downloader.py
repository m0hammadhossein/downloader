from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
from argparse import ArgumentParser

disable_warnings(InsecureRequestWarning)

def progress(current, total):
    t = int(current * 100 / total)
    t2 = int(current * 20 / total)
    p = (t2 * '█') + ((20 - t2) * '░')
    return p + f' [%{t}]'

def filesize(x):
    types = ('TB', 'GB', 'MB', 'KB', 'B')
    cn = 4
    while x >= 1024:
        cn -= 1
        x /= 1024
    return '{:.2f} {:s}'.format(x, types[cn])

parser = ArgumentParser()
parser.add_argument('-u', required=True, dest='url', help='enter url', type=str)
parser.add_argument('-o', required=True, dest='file', help='enter name output file', type=str)
args = parser.parse_args()
try:
    with open(args.file, 'ab+') as file:
        downloaded = file.seek(0, 2)
        headers = {'Accept-Encoding': 'identity', 'Range': f'bytes={downloaded}-'}
        url = get(args.url, stream=True, headers=headers, verify=False)
        total = int(url.headers.get('content-length')) + downloaded
        t_total = filesize(total)
        try:
            for data in url.iter_content(chunk_size=1048576):
                file.write(data)
                downloaded += len(data)
                print(progress(downloaded, total), f'{filesize(downloaded)}/{t_total}', end='\r')
        except KeyboardInterrupt:
            print('\nStopped')
            exit(1)
    print('\ncompeleted')
except Exception as e:
    print(e.__str__())