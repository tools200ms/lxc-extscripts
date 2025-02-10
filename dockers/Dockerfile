FROM 200ms/devuan_dev2

RUN apt install --assume-yes --no-install-recommends \
    capnproto libcapnp-dev build-essential gcc make \
    libssl-dev libpcre3-dev zlib1g-dev \
    ca-certificates git

RUN git -C /usr/src clone https://github.com/nginx/nginx.git

RUN cd /usr/src/nginx && ./auto/configure && make && make install

# --add-dynamic-module=/root/ds --with-http_ssl_module

# capnp compile -oc++ log.capnp

# gcc -o ngx_http_capnlog_module.so -fPIC -shared capnports_mod.c ./log.capnp.c++ -lcapnp -lssl -lcrypto
#RUN git -C /usr/src/ clone https://github.com/cloudflare/lua-capnproto.git
#RUN cd /usr/src/lua-capnproto; luarocks make
#luarocks install lua-capnproto
