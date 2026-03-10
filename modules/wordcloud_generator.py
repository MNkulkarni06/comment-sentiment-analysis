
from wordcloud import WordCloud
from collections import Counter
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64

class WordCloudGenerator:
    """
    Generates word clouds for sentiment visualization
    """
    2
    def __init__(self, width=800, height=400):
        """
        Initialize the word cloud generator
        
        Args:
            width (int): Width of the word cloud image
            height (int): Height of the word cloud image
        """
        self.width = width
        self.height = height
        self.default_colormap = {
            'positive': 'Greens',
            'negative': 'Reds',
            'neutral': 'Blues',
            'all': 'viridis'
        }
    
    def generate_word_frequency(self, tokens_list):
        """
        Generate word frequency dictionary from tokens
        
        Args:
            tokens_list (list): List of token lists or single token list
            
        Returns:
            dict: Word frequency dictionary
        """
        if not tokens_list:
            return {}
        
        # Flatten the list if it's a list of lists
        if isinstance(tokens_list[0], list):
            all_tokens = [token for tokens in tokens_list for token in tokens]
        else:
            all_tokens = tokens_list
        
        # Count word frequencies
        word_freq = Counter(all_tokens)
        
        return dict(word_freq)
    
    def create_wordcloud(self, word_freq, colormap='viridis', background_color='white'):
        """
        Create a word cloud from word frequency dictionary
        
        Args:
            word_freq (dict): Word frequency dictionary
            colormap (str): Matplotlib colormap name
            background_color (str): Background color
            
        Returns:
            WordCloud: Generated word cloud object
        """
        if not word_freq:
            # Return empty word cloud
            return None
        
        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            background_color=background_color,
            colormap=colormap,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(word_freq)
        
        return wordcloud
    
    def wordcloud_to_base64(self, wordcloud):
        """
        Convert word cloud to base64 encoded image
        
        Args:
            wordcloud (WordCloud): WordCloud object
            
        Returns:
            str: Base64 encoded image string
        """
        if wordcloud is None:
            return None
        
        # Create figure
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        
        # Encode to base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Close plot to free memory
        plt.close()
        
        return image_base64
    
    def generate_sentiment_wordclouds(self, results):
        """
        Generate word clouds for different sentiments
        
        Args:
            results (list): List of sentiment analysis results
            
        Returns:
            dict: Dictionary containing base64 encoded word clouds
        """
        # Separate tokens by sentiment
        positive_tokens = []
        negative_tokens = []
        neutral_tokens = []
        all_tokens = []
        
        for result in results:
            tokens = result.get('tokens', [])
            sentiment = result.get('sentiment', 'Neutral')
            
            all_tokens.extend(tokens)
            
            if sentiment == 'Positive':
                positive_tokens.extend(tokens)
            elif sentiment == 'Negative':
                negative_tokens.extend(tokens)
            else:
                neutral_tokens.extend(tokens)
        
        # Generate word frequencies
        all_freq = self.generate_word_frequency(all_tokens)
        positive_freq = self.generate_word_frequency(positive_tokens)
        negative_freq = self.generate_word_frequency(negative_tokens)
        neutral_freq = self.generate_word_frequency(neutral_tokens)
        
        # Generate word clouds
        wordclouds = {}
        
        # All comments word cloud
        if all_freq:
            wc_all = self.create_wordcloud(all_freq, self.default_colormap['all'])
            wordclouds['all'] = self.wordcloud_to_base64(wc_all)
        
        # Positive word cloud
        if positive_freq:
            wc_positive = self.create_wordcloud(positive_freq, self.default_colormap['positive'])
            wordclouds['positive'] = self.wordcloud_to_base64(wc_positive)
        
        # Negative word cloud
        if negative_freq:
            wc_negative = self.create_wordcloud(negative_freq, self.default_colormap['negative'])
            wordclouds['negative'] = self.wordcloud_to_base64(wc_negative)
        
        # Neutral word cloud
        if neutral_freq:
            wc_neutral = self.create_wordcloud(neutral_freq, self.default_colormap['neutral'])
            wordclouds['neutral'] = self.wordcloud_to_base64(wc_neutral)
        
        return wordclouds
    
    def get_top_words(self, word_freq, top_n=10):
        """
        Get top N most frequent words
        
        Args:
            word_freq (dict): Word frequency dictionary
            top_n (int): Number of top words to return
            
        Returns:
            list: List of tuples (word, frequency)
        """
        if not word_freq:
            return []
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:top_n]
