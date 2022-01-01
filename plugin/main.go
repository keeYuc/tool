package main

import (
	"C"
)
import (
	"app/model"
	"app/patterns"
)

func main() {
}

//export DoubleStarsDay
func DoubleStarsDay(dataLen int, a, b, c []float32) (float32, int32) {
	tdx := model.Tdx{
		Len: dataLen,
		InA: a,
		InB: b,
		InC: c,
	}
	return patterns.DoubleStars{}.LevelDay(&tdx)
}

//export DoubleStarsM15
func DoubleStarsM15(dataLen int, a, b, c []float32) float32 {
	tdx := model.Tdx{
		Len: dataLen,
		InA: a,
		InB: b,
		InC: c,
	}
	return patterns.DoubleStars{}.LevelM15(&tdx)
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
