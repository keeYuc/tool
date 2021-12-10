
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2
rpc_url = 'file-center.regoo:9000'

with open('./564792.jpg') as f:
    s = f.read()
    server = file_center_service_pb2_grpc.FileCenterServiceStub(
        grpc.insecure_channel(rpc_url))
    rsb = server.UploadImage(image_pb2.UploadImageReq(
        AppId="GCP", CloseImgCompress="false", ImgContent=s))
    print(rsb)
