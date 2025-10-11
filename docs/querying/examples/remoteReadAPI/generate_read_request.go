package main

import (
	"fmt"
	"os"
	"time"

	"github.com/gogo/protobuf/
	"github.com/golang/snappy"
	"github.com/prometheus/prometheus/prompb"
)

func main() {
	// Crear ReadRequest
	req := &prompb.ReadRequest{
		Queries: []*prompb.Query{
			{
				Matchers: []*prompb.LabelMatcher{
					{
						Type:  prompb.LabelMatcher_EQ,
						Name:  "__name__",
						Value: "up",
					},
				},
				StartTimestampMs: time.Now().Add(-1 * time.Hour).UnixMilli(),
				EndTimestampMs:   time.Now().UnixMilli(),
			},
		},
	}

	// Serializar a protobuf
	data, err := proto.Marshal(req)
	if err != nil {
		panic(err)
	}

	// Comprimir con snappy
	compressed := snappy.Encode(nil, data)

	// Guardar a archivo
	err = os.WriteFile("readrequest.pb", compressed, 0644)
	if err != nil {
		panic(err)
	}

	fmt.Printf("ReadRequest generado: readrequest.pb (%d bytes)\n", len(compressed))
}
