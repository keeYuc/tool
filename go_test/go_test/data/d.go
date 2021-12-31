package data

var datas []string

func Add(str string) string {
	data := []byte(str)
	sData := string(data)
	for i := range str {
		datas = append(datas, string(i))
	}

	return sData
}
