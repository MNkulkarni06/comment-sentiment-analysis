
import csv
import os

class DataLoader:
    """
    Loads and validates comment data from CSV files
    """
    
    def __init__(self):
        """Initialize the data loader"""
        pass
    
    def load_csv(self, filepath, comment_column='comment'):
        """
        Load comments from CSV file
        
        Args:
            filepath (str): Path to CSV file
            comment_column (str): Name of the column containing comments
            
        Returns:
            list: List of comments
        """
        comments = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    comment = row.get(comment_column, '').strip()
                    if comment:  # Only add non-empty comments
                        comments.append(comment)
            
            return comments
        
        except FileNotFoundError:
            print(f"Error: File {filepath} not found")
            return []
        
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return []
    
    def validate_comments(self, comments):
        """
        Validate and filter comments
        
        Args:
            comments (list): List of comments
            
        Returns:
            list: List of valid comments
        """
        valid_comments = []
        
        for comment in comments:
            # Check if comment is a string
            if not isinstance(comment, str):
                continue
            
            # Remove leading/trailing whitespace
            comment = comment.strip()
            
            # Check if comment is not empty
            if comment:
                valid_comments.append(comment)
        
        return valid_comments
    
    def load_and_validate(self, filepath, comment_column='comment'):
        """
        Load and validate comments from CSV file
        
        Args:
            filepath (str): Path to CSV file
            comment_column (str): Name of the column containing comments
            
        Returns:
            tuple: (comments, metadata)
        """
        comments = self.load_csv(filepath, comment_column)
        valid_comments = self.validate_comments(comments)
        
        metadata = {
            'total_loaded': len(comments),
            'valid_comments': len(valid_comments),
            'invalid_comments': len(comments) - len(valid_comments),
            'source_file': os.path.basename(filepath)
        }
        
        return valid_comments, metadata
    
    def get_sample_comments(self, comments, n=5):
        """
        Get a sample of comments
        
        Args:
            comments (list): List of comments
            n (int): Number of samples to return
            
        Returns:
            list: Sample of comments
        """
        return comments[:n] if len(comments) >= n else comments
