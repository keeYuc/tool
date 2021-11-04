package main

import "sync"

var a = sync.WaitGroup{}

func main() {
	a.Add(1)
	a.Add(-100)
}

//func DoSyncFunc(funcList *[]string) {
//	*funcList = append(*funcList, "a")
//}

//func main() {
//	//list := make([]string, 0, 10)
//	//go DoSyncFunc(&list)
//	//go DoSyncFunc(&list)
//	//go DoSyncFunc(&list)
//	//go DoSyncFunc(&list)
//	//go DoSyncFunc(&list)
//	//go DoSyncFunc(&list)
//	//time.Sleep(time.Second)
//	//fmt.Println(list)
//	sync_chan := make(chan string, 10)
//	sync_chan <- "11"
//	sync_chan <- "11"
//	sync_chan <- "11"
//	sync_chan <- "11"
//a:
//	for {
//		select {
//		case id := <-sync_chan:
//			fmt.Println(id)
//		default:
//			fmt.Println("wu")
//			time.Sleep(time.Second)
//			break a
//		}
//	}
//	fmt.Println("yes")
//	fmt.Println("yes")
//	fmt.Println("yes")
//	fmt.Println("yes")
//	fmt.Println("yes")
//}
