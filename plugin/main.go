package main

import (
	"C"
	"bytes"
	"encoding/json"
	"net/http"
)

func main() {
}

//export SendData
func SendData(a, b, c []float32) {
	data := map[string][]float32{
		"a": a,
		"b": b,
		"c": c,
	}
	res, _ := json.Marshal(data)
	buf := new(bytes.Buffer)
	buf.Write(res)
	req, _ := http.NewRequest(http.MethodPost, "http://localhost:8080/debug/", buf)
	client := http.Client{}
	client.Do(req)
}
