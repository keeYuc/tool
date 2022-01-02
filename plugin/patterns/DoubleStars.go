package patterns

import (
	"app/model"
	"app/tool"
)

type DoubleStars struct{}

func (d DoubleStars) LevelDay(tdx *model.Tdx) (float32, int32) {
	level := 15
	// close volume diffMa5
	if tdx.Len < 4 {
		return 1, 1
	}
	zf2 := tool.GetGrow(tdx.InA, 2) //>2%涨幅
	if zf2 < 2 {
		return zf2, 2
	}
	zf1 := tool.GetGrow(tdx.InA, 1) //第二天需要回调不能超过涨幅单次70%
	xd1 := zf1 * 100 / zf2
	if xd1 <= -70 || xd1 >= 15 {
		return xd1, 3
	}
	zf0 := tool.GetGrow(tdx.InA, 0) //第三天需要回调不能超过涨幅单次70%
	xd0 := zf0 * 100 / zf2
	if xd0 <= -70 || xd0 >= 15 {
		return xd0, 4
	}
	if xd0+xd1 <= -70 || xd0+xd1 >= 30 { //总回撤超过70%上涨超过30%
		return xd0 + xd1, 5
	}

	if tdx.InA[tdx.Len-1-2] <= tool.PureLastMa(tdx.InA, level)*1.02 { //超过15日均线2%
		return 1, 6
	}
	if tool.GetMax(tdx.InA[:tdx.Len-1-2], level) > tdx.InA[tdx.Len-1-2] { // 15日最高
		return tool.GetMax(tdx.InA[:tdx.Len-1-2], level), 7
	}
	if tdx.InB[tdx.Len-1-1] > tdx.InB[tdx.Len-1-2] || tdx.InB[tdx.Len-1] > tdx.InB[tdx.Len-1-2] { // 回调缩量
		return 1, 8
	}
	min := tool.GetMin(tdx.InA, level*2)
	if (tdx.InA[tdx.Len-1]-min)/min > 0.1 { //30日最大涨幅小于10%
		return (tdx.InA[tdx.Len-1] - min) / min, 9
	}
	//15 日最低价反向数量
	low_index := tool.GetMinCount(tdx.InA, level)
	up := tool.GetUpSum(tdx.InC, low_index)
	if up/tdx.InA[tdx.Len-1] > 0.035 { //15日内5日均线上升总幅度小于%
		return up, 10
	}
	return 0, 0
}
func (d DoubleStars) LevelM15(tdx *model.Tdx) float32 {
	//close a60 macd
	return 0
}



