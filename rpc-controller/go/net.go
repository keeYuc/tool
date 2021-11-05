package rpc_client

import (
	"context"

	grpc "google.golang.org/grpc"
)

func Invoke(cc *grpc.ClientConn, ctx context.Context, method string, args, reply interface{}, opts ...grpc.CallOption) error {
	return cc.Invoke(ctx, method, args, reply, opts...)
}
