
from dagster import ConfigurableResource
from pydantic import PrivateAttr
from sqlalchemy import create_engine, text, Engine
import pandas as pd

class StarRocksResource(ConfigurableResource):
    host: str
    port: int = 19030
    username: str
    password: str
    database: str
    
    _engine: Engine = PrivateAttr(default=None)
    
    @property
    def connection_string(self) -> str:
        return f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        
    def get_engine(self):
        if self._engine is None:
            # Create engine with connection pooling
            # pool_pre_ping=True handles dropped connections gracefully
            self._engine = create_engine(
                self.connection_string, 
                pool_pre_ping=True, 
                pool_size=5, 
                max_overflow=10
            )
        return self._engine
        
    def execute_query(self, sql: str):
        with self.get_engine().connect() as conn:
            return pd.read_sql(text(sql), conn)
            
    def load_pandas(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
        df.to_sql(
            table_name, 
            con=self.get_engine(), 
            if_exists=if_exists, 
            index=False,
            method='multi', 
            chunksize=1000
        )
