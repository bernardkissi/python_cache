import redis
import os
import sys
import shutil
from datetime import datetime


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    backup_path = 'backups/'

    def __init__(self, host: str = 'localhost', port: int = 6379, db=0, encoding='utf-8', decode_responses=True):
        self.__host = host
        self.__port = port
        self.client = redis.Redis(host=self.__host, port=self.__port, db=0)

    def createBackup(self):
        config_dir = self.getConfigDir()
        res = self.client.bgsave()
        if res:
            self.copyToBackupDir(config_dir, self.backup_path, self.__port)
            print("Redis db:0 backup successfully")
        else:
            print("Redis db:0 backup failed")

    def restore(self):
        pass

    def getConfigDir(self):
        d = self.client.config_get('dir')
        dbfilename = self.client.config_get('dbfilename')
        return '%s/%s' % (d['dir'], dbfilename['dbfilename'])

    @staticmethod
    def copyToBackupDir(rdbFile: str, backup_dir: str, port: int):
        backup_filename = '%s/%s_%s_port_%d.rdb' % (backup_dir, datetime.now(), 'dump', port)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        elif not os.path.isdir(backup_dir):
            sys.stderr.write('backupdir: %s is not a directory.\n' % backup_dir)
            return False
        elif os.path.exists(backup_filename):
            sys.stderr.write('backupfile: %s already exists.\n' % backup_filename)
            return False
        shutil.copy2(rdbFile, backup_filename)
