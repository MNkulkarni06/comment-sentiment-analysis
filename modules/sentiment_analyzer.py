
import os

class SentimentAnalyzer:
    """
    Lexicon-based sentiment analyzer that classifies text as positive, negative, or neutral
    """
    
    def __init__(self, positive_words_file, negative_words_file):
        """
        Initialize the sentiment analyzer with lexicon files
        
        Args:
            positive_words_file (str): Path to positive words file
            negative_words_file (str): Path to negative words file
        """
        self.positive_words = self._load_lexicon(positive_words_file)
        self.negative_words = self._load_lexicon(negative_words_file)
    
    def _load_lexicon(self, filepath):
        """
        Load lexicon from file
        
        Args:
            filepath (str): Path to lexicon file
            
        Returns:
            set: Set of words in the lexicon
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = {line.strip().lower() for line in f if line.strip()}
            return words
        except FileNotFoundError:
            print(f"Warning: Lexicon file {filepath} not found")
            return set()
        except Exception as e:
            print(f"Error loading lexicon from {filepath}: {e}")
            return set()
    
    def calculate_sentiment_score(self, tokens):
        """
        Calculate sentiment score based on positive and negative word matches
        
        Args:
            tokens (list): List of preprocessed tokens
            
        Returns:
            tuple: (sentiment_score, positive_count, negative_count)
        """
        positive_count = 0
        negative_count = 0
        
        for token in tokens:
            if token in self.positive_words:
                positive_count += 1
            elif token in self.negative_words:
                negative_count += 1
        
        sentiment_score = positive_count - negative_count
        
        return sentiment_score, positive_count, negative_count
    
    def classify_sentiment(self, tokens):
        """
        Classify sentiment based on tokens
        
        Args:
            tokens (list): List of preprocessed tokens
            
        Returns:
            dict: Dictionary containing sentiment classification and details
        """
        score, pos_count, neg_count = self.calculate_sentiment_score(tokens)
        
        # Determine sentiment category
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': pos_count,
            'negative_count': neg_count
        }
    
    def analyze_text(self, text, tokens):
        """
        Analyze sentiment of a single text
        
        Args:
            text (str): Original text
            tokens (list): Preprocessed tokens
            
        Returns:
            dict: Complete sentiment analysis result
        """
        result = self.classify_sentiment(tokens)
        result['original_text'] = text
        result['tokens'] = tokens
        
        return result
    
    def analyze_multiple(self, texts_with_tokens):
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts_with_tokens (list): List of tuples (text, tokens)
            
        Returns:
            list: List of sentiment analysis results
        """
        results = []
        for text, tokens in texts_with_tokens:
            result = self.analyze_text(text, tokens)
            results.append(result)
        
        return results
    
    def get_sentiment_distribution(self, results):
        """
        Calculate sentiment distribution from results
        
        Args:
            results (list): List of sentiment analysis results
            
        Returns:
            dict: Sentiment distribution statistics
        """
        total = len(results)
        if total == 0:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_percent': 0,
                'negative_percent': 0,
                'neutral_percent': 0
            }
        
        positive = sum(1 for r in results if r['sentiment'] == 'Positive')
        negative = sum(1 for r in results if r['sentiment'] == 'Negative')
        neutral = sum(1 for r in results if r['sentiment'] == 'Neutral')
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_percent': round((positive / total) * 100, 2),
            'negative_percent': round((negative / total) * 100, 2),
            'neutral_percent': round((neutral / total) * 100, 2)
        }
    
    def get_matched_words(self, tokens):
        """
        Get lists of matched positive and negative words
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            dict: Dictionary with positive and negative word lists
        """
        positive_matches = [token for token in tokens if token in self.positive_words]
        negative_matches = [token for token in tokens if token in self.negative_words]
        
        return {
            'positive_words': positive_matches,
            'negative_words': negative_matches
        }
