package main

import "fmt"




func main(){
	ts_test1()
	ts_test2()
}

func ts_test1(){
	print("im 1")
}
func ts_test2(){
	print("im 2")
}

func print(a string){
	fmt.Println(a)
}