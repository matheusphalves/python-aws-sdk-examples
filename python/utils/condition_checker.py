from typing import List, Callable, Dict, Any, Tuple
from collections import defaultdict


class DataFilter:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def validate_by_conditions(data: List[Dict[str, Any]], conditions: List[Callable[[Dict[str, Any]], bool]]) -> Tuple[List[Any], List[Any]]:
        # Initialize the lists of records
        passed_records = []
        failed_records = []

        if not data:
            return (passed_records, failed_records)

        # Process each record to determine its status based on all conditions
        for record in data:
            passed = all(condition(record) for condition in conditions)
            if passed:
                passed_records.append(record)
            else:
                failed_records.append(record)
        
        return (passed_records, failed_records)
    
    @staticmethod
    def find_duplicate_records_by_keys(data: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
        if not data:
            return []
        
        if not keys:
            return []
        
        record_groups = defaultdict(list)
        
        for record in data:
            key_tuple = tuple(record.get(key) for key in keys)
            record_groups[key_tuple].append(record)
        
        duplicates = []
        for key_tuple, group in record_groups.items():
            if len(group) > 1:
                base_record = {key: value for key, value in zip(keys, key_tuple)}
                result = base_record.copy()  # Create a copy of the base record
                result['duplicates'] = group
                duplicates.append(result)
        
        return duplicates