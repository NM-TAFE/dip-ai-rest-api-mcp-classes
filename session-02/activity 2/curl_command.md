<!-- Common format for testing MCP servers -->

curl 'http://127.0.0.1:5000/?date=2026-01-21&start_date=&end_date=&count=' \
 -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,_/_;q=0.8,application/signed-exchange;v=b3;q=0.7' \
 -H 'Accept-Language: en-AU,en;q=0.9' \
 -H 'Connection: keep-alive' \
 -H 'Referer: http://127.0.0.1:5000/?date=&start_date=&end_date=&count=' \
 -H 'Sec-Fetch-Dest: document' \
 -H 'Sec-Fetch-Mode: navigate' \
 -H 'Sec-Fetch-Site: same-origin' \
 -H 'Sec-Fetch-User: ?1' \
 -H 'Upgrade-Insecure-Requests: 1' \
 -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0' \
 -H 'sec-ch-ua: "Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'sec-ch-ua-platform: "Windows"'
