package main

import (
	"C"
)
import (
	"app/model"
	"app/pattern"

	"honnef.co/go/tools/pattern"
)

func main() {
}

//export DoubleStarsDay
func DoubleStarsDay(tdx model.Tdx) bool {
	return pattern.DoubleStars{}.LevelDay(&tdx)
}

//export DoubleStarsM15
func DoubleStarsM15(tdx model.Tdx) bool {
	return pattern.DoubleStars{}.LevelM15(&tdx)
}

////* test data
////export SendData
//func SendData(a, b, c []float32) {
//	data := map[string][]float32{
//		"a": a,
//		"b": b,
//		"c": c,
//	}
//	res, _ := json.Marshal(data)
//	buf := new(bytes.Buffer)
//	buf.Write(res)
//	req, _ := http.NewRequest(http.MethodPost, "http://localhost:8080/debug/", buf)
//	client := http.Client{}
//	client.Do(req)
//}
