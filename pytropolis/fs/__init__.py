## Create a new instance of the MinioFileManager class
from pytropolis.fs.minio_fs import MinioFileManager
from pytropolis.configuration import get_configuration

def create_minio_file_manager():
    """
    Create a new instance of the MinioFileManager class.
    """
    cfg = get_configuration()

    __instance = MinioFileManager(
        cfg['minio']['endpoint'], 
        cfg['minio']['access_key'], 
        cfg['minio']['secret_key'], 
        cfg['minio']['secure']
    )
    
    return __instance