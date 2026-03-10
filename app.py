from flask import Flask, render_template, request, jsonify, send_file
import os
import sys

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.text_preprocessor import TextPreprocessor
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.wordcloud_generator import WordCloudGenerator
from modules.data_loader import DataLoader

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sentiment-analysis-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'static', 'datasets')
POSITIVE_WORDS_FILE = os.path.join(DATASET_DIR, 'positive_words.txt')
NEGATIVE_WORDS_FILE = os.path.join(DATASET_DIR, 'negative_words.txt')
DEFAULT_DATASET_FILE = os.path.join(DATASET_DIR, 'comments.csv')

# Initialize modules
text_preprocessor = TextPreprocessor()
sentiment_analyzer = SentimentAnalyzer(POSITIVE_WORDS_FILE, NEGATIVE_WORDS_FILE)
wordcloud_generator = WordCloudGenerator()
data_loader = DataLoader()

# Global variable to store current analysis results (in-memory storage)
current_results = None


@app.route('/')
def index():
    """
    Home page route
    """
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """
    Analyze comments from dataset and display results
    """
    global current_results
    
    if request.method == 'POST':
        # Load dataset
        comments, metadata = data_loader.load_and_validate(DEFAULT_DATASET_FILE)
        
        if not comments:
            return render_template('analyze.html', 
                                 error="No valid comments found in dataset")
        
        # Preprocess comments
        preprocessed_data = []
        for comment in comments:
            tokens = text_preprocessor.preprocess(comment)
            preprocessed_data.append((comment, tokens))
        
        # Perform sentiment analysis
        results = sentiment_analyzer.analyze_multiple(preprocessed_data)
        
        # Calculate sentiment distribution
        distribution = sentiment_analyzer.get_sentiment_distribution(results)
        
        # Generate word clouds
        wordclouds = wordcloud_generator.generate_sentiment_wordclouds(results)
        
        # Store results in memory
        current_results = {
            'results': results,
            'distribution': distribution,
            'wordclouds': wordclouds,
            'metadata': metadata
        }
        
        return render_template('analyze.html',
                             results=results,
                             distribution=distribution,
                             wordclouds=wordclouds,
                             metadata=metadata,
                             show_results=True)
    
    return render_template('analyze.html')


@app.route('/single-analysis', methods=['GET', 'POST'])
def single_analysis():
    """
    Analyze a single comment entered by user
    """
    if request.method == 'POST':
        comment = request.form.get('comment', '').strip()
        
        if not comment:
            return render_template('single_analysis.html',
                                 error="Please enter a comment to analyze")
        
        # Preprocess comment
        tokens = text_preprocessor.preprocess(comment)
        
        if not tokens:
            return render_template('single_analysis.html',
                                 error="No valid words found in comment after preprocessing",
                                 comment=comment)
        
        # Perform sentiment analysis
        result = sentiment_analyzer.analyze_text(comment, tokens)
        
        # Get matched words
        matched_words = sentiment_analyzer.get_matched_words(tokens)
        
        # Generate word cloud for single comment
        word_freq = wordcloud_generator.generate_word_frequency(tokens)
        
        # Determine colormap based on sentiment
        colormap_map = {
            'Positive': 'Greens',
            'Negative': 'Reds',
            'Neutral': 'Blues'
        }
        colormap = colormap_map.get(result['sentiment'], 'viridis')
        
        wordcloud_obj = wordcloud_generator.create_wordcloud(word_freq, colormap)
        wordcloud_base64 = wordcloud_generator.wordcloud_to_base64(wordcloud_obj)
        
        return render_template('single_analysis.html',
                             result=result,
                             matched_words=matched_words,
                             wordcloud=wordcloud_base64,
                             comment=comment,
                             show_result=True)
    
    return render_template('single_analysis.html')


@app.route('/results')
def results():
    """
    Display detailed results from the last analysis
    """
    global current_results
    
    if current_results is None:
        return render_template('results.html',
                             error="No analysis results available. Please run analysis first.")
    
    return render_template('results.html',
                         results=current_results['results'],
                         distribution=current_results['distribution'],
                         wordclouds=current_results['wordclouds'],
                         metadata=current_results['metadata'])


@app.route('/about')
def about():
    """
    About page with project information
    """
    return render_template('about.html')


@app.route('/documentation')
def documentation():
    """
    Documentation page with system information
    """
    # Get lexicon statistics
    pos_words_count = len(sentiment_analyzer.positive_words)
    neg_words_count = len(sentiment_analyzer.negative_words)
    
    doc_info = {
        'positive_words_count': pos_words_count,
        'negative_words_count': neg_words_count,
        'total_lexicon_words': pos_words_count + neg_words_count,
        'stop_words_count': len(text_preprocessor.stop_words)
    }
    
    return render_template('documentation.html', doc_info=doc_info)


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API endpoint for sentiment analysis
    """
    data = request.get_json()
    
    if not data or 'comment' not in data:
        return jsonify({'error': 'No comment provided'}), 400
    
    comment = data['comment'].strip()
    
    if not comment:
        return jsonify({'error': 'Empty comment'}), 400
    
    # Preprocess and analyze
    tokens = text_preprocessor.preprocess(comment)
    result = sentiment_analyzer.analyze_text(comment, tokens)
    
    return jsonify(result)


@app.route('/api/dataset-stats')
def api_dataset_stats():
    """
    API endpoint to get dataset statistics
    """
    comments, metadata = data_loader.load_and_validate(DEFAULT_DATASET_FILE)
    
    return jsonify({
        'total_comments': len(comments),
        'metadata': metadata
    })


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """
    Handle 500 errors
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
    
    # Run the application
    print("Starting Comment Sentiment Analysis Application...")
    print(f"Dataset directory: {DATASET_DIR}")
    print(f"Positive words loaded: {len(sentiment_analyzer.positive_words)}")
    print(f"Negative words loaded: {len(sentiment_analyzer.negative_words)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
