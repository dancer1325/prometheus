---
title: Remote Read API
sort_rank: 7
---

* `/api/v1/read`
  * ⚠️EXPERIMENTAL⚠️
    * == ❌NOT part of stable API❌
  * allows
    * external clients can read Prometheus's functionality 
  * [snappy](https://github.com/google/snappy) compression
  * [API definition](https://github.com/prometheus/prometheus/blob/main/prompb/remote.proto)
    * [Protobuf definitions](https://buf.build/prometheus/prometheus/docs/main:prometheus#prometheus.ReadRequest)
  * 's return
    * raw samples / match the requested query
  * ' goal
    * programmatic integration
      * ❌NOT manual hit❌
  * ⚠️-- via -- POST⚠️

## Streamed Chunks

* TODO: These streamed chunks utilize an XOR algorithm inspired by the [Gorilla](http://www.vldb.org/pvldb/vol8/p1816-teller.pdf)
compression to encode the chunks
However, it provides resolution to the millisecond instead of to the second.
