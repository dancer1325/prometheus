* `docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus`

# manual hit
* hit [sample.http](sample.http)
  * return 200 & Content-Length: NOT empty
    * TODO: how to decompress the response

# Notes
* [readrequest.pb](readrequest.pb)
  * generated -- via -- `go run generate_read_request.go`
  * uses
    * required by "/v1/read"