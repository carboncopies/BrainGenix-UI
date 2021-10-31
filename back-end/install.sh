sudo apt install libnss3-tools -y

wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64

sudo cp mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert

sudo chmod +x /usr/local/bin/mkcert

mkcert -install

mkcert -CAROOT

mkcert localhost 127.0.0.1 ::1

mkdir .gitsecret

mv localhost+2.pem .gitsecret/cert.pem

mv localhost+2-key.pem .gitsecret/key.pem


