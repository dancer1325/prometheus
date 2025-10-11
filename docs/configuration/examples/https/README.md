# requirements
* docker
* tools / generate bcrypt passwords
  * [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)
    * `brew install httpd`

# Basic Auth
* generate bcrypt passwords
  * `htpasswd -nBC 10 alice` & `htpasswd -nBC 10 bob` & pass password
* `docker compose up -d`
* localhost:9090
  * Problems:
    * Problem1: 401
      * Solution: remove ALL volumes
* https://localhost:9090
  * NOT exist
* http://localhost:9090/
  * alice/password
  * bob/password

## TLS
* create the certificates
  ```
  # Generar certificados self-signed
    openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
        -keyout server.key \
        -out server.crt \
        -subj "/C=US/ST=CA/L=San Francisco/O=MyOrg/CN=localhost"
  ```
* TODO: 