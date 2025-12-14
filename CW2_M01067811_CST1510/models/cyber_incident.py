from datetime import datetime

class SecurityIncident:
    """Represents cyber incident in the platform"""

    def __init__(self,incident_id:int,title:str,severity:str,status:str,description: str = "", date: str = None, 
                 incident_type: str = "", reported_by: str = ""):
        self.__id=incident_id
        self.__title = title
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__date = date or datetime.now().strftime('%Y-%m-%d')
        self.__incident_type = incident_type
        self.__reported_by = reported_by

    @property
    def id(self):
        return self.__id
    
    @property
    def title(self) :
        return self.__title
    
    @property
    def severity(self) :
        return self.__severity
    
    @property
    def status(self) :
        return self.__status
    
    @property
    def description(self) :
        return self.__description
    
    def update_status(self, new_status: str) :
        """Update the status of the incident."""
        self.__status = new_status
    
    def get_severity_level(self) -> int:
        """Get numeric severity level (1-4)"""
        severity_map = {
            "low": 1,
            "medium": 2, 
            "high": 3,
            "critical": 4
        }
        return severity_map.get(self.__severity.lower(), 0)
    
    def to_dict(self) -> dict:
        """Converting to dictionary for DataFrame"""
        return {
            'id': self.__id,
            'title': self.__title,
            'severity': self.__severity,
            'status': self.__status,
            'description': self.__description,
            'date': self.__date,
            'incident_type': self.__incident_type
        }
    
    def __str__(self) -> str:
        return f"Incident #{self.__id}: {self.__title} [{self.__severity}]"
    
    

