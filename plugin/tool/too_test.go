package tool

import (
	"fmt"
	"testing"
)

func Test_All(t *testing.T) {
	l := make(chan int, 10)
	l <- 1
	fmt.Println(len(l))
}

func Test_Ma(t *testing.T) {
	// 1,2,3,4 = 2.5
	ma := NewMa(4)
	fmt.Println(ma.Get())
	for i := 0; i < 5; i++ {
		ma.Add(float32(i))
	}
	fmt.Println(ma.Get())
	//2,3,4,5 = 3.5
	ma.Add(float32(5))
	fmt.Println(ma.Get())
}

func Test_Grow(t *testing.T) {
	l := []float32{1, 2, 3}
	// 50
	grow := GetGrow(l, 0)
	if grow != 50 {
		t.Error(grow)
	}
	//100
	grow = GetGrow(l, 1)
	if grow != 100 {
		t.Error(grow)
	}
}
