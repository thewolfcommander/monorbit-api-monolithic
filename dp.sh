git add . && git commit -m "Fixed bug in Creating Support Tickets"
git push origin master
ssh -i "monorbit-alpha.pem" -t ubuntu@ec2-54-187-152-205.us-west-2.compute.amazonaws.com 'cd /usr/local/apps/monorbit-api-monolithic/; sudo sh /usr/local/apps/monorbit-api-monolithic/deploy/update.sh; exec $SHELL'
exit

# thewolfcommander
# Billionaire2201