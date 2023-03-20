import urllib.request as ur
import re
import sys
import pandas as pd
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers = {'User-Agent': user_agent}

argument_sitemap = sys.argv[1]
req = ur.Request(argument_sitemap, headers=headers)
base_sitemap = ur.urlopen(req, context=ctx)
base_sitemap_lines = base_sitemap.readlines()

# Build an OpenerDirector with HTTPSHandler and the context
opener = ur.build_opener(ur.HTTPSHandler(context=ctx))

output = []

for base_sitemap_step in base_sitemap_lines:
    data = re.findall(b'<loc>(https?://[^<]+)</loc>', base_sitemap_step)
    for sub_sitemap_from_base_sitemap in data:
        sub_sitemap_req = ur.Request(sub_sitemap_from_base_sitemap.decode('utf-8'), headers=headers)
        sub_sitemap = opener.open(sub_sitemap_req)
        sub_sitemap_lines = sub_sitemap.readlines()
        for sub_sitemap_step in sub_sitemap_lines:
            data2 = re.findall(b'<loc>(https?://[^<]+)</loc>', sub_sitemap_step)
            for page_from_sub_sitemap in data2:
                row = [page_from_sub_sitemap.decode('utf-8')]
                output.append(row)

df = pd.DataFrame(output)
df.to_csv('sitemap_extract.csv', index=False, header=['URLs'])
