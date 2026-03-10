/**
 * Main JavaScript file for Comment Sentiment Analysis Application
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are used
    initializeTooltips();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Add form validation
    addFormValidation();
    
    // Initialize alert auto-dismiss
    initializeAlertAutoDismiss();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add smooth scrolling to anchor links
 */
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Add form validation
 */
function addFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function initializeAlertAutoDismiss() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

/**
 * Analyze comment using API
 */
async function analyzeComment(comment) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment: comment })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error analyzing comment:', error);
        throw error;
    }
}

/**
 * Get dataset statistics using API
 */
async function getDatasetStats() {
    try {
        const response = await fetch('/api/dataset-stats');
        
        if (!response.ok) {
            throw new Error('Failed to fetch stats');
        }
        
        const stats = await response.json();
        return stats;
    } catch (error) {
        console.error('Error fetching dataset stats:', error);
        throw error;
    }
}

/**
 * Display loading spinner
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

/**
 * Hide loading spinner
 */
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '11';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    document.getElementById('toastContainer').appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Format sentiment score with color
 */
function formatSentimentScore(score) {
    let color = 'secondary';
    let icon = 'meh';
    
    if (score > 0) {
        color = 'success';
        icon = 'smile';
    } else if (score < 0) {
        color = 'danger';
        icon = 'frown';
    }
    
    return `<span class="text-${color}"><i class="fas fa-${icon}"></i> ${score}</span>`;
}

/**
 * Format sentiment badge
 */
function formatSentimentBadge(sentiment) {
    const badgeClass = {
        'Positive': 'success',
        'Negative': 'danger',
        'Neutral': 'secondary'
    }[sentiment] || 'secondary';
    
    const icon = {
        'Positive': 'smile',
        'Negative': 'frown',
        'Neutral': 'meh'
    }[sentiment] || 'meh';
    
    return `<span class="badge bg-${badgeClass}"><i class="fas fa-${icon}"></i> ${sentiment}</span>`;
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy to clipboard', 'danger');
    });
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename = 'results.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let row of rows) {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        
        for (let col of cols) {
            csvRow.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        }
        
        csv.push(csvRow.join(','));
    }
    
    // Download CSV
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

/**
 * Validate comment input
 */
function validateComment(comment) {
    if (!comment || comment.trim().length === 0) {
        return {
            valid: false,
            message: 'Please enter a comment'
        };
    }
    
    if (comment.trim().length < 3) {
        return {
            valid: false,
            message: 'Comment must be at least 3 characters long'
        };
    }
    
    return {
        valid: true,
        message: ''
    };
}

/**
 * Highlight sentiment words in text
 */
function highlightSentimentWords(text, positiveWords, negativeWords) {
    let highlightedText = text;
    
    // Highlight positive words
    positiveWords.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        highlightedText = highlightedText.replace(regex, `<mark class="bg-success text-white">${word}</mark>`);
    });
    
    // Highlight negative words
    negativeWords.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, 'gi');
        highlightedText = highlightedText.replace(regex, `<mark class="bg-danger text-white">${word}</mark>`);
    });
    
    return highlightedText;
}

/**
 * Calculate reading time
 */
function calculateReadingTime(text) {
    const wordsPerMinute = 200;
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / wordsPerMinute);
    return minutes;
}

/**
 * Debounce function for search inputs
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Get sentiment color
 */
function getSentimentColor(sentiment) {
    const colors = {
        'Positive': '#28a745',
        'Negative': '#dc3545',
        'Neutral': '#6c757d'
    };
    return colors[sentiment] || colors['Neutral'];
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        analyzeComment,
        getDatasetStats,
        showLoading,
        hideLoading,
        showToast,
        formatSentimentScore,
        formatSentimentBadge,
        copyToClipboard,
        exportTableToCSV,
        validateComment,
        highlightSentimentWords,
        calculateReadingTime,
        debounce,
        formatNumber,
        getSentimentColor
    };
}
