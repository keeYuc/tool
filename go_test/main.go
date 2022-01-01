package main

import (
	"C"
)
import "fmt"

func main() {}

//export Show
func Show() {
	fmt.Println("welcome use go")
}

//export Add
func Add(a int) int {
	return a + 1
}
