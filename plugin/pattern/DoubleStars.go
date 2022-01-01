package pattern

import "app/model"

type DoubleStars struct{}

func (d DoubleStars) LevelDay(tdx *model.Tdx) bool {
	//open close volume
	if tdx.Len < 3 {
		return false
	}
	return false
}
func (d DoubleStars) LevelM15(tdx *model.Tdx) bool {
	//close a60 macd
	return false
}
