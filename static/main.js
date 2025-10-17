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

    // Add loading state to buttons (except file upload forms)
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        // Skip if this is a file upload form
        const form = button.closest('form');
        if (form && form.enctype === 'multipart/form-data') {
            console.log('Skipping loading state for file upload form');
            return;
        }
        
        button.addEventListener('click', function(e) {
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

    // (Removed form delete handler - now using AJAX buttons only)

    // File upload preview and validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const file = this.files[0];
            console.log('File selected:', file);
            
            if (file) {
                // Check file type
                if (!file.name.toLowerCase().endsWith('.csv')) {
                    alert('กรุณาเลือกไฟล์ .csv เท่านั้น');
                    this.value = '';
                    return;
                }
                
                // Check file size (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    alert('ไฟล์มีขนาดใหญ่เกินไป (เกิน 10MB)');
                    this.value = '';
                    return;
                }
                
                const fileInfo = document.createElement('div');
                fileInfo.className = 'mt-2 text-success small';
                fileInfo.innerHTML = `<i class="fas fa-check me-1"></i>ไฟล์: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
                
                // Remove existing file info
                const existingInfo = this.parentNode.querySelector('.file-info');
                if (existingInfo) {
                    existingInfo.remove();
                }
                
                fileInfo.classList.add('file-info');
                this.parentNode.appendChild(fileInfo);
                
                console.log('File validated successfully:', file.name, file.size);
            }
        });
    });

    // Debug form submission for CSV import
    const importForms = document.querySelectorAll('form[enctype="multipart/form-data"]');
    console.log('Found file upload forms:', importForms.length);
    
    importForms.forEach(function(form, index) {
        console.log(`Setting up form ${index}:`, form);
        form.addEventListener('submit', function(e) {
            console.log('=== FORM SUBMIT EVENT ===');
            const fileInput = form.querySelector('input[type="file"]');
            const file = fileInput ? fileInput.files[0] : null;
            
            console.log('Form action:', form.action || 'default');
            console.log('Form method:', form.method);
            console.log('File input:', fileInput);
            console.log('Selected file:', file);
            
            if (!file) {
                console.log('NO FILE - STOPPING SUBMISSION');
                e.preventDefault();
                alert('กรุณาเลือกไฟล์ CSV');
                return false;
            }
            
            if (!file.name.toLowerCase().endsWith('.csv')) {
                console.log('NOT CSV FILE - STOPPING SUBMISSION');
                e.preventDefault();
                alert('กรุณาเลือกไฟล์ .csv เท่านั้น');
                return false;
            }
            
            console.log('Form submission validated, proceeding...');
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
