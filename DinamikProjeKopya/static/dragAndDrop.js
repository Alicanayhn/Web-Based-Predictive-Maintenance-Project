const cards = document.querySelectorAll('.draggable');
let dragged = null;

console.log(cards)

cards.forEach(card => {
    card.addEventListener('dragstart', (e) => {
        
        dragged = e.target;
        setTimeout(() => {
            e.target.classList.add('dragging');
        }, 0);
    });

    card.addEventListener('dragend', (e) => {
        setTimeout(() => {
            dragged.classList.remove('dragging');
            dragged = null;
        }, 0);
    });
});

const container = document.querySelectorAll('.row');

container.forEach(row => {
    row.addEventListener('dragover', (e) => {

        e.preventDefault();
        const afterElement = getDragAfterElement(row, e.clientY);
        if (afterElement == null) {
            row.appendChild(dragged);
        } else {
            row.insertBefore(dragged, afterElement);
        }
    });
});


function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {

        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}