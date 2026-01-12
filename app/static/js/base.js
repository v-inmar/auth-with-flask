// Make sure dom loaded before executing any scripts
document.addEventListener('DOMContentLoaded', () => {
    triggerFlashModal();
});


const triggerFlashModal  = () => {
    const flashModalElement = document.getElementById('flashModal');
    const flashModal = new bootstrap.Modal(flashModalElement);

    const flashModalBodyElement = document.getElementById('flashModalBody');
    if (flashModalBodyElement.children.length > 0) {
        flashModal.show();
    }
};


