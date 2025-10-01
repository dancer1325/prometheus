---
title: Writing HTTP service discovery
nav_title: HTTP SD
sort_rank: 7
---

## Comparison between File-Based SD and HTTP SD

* generic Service Discovery implementations
  * [File SD](https://prometheus.io/docs/guides/file-sd/#use-file-based-service-discovery-to-discover-scrape-targets)
  * [HTTP SD](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#http_sd_config)

| Item             | File SD                         | HTTP SD                                       |
|------------------|---------------------------------|-----------------------------------------------|
| Event Based      | Yes -- via -- inotify           | No                                            |
| Update frequency | INSTANT -- thanks to -- inotify | -- based on -- refresh_interval               |
| Format           | Yaml or JSON                    | JSON                                          |
| Transport        | Local file                      | HTTP/HTTPS                                    |
| Security         | File-Based security             | TLS, Basic auth, Authorization header, OAuth2 |

## Requirements of HTTP SD endpoints

* uses
  * | implement an HTTP SD endpoint

* response
  * consumed as it's
    * == unmodified
  * requirements
    * status: 200
    * `-H Content-Type: application/json`
    * UTF-8 formatted 
* request
  * `-H X-Prometheus-Refresh-Interval-Seconds:refresh_interval`

* TODO:     
If no targets should be transmitted, HTTP 200 must also be emitted, with an empty list `[]`
Target lists are unordered.

Prometheus caches target lists. If an error occurs while fetching an updated
targets list, Prometheus keeps using the current targets list. The targets list
is not saved across restart. The `prometheus_sd_http_failures_total` counter
metric tracks the number of refresh failures.

The whole list of targets must be returned on every scrape. There is no support
for incremental updates. A Prometheus instance does not send its hostname and it
is not possible for a SD endpoint to know if the SD requests is the first one
after a restart or not.

The URL to the HTTP SD is not considered secret. The authentication and any API
keys should be passed with the appropriate authentication mechanisms. Prometheus
supports TLS authentication, basic authentication, OAuth2, and authorization
headers.

## HTTP_SD format

```json
[
  {
    "targets": [ "<host>", ... ],
    "labels": {
      "<labelname>": "<labelvalue>", ...
    }
  },
  ...
]
```

* _Examples:_

    ```json
    [
        {
            "targets": ["10.0.10.2:9100", "10.0.10.3:9100", "10.0.10.4:9100", "10.0.10.5:9100"],
            "labels": {
                "__meta_datacenter": "london",
                "__meta_prometheus_job": "node"
            }
        },
        {
            "targets": ["10.0.40.2:9100", "10.0.40.3:9100"],
            "labels": {
                "__meta_datacenter": "london",
                "__meta_prometheus_job": "alertmanager"
            }
        },
        {
            "targets": ["10.0.40.2:9093", "10.0.40.3:9093"],
            "labels": {
                "__meta_datacenter": "newyork",
                "__meta_prometheus_job": "alertmanager"
            }
        }
    ]
    ```
