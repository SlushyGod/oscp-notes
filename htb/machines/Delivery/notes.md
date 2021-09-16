visiting the site we get a subdomain -> http://helpdesk.delivery.htb
http://delivery.htb:8065 <- "mattermost server"

server version -> nginx/1.14.2

had to add the subdomain to hosts file

http://helpdesk.delivery.htb:
- seems to be a ticketing platform, might be able to get sqli or file upload since you are allowed to view the attachment
- we know its running python so keep that in mind (most likely flask because of port 5000)
- running osTicket which has quite a few exploits