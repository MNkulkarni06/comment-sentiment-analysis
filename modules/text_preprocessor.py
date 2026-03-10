
import re
import string

class TextPreprocessor:
    """
    Handles all text preprocessing operations including:
    - Text cleaning
    - Normalization
    - Tokenization
    - Stop word removal
    """
    
    def __init__(self):
        """Initialize the preprocessor with common stop words"""
        self.stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this', 'that',
            'it', 'from', 'are', 'was', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could',
            'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'we',
            'they', 'them', 'their', 'my', 'your', 'his', 'her', 'its',
            'our', 'me', 'him', 'us', 'what', 'when', 'where', 'who',
            'how', 'why', 'am', 'so', 'than', 'too', 'very', 'just',
            'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under',
            'again', 'further', 'then', 'once', 'here', 'there', 'all',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'only', 'own', 'same', 'than', 'not', 'no', 'nor', 'if', 'also'
        }
    
    def clean_text(self, text):
        """
        Clean text by removing special characters, punctuation, and numbers
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def normalize_text(self, text):
        """
        Normalize text by converting to lowercase
        
        Args:
            text (str): Input text
            
        Returns:
            str: Normalized text
        """
        return text.lower()
    
    def tokenize(self, text):
        """
        Split text into individual tokens (words)
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of tokens
        """
        return text.split()
    
    def remove_stop_words(self, tokens):
        """
        Remove common stop words from token list
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Filtered list of tokens
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Raw input text
            
        Returns:
            list: List of preprocessed tokens
        """
        if not text or not isinstance(text, str):
            return []
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Normalize text
        normalized_text = self.normalize_text(cleaned_text)
        
        # Tokenize
        tokens = self.tokenize(normalized_text)
        
        # Remove stop words
        filtered_tokens = self.remove_stop_words(tokens)
        
        # Remove empty tokens
        filtered_tokens = [token for token in filtered_tokens if token.strip()]
        
        return filtered_tokens
    
    def preprocess_multiple(self, texts):
        """
        Preprocess multiple texts
        
        Args:
            texts (list): List of text strings
            
        Returns:
            list: List of preprocessed token lists
        """
        return [self.preprocess(text) for text in texts]
