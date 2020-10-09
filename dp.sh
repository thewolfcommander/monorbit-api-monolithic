git add . && git commit -m "Deploying on AWS EC2"
git push origin master
ssh -i "monorbit-alpha.pem" ubuntu@ec2-54-187-152-205.us-west-2.compute.amazonaws.com