# Local storage
* `mkdir -p prometheus-data`
* `docker compose up -d`

# Local storage
## On-disk layout
### ingested samples / grouped | blocks of 2 hours
* ⚠️you need to wait for | 2 hours / create the block⚠️
* `curl -XPOST http://localhost:9090/api/v1/admin/tsdb/snapshot`
  * force snapshot
* see the folder "/prometheus-data/snapshots/*/*"
### 2-hour block == directory / has 👀chunks subdirectory + ALL time series samples | 2 hours + metadata file + index file
* see the folder "/prometheus-data/snapshots/*/*"
* files WITHOUT extension
  * == binaries / TSDB's format
* `promtool tsdb analyze prometheus-data/snapshots/*`
  * analyze the TSDB's format files
#### grouped | >=1 segment files / <= 512MB
* `ls -lah prometheus-data/snapshots/**/chunks/`
  * check size < 512 MB
#### if series are deleted via the API -> deletion records are stored | separate tombstone files
* `ls -lah prometheus-data/snapshots/**/tombstones`
  * write down the size
* `curl -X POST \
  'http://localhost:9090/api/v1/admin/tsdb/delete_series?match[]=up'`
* `ls -lah prometheus-data/snapshots/**/tombstones`
  * Problems:
    * Problem1: Why has it SAME size?
      * Solution: TODO:
### CURRENT block
* prometheus-data/chunks_head
#### secured against crashes -- by a -- write-ahead log (WAL)
* prometheus-data/wal
### WAL
#### | 128MB segments
* `ls -lah prometheus-data/wal`
#### raw data / NOT yet compacted  -> 's size > regular block files
* `du -sh prometheus-data/wal/` >> `du -sh prometheus-data/snapshots/*/`
#### Prometheus retain >= 3 WAL files
* `ls -lah prometheus-data/wal`
### Prometheus runs as standalone server
* `docker ps | grep prometheus`
## Compaction
* TODO: how to proof
## Operational aspects
### Prometheus sample's size == 1-2 bytes
* Attempts:
  * Attempt1: `promtool tsdb analyze prometheus-data/snapshots/20251010T212759Z-7fa34e8dd01f7850/01K780C15ACZM8MVNM6FF94XC7 | grep -E "(samples|bytes|compression)"`
    * "no blocks found"
* Solution: TODO:
### Expired block cleanup
* Attempts:
  * Attempt1: `docker logs prometheus 2>&1 | grep -i "cleanup\|expired\|delete"`
    * nothing returned
* Solution: TODO:

# Remote storage integrations
## ways
### remote_write
* [here](/prometheus/documentation/examples/remote_storage/example_write_adapter)
### write receiver
* TODO:
### remote_read
* [here](/prometheus/documentation/examples/remote_storage/remote_storage_adapter)
### return data
* [here](https://github.com/dancer1325/grafana/tree/main/docs/sources/fundamentals/getting-started/first-dashboards/grafanaAndPrometheus)
## use a snappy-compressed protocol buffer encoding -- over -- HTTP
* TODO: 
# TODO: