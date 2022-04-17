sudo mn -c
git pull
sudo rm -r profinet_states/*
sudo rm -r logs/*
sudo rm -r swat_s2_db.sqlite
sudo python init.py
sudo killall -e pn_dev
sudo killall -e python2
sudo killall -e python
sudo killall -e python3
