// IT Business Shop - Main JavaScript
console.log('IT Business Shop loaded successfully!');

// Smooth scrolling for navigation
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 150);
        }, 5000);
    });

    // Add loading state to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>กำลังประมวลผล...';
            button.disabled = true;
            
            // Re-enable after form submission (in case of validation errors)
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        });
    });

    // Format number inputs
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Handle delete confirmation
    const deleteForms = document.querySelectorAll('form[action*="/delete"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const confirmMessage = form.getAttribute('data-confirm') || 'คุณแน่ใจที่จะลบรายการนี้หรือไม่?';
            if (!confirm(confirmMessage)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const fileInfo = document.createElement('div');
                fileInfo.className = 'mt-2 text-muted small';
                fileInfo.innerHTML = `<i class="fas fa-file me-1"></i>ไฟล์: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
                
                // Remove existing file info
                const existingInfo = this.parentNode.querySelector('.file-info');
                if (existingInfo) {
                    existingInfo.remove();
                }
                
                fileInfo.classList.add('file-info');
                this.parentNode.appendChild(fileInfo);
            }
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('th-TH', {
        style: 'currency',
        currency: 'THB',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// AJAX Delete Function
function deleteEntry(entryId) {
    if (!confirm(`ต้องการลบรายการ ID: ${entryId} หรือไม่?`)) {
        return false;
    }
    
    console.log(`Attempting to delete entry ID: ${entryId}`);
    
    fetch(`/entry/${entryId}/delete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => {
        console.log('Delete response:', response.status);
        if (response.ok) {
            showToast('ลบรายการเรียบร้อยแล้ว', 'success');
            // Reload page to show updated list
            setTimeout(() => window.location.reload(), 1000);
        } else {
            showToast('เกิดข้อผิดพลาดในการลบ', 'error');
        }
    })
    .catch(error => {
        console.error('Delete error:', error);
        showToast('เกิดข้อผิดพลาดในการลบ: ' + error, 'error');
    });
    
    return false;
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(function() {
        toast.remove();
    }, 3000);
}
