from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 创建数据库连接
engine = create_engine("mysql+pymysql://root:Mjy123456~@localhost/test1")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型
Base = declarative_base()