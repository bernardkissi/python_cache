import redis
import os
import sys
import glob
import time
import shutil
import subprocess
from datetime import datetime


class AutoStartConnection(redis.Connection):
    # overrides redis.Connection.connect
    def connect(self):
        """connect but start Redis if it is not there"""
        connect = super(AutoStartConnection, self).connect
        try:
            connect()
        except redis.exceptions.ConnectionError:
            print("Redis offline, starting it.")
            subprocess.Popen(["redis-server"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
            time.sleep(1)
            connect()
            print("Redis start successful.")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RedisClient(metaclass=Singleton):
    backup_path = 'backups/'
    # change value to suit your path # type 'config get dir' in the terminal
    redis_dump_path = '/usr/local/var/db/redis/'

    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.__host = host
        self.__port = port
        self.connection = redis.ConnectionPool(connection_class=AutoStartConnection)
        self.client = redis.Redis(host=self.__host, port=self.__port, db=0, encoding='utf-8',
                                  decode_responses=True, connection_pool=self.connection)
        self.client.config_set('dir', self.redis_dump_path)

    def createBackup(self):
        config_dir = self.getConfigDir()
        print(config_dir)
        backup_filename = '%s/%s_%s_port_%d.rdb' % (self.backup_path, datetime.now(), 'dump', self.__port)
        res = self.client.bgsave()
        if res:
            self.copyToDir(config_dir, self.backup_path, backup_filename)
            print(f'Redis database:{self.__port} backup successfully')
        else:
            print("Redis db:0 backup failed")

    # def restoreBackUp(self):
    #     config_dir = self.getConfigDir()
    #     directory = self.client.config_get('dir')
    #     # # STOP THE REDIS SERVER
    #     self.client.shutdown()
    #     # # COPY BACKUP TO REDIS DIR
    #     latest_backup = self.__latestBackup()
    #     self.copyToRedisDir(config_dir, directory['dir'], latest_backup)

    def getConfigDir(self):
        d = self.client.config_get('dir')
        dbfilename = self.client.config_get('dbfilename')
        return '%s/%s' % (d['dir'], dbfilename['dbfilename'])

    def __latestBackup(self):
        list_of_files = glob.glob(self.backup_path + '*rdb')
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    @staticmethod
    def copyToDir(rdbFile: str, directory: str, filename: str, ):
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            sys.stderr.write('backupdir: %s is not a directory.\n' % directory)
            return False
        elif os.path.exists(filename):
            sys.stderr.write('backupfile: %s already exists.\n' % filename)
            return False
        shutil.copy2(rdbFile, filename)

    @staticmethod
    def copyToRedisDir(rdbFile: str, directory: str, filename: str):
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            sys.stderr.write('backupdir: %s is not a directory.\n' % directory)
            return False
        shutil.copy2(filename, rdbFile)
