// ==================== UTILITY FUNCTIONS ====================

/**
 * Show notification to user
 * @param {string} message - Notification message
 * @param {string} type - Type: 'success', 'error', 'info', 'warning'
 * @param {number} duration - Duration in milliseconds
 */
function showNotification(message, type = 'info', duration = 3000) {
    const alertClass = `alert-${type}`;
    const alertElement = document.createElement('div');
    alertElement.className = `alert ${alertClass} alert-dismissible fade show m-3`;
    alertElement.setAttribute('role', 'alert');
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.insertBefore(alertElement, document.querySelector('main'));
    
    if (duration > 0) {
        setTimeout(() => {
            alertElement.remove();
        }, duration);
    }
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Get CSRF token from meta tag or cookie
 */
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

// ==================== FORM HANDLERS ====================

/**
 * Handle form submission with AJAX
 */
document.addEventListener('submit', function(e) {
    if (e.target.classList.contains('ajax-form')) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const url = form.action;
        const method = form.method;
        
        fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Form submitted successfully!', 'success');
                form.reset();
            } else {
                showNotification('An error occurred: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            showNotification('Error: ' + error.message, 'error');
        });
    }
});

// ==================== CODE EDITOR ====================

class CodeEditor {
    constructor(editorId) {
        this.editor = document.getElementById(editorId);
        this.lineNumbers = null;
        this.init();
    }
    
    init() {
        if (!this.editor) return;
        
        // Create line numbers container
        const container = this.editor.parentElement;
        this.lineNumbers = document.createElement('div');
        this.lineNumbers.className = 'line-numbers';
        container.insertBefore(this.lineNumbers, this.editor);
        
        // Handle input
        this.editor.addEventListener('input', () => this.updateLineNumbers());
        this.editor.addEventListener('keydown', (e) => this.handleTab(e));
        this.editor.addEventListener('scroll', () => this.syncScroll());
        
        this.updateLineNumbers();
    }
    
    handleTab(event) {
        if (event.key !== 'Tab') return;
        event.preventDefault();
        
        const start = this.editor.selectionStart;
        const end = this.editor.selectionEnd;
        
        this.editor.value = this.editor.value.substring(0, start) + '\t' + this.editor.value.substring(end);
        this.editor.selectionStart = this.editor.selectionEnd = start + 1;
    }
    
    updateLineNumbers() {
        const lines = this.editor.value.split('\n').length;
        let html = '';
        for (let i = 1; i <= lines; i++) {
            html += i + '\n';
        }
        this.lineNumbers.textContent = html;
    }
    
    syncScroll() {
        this.lineNumbers.scrollTop = this.editor.scrollTop;
    }
    
    getCode() {
        return this.editor.value;
    }
    
    setCode(code) {
        this.editor.value = code;
        this.updateLineNumbers();
    }
}

// ==================== EXERCISE SUBMISSION ====================

class ExerciseSubmitter {
    constructor(exerciseId) {
        this.exerciseId = exerciseId;
        this.submitBtn = document.getElementById('submit-btn');
        this.feedbackDiv = document.getElementById('feedback');
        
        if (this.submitBtn) {
            this.submitBtn.addEventListener('click', () => this.submit());
        }
    }
    
    submit() {
        const codeEditor = new CodeEditor('code-input');
        const code = codeEditor.getCode();
        
        if (!code.trim()) {
            showNotification('Please write some code!', 'warning');
            return;
        }
        
        this.submitBtn.disabled = true;
        this.submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
        
        fetch(`/api/exercise/${this.exerciseId}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ code: code })
        })
        .then(response => response.json())
        .then(data => {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = 'Submit Solution';
            
            if (data.success) {
                const resultClass = data.is_correct ? 'success' : 'warning';
                const message = data.is_correct ? '✓ Correct!' : '✗ Incorrect';
                
                this.feedbackDiv.className = `alert alert-${resultClass}`;
                this.feedbackDiv.innerHTML = `
                    <strong>${message}</strong><br>
                    ${data.feedback}
                    ${data.is_correct ? `<br>Points awarded: ${data.points_awarded}` : ''}
                `;
                this.feedbackDiv.style.display = 'block';
                
                showNotification(message, data.is_correct ? 'success' : 'info');
            }
        })
        .catch(error => {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = 'Submit Solution';
            showNotification('Error: ' + error.message, 'error');
        });
    }
}

// ==================== PROGRESS TRACKER ====================

class ProgressTracker {
    constructor() {
        this.progressBars = document.querySelectorAll('[data-progress]');
    }
    
    updateProgress(moduleId, percentage) {
        const bar = document.querySelector(`[data-progress="${moduleId}"]`);
        if (bar) {
            bar.style.width = percentage + '%';
            bar.textContent = Math.round(percentage) + '%';
        }
    }
    
    animateProgress(moduleId, startPercent, endPercent, duration = 1000) {
        const start = Date.now();
        const increment = (endPercent - startPercent) / (duration / 16);
        let current = startPercent;
        
        const animate = () => {
            current += increment;
            if (current <= endPercent) {
                this.updateProgress(moduleId, current);
                requestAnimationFrame(animate);
            } else {
                this.updateProgress(moduleId, endPercent);
            }
        };
        
        animate();
    }
}

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    
    // Initialize popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => new bootstrap.Popover(popover));
    
    console.log('ML Learning Pathway loaded successfully!');
});
