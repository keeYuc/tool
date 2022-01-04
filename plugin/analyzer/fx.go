package analyzer

import "app/model"

func Contain(arr []*model.Pure) []*model.Pure {
	long := len(arr)
	arr_new := make([]*model.Pure, 0, long)
	cache := new(model.Pure)
	for i := 0; i-1 < long; i++ {
		if arr[i].Contain(arr[i+1]) {
			//todo 包含
		} else if cache.H+cache.C+cache.L != 0 {
			arr_new = append(arr_new, cache)
			//todo
		} else {
			// todo
		}
	}
	return arr_new
}

func Fx(arr []*model.Pure) {}
