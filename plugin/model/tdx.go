package model

type Tdx struct {
	Len int
	InA []float32
	InB []float32
	InC []float32
}

func Exchange(dataLen int, a, b, c []float32) Tdx {
	return Tdx{
		Len: dataLen,
		InA: a,
		InB: b,
		InC: c,
	}
}
