document.addEventListener('DOMContentLoaded', () => {
    const joinBtn = document.getElementById('join-btn');
    if (joinBtn) {
        joinBtn.addEventListener('mouseover', () => {
            joinBtn.style.boxShadow = '0 0 15px rgba(99, 102, 241, 0.7)';
        });
        joinBtn.addEventListener('mouseout', () => {
            joinBtn.style.boxShadow = 'none';
        });
    }
});