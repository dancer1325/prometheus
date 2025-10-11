## Remote Write Adapter Example

* goal
  * how to write a server / receive samples -- from the -- remote storage output

* steps
  * | this path,
    * `go build`
      * generate "./example_write_adapter" 
    * `./example_write_adapter`
    * `docker compose up -d`

* checks
  * | `./example_write_adapter`
    * logs ALL metrics scrapped