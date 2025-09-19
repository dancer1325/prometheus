* protobufs
  * ALREADY, are 
    * compiled
    * versioned
    * controlled
  * | build Prometheus,
    * ❌NOT NORMALLY need to re-compile them❌
    * if you have modified the defs -> need to re-compile
      * steps
        * | root path
          * install [protoc v3.15.8>](https://protobuf.dev/installation/)
            * 
          * uncomment [Makefile.common](/prometheus/Makefile.common)
          * `make common-proto`
