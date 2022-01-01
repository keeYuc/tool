package tool

//---------------------ma---------------------------
type Ma struct {
	Len     int
	History chan float32
	Value   float32
}

func NewMa(len int) Ma {
	return Ma{
		Len:     len,
		History: make(chan float32, len+1),
		Value:   0.0,
	}
}

func (m *Ma) Add(f float32) {
	if len(m.History) >= m.Len {
		m.Value -= <-m.History
	}
	m.History <- f
	m.Value += f
}

func (m *Ma) Get() float32 {
	return m.Value / float32(m.Len)
}

//---------------------ma---------------------------

//---------------------grow---------------------------
func GetGrow(l []float32, shift int) float32 {
	last := l[len(l)-1-shift-1]
	this := l[len(l)-1-shift]
	return (this - last) * 100 / last
}

//---------------------grow---------------------------
