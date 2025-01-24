from zoneinfo import ZoneInfo
from datetime import datetime

class DatetimeUtils:

    @staticmethod
    def now(strftime='%Y-%m-%dT%H:%M:%S', zone_info='America/Sao_Paulo') -> str:
        dt_utc = datetime.now(ZoneInfo('UTC'))
        
        return dt_utc.astimezone(ZoneInfo(zone_info)).strftime(strftime)
    
    @staticmethod
    def parse_by_zone(dt_utc, strftime='%Y-%m-%dT%H:%M:%S', zone_info='America/Sao_Paulo') -> str:
        
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=ZoneInfo('UTC'))
        
        return dt_utc.astimezone(ZoneInfo(zone_info)).strftime(strftime)

    def parse(dt_utc, strftime) -> str:
        
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=ZoneInfo('UTC'))

        if strftime is None:
            strftime = '%Y-%m-%dT%H:%M:%S'
        
        return dt_utc.strftime(strftime)