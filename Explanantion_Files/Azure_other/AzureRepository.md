# Azure Repository

## Create Directory and Sub-directory

```python
from azure.storage.fileshare import ShareDirectoryClient
import upload_to_azure

dir_client = ShareDirectoryClient.from_connection_string(c_str, s_name, d_path)
dir_client.create_directory()

for subd_name in sub_dirs:
    dir_client.create_subdirectory(subd_name)
```

---

## Upload

```python
from azure.storage.fileshare import ShareFileClient

file_client = ShareFileClient.from_connection_string(c_str, s_name, file_path)
with open(source_name, "rb") as source_file:
    file_client.upload_file(source_file)
```

---

## Download

```python
from azure.storage.fileshare import ShareFileClient

file_client = ShareFileClient.from_connection_string(c_str, s_name, file_path)

with open(desti_dir + "/" + ele['name'], "wb") as data:
    stream = file_client.download_file()
    data.write(stream.readall())
```

---

## Delete

```python
from azure.storage.fileshare import ShareDirectoryClient

dir_client = ShareDirectoryClient.from_connection_string(c_str, s_name, d_path)
dir_client.delete_directory()

from azure.storage.fileshare import ShareFileClient

file_client = ShareFileClient.from_connection_string(c_str, s_name, file_path)
file_client.delete_file()
```

---

## List

```python
from azure.storage.fileshare import ShareDirectoryClient

dir_client = ShareDirectoryClient.from_connection_string(c_str, s_name, d_path)

for item in dir_client.list_directories_and_files():
    print(item)
```