package rpc_client

import (
	"context"

	grpc "google.golang.org/grpc"
)

var methodMap map[string][]func(cc *grpc.ClientConn, ctx context.Context, method string, args, reply interface{}, opts ...grpc.CallOption)

func init() {

}

//type middleware interface {
//	getFn() func()
//}

//func middlewares_pure(method string) []func() {
//	return []func(){}
//}
//  全量请求监控，统计
// 外部调用部分 代码生成部分 代码生成器部分 数据监控中心部分
func middlewares(cc *grpc.ClientConn, ctx context.Context, method string, args, reply interface{}, opts ...grpc.CallOption) []func() {
	return []func(){}
}

func Invoke(cc *grpc.ClientConn, ctx context.Context, method string, args, reply interface{}, opts ...grpc.CallOption) error {
	for _, fn := range middlewares(cc, ctx, method, args, reply, opts...) {
		fn()
	}
	return cc.Invoke(ctx, method, args, reply, opts...)
}
