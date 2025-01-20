# ساخت دیتابیس
cd ~postgres/
sudo -u postgres psql -c "CREATE DATABASE oktavaz;"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'akjsfkj22WEQDS@#DSA';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE oktavaz TO postgres;"
echo "Database created"
