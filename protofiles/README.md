Для генерации protobuf файлов. Запускать внутри папки сервиса. 

```
python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/name --grpc_python_out=src/api/grpc/protobufs/name --pyi_out=src/api/grpc/protobufs/name ../protofiles/name.proto
```

python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/profiles --grpc_python_out=src/api/grpc/protobufs/profiles --pyi_out=src/api/grpc/protobufs/profiles ../protofiles/profiles.proto