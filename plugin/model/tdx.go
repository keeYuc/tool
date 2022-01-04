package model

type Pure struct {
	C     float32
	H     float32
	L     float32
	Range IndexRange
}

type IndexRange struct {
	L int
	R int
}

func (p *Pure) Contain(next *Pure) bool {
	return p.H >= next.H && p.L <= next.H
}

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

func ExchangePure(dataLen int, a, b, c []float32) []*Pure {
	arr := make([]*Pure, 0, dataLen)
	for i := 0; i < dataLen; i++ {
		item := new(Pure)
		item.C = a[i]
		item.H = b[i]
		item.L = c[i]
		item.Range.L = i
		item.Range.R = i
	}
	return arr
}
