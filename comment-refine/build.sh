#python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/seo --python_out=./protocol --grpc_python_out=./protocol ./protobuf/seo/
#python -m grpc_tools.protoc -I ./protobuf  --python_out=./protocol --grpc_python_out=./protocol ./protobuf/*.proto
python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/file-center --python_out=./protocol --grpc_python_out=./protocol ./protobuf/file-center/file_center_service.proto
python -m grpc_tools.protoc -I ./protobuf -I ./protobuf/file-center --python_out=./protocol --grpc_python_out=./protocol ./protobuf/file-center/image.proto
echo "build fin"