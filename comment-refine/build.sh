python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/seo --python_out=./protocol --grpc_python_out=./protocol ./protobuf/seo/data.proto
python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/seo  --python_out=./protocol --grpc_python_out=./protocol ./protobuf/seo/seo_service.proto
#python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/file-center --python_out=./protocol --grpc_python_out=./protocol ./protobuf/file-center/file_center_service.proto
#python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/file-center --python_out=./protocol --grpc_python_out=./protocol ./protobuf/file-center/image.proto
echo "build fin"