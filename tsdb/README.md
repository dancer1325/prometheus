# TSDB

* == Prometheus TSDB (Time Series DataBase) library /
  * handles storage
  * query ALL Prometheus v2 data

## Documentation

* [Data format](docs/format/README.md)
* [Usage](docs/usage.md)
* [Bstream details](docs/bstream.md)

## External resources

* [ORIGINAL design](docs/originalDesign.md)
* Video: [Storing 16 Bytes at Scale](https://youtu.be/b_pEevMAC3I) from [PromCon 2017](https://promcon.io/2017-munich/).
* Compression is based on the Gorilla TSDB [white paper](http://www.vldb.org/pvldb/vol8/p1816-teller.pdf).


A series of blog posts explaining different components of TSDB:
* [The Head Block](https://ganeshvernekar.com/blog/prometheus-tsdb-the-head-block/)
* [WAL and Checkpoint](https://ganeshvernekar.com/blog/prometheus-tsdb-wal-and-checkpoint/)
* [Memory Mapping of Head Chunks from Disk](https://ganeshvernekar.com/blog/prometheus-tsdb-mmapping-head-chunks-from-disk/)
* [Persistent Block and its Index](https://ganeshvernekar.com/blog/prometheus-tsdb-persistent-block-and-its-index/)
* [Queries](https://ganeshvernekar.com/blog/prometheus-tsdb-queries/)
* [Compaction and Retention](https://ganeshvernekar.com/blog/prometheus-tsdb-compaction-and-retention/)
* [Snapshot on Shutdown](https://ganeshvernekar.com/blog/prometheus-tsdb-snapshot-on-shutdown/)


## Examples

### [example_test.go](example_test.go)

* how to execute?
  * `go test example_test.go`
    * Problems:
      * Problem1: "./example_test.go:37:13: undefined: Open - ./example_test.go:37:33: undefined: DefaultOptions"
        * Solution: `go test -run Example`

* how to debug locally?
  * -- via -- Jetbrains IDE

    ![](static/debugJetbrainsSetUp.png)

### TODO: 