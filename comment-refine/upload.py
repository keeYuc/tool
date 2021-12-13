import grpc
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2
rpc_url = 'localhost:9007'
print("yes")
con = grpc.insecure_channel(rpc_url)
print("yes")
server = file_center_service_pb2_grpc.FileCenterServiceStub(con)
print("yes")
print(server)
with open('./564792.jpg', 'rb') as f:
    s = f.read()
    rsb = server.UploadImage(image_pb2.UploadImageReq(app_id="GCP", close_img_compress="false"))
    print(rsb)
