# handy-scrapers
 A collection of handy web scrapers

Docker setup...
```
docker build -t scrapers .
docker run --rm -it -p 8881:8881 -v "`pwd`":/data scrapers
```