# Команды для генерации protobuf файлов

Запускать внутри папки сервиса.

## Общая команда:

```
python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/name --grpc_python_out=src/api/grpc/protobufs/name --pyi_out=src/api/grpc/protobufs/name ../protofiles/name.proto
```

## Команда для генерации файлов accounts сервиса:

```
python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/accounts --grpc_python_out=src/api/grpc/protobufs/accounts --pyi_out=src/api/grpc/protobufs/accounts ../protofiles/accounts.proto
```

## Команда для генерации файлов profiles сервиса:

```
python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/profiles --grpc_python_out=src/api/grpc/protobufs/profiles --pyi_out=src/api/grpc/protobufs/profiles ../protofiles/profiles.proto
```

## Команда для генерации файлов recommendations сервиса:

```
python -m grpc_tools.protoc -I ../protofiles --python_out=src/api/grpc/protobufs/recommendations --grpc_python_out=src/api/grpc/protobufs/recommendations --pyi_out=src/api/grpc/protobufs/recommendations ../protofiles/recommendations.proto
```
