# image-crawler

Crawl images from https://www.24h.com.vn/thoi-trang-c78.html 

# RUN

### crawl images only one time
<pre>
usage : crawler.py [--n N]

options:

  --n N         The number of images downloads in one time, default = 3

</pre>

### crawl images periodically
<pre>
usage: crawler.py [-h] [--s S] [--m M] [--h H] [--e HH:MM:SS] [--n N]   

options:<br />
  -h, --help    show this help message and exit<br />
  --s S         Run crawler after every S seconds<br />
  --m M         Run crawler after every M minutes<br />
  --h H         Run crawler after every H hours<br />
  --e HH:MM:SS  Run crawler every day at specific HH:MM:SS<br />
  --n N         The number of images downloads in one time, default = 3<br />
</pre>
