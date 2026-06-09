from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path_or_stream):
        """
        Parses a document file path or file-like object and returns structured data.
        
        Args:
            file_path_or_stream: Path to the file (str) or a file-like object (bytes stream).
            
        Returns:
            dict: Structured data extracted from the document.
        """
        pass
